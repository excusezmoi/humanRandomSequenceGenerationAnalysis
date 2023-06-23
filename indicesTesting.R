library(ARTool)
library(tidyr)
library(rcompanion)
library(rstatix)
library(ini)
library(rstudioapi)
library(stringr)

# Read the config file
currentFolder <- str_sub(getSourceEditorContext()$path, 1, -18) # -18 to remove the file name
configPath <- paste(currentFolder, "/config.ini", sep = "")
config <- read.ini(configPath, encoding = "UTF-8")

# Access and print the values
# print(config)

#read csv file
rgCalcData <- read.csv(config$FILES$rgCalcResultsCSVFile, header = TRUE, sep = ",")
print(rgCalcData)

#extract (s or f) and (num or act) respectively as two variables
speed <- c(); numOrAct <- c()
for (i in rgCalcData$type) {
  speed <- append(speed, substr(i, 1, 1))
  numOrAct <- append(numOrAct, substr(i, 2, 4))
}

sortedDataAll <- data.frame(rgCalcData[1], speed, numOrAct, rgCalcData[, c(4:60)])

#踢掉董
rgCalcData <- subset(rgCalcData, subject != "3")
sortedDataAll <- subset(sortedDataAll, subject != "3")


#R art analysis and effect size
resultRand <- art(R ~ factor(speed) * factor(numOrAct) + Error(factor(subject)), data = sortedDataAll)
result <- anova(resultRand)
print(result, verbose = TRUE)

result$"Pr(>F)" #A way to extract the p-values!

#capture.output(result,file="W:/Me/Research/心理/實驗結果/test.xls")

result$eta.sq.part <- with(result, `Sum Sq` / (`Sum Sq` + `Sum Sq.res`))
result
#The interaction is significant and both main effects are significant.

#Bootstrapping participants to do power analysis
numbersToDrawFrom <- c(1, 2, 4, 5, 6, 7, 8, 9)
bootstrappedParticipants <- c()
for (i in 1:10000) {
  bootstrappedParticipants <- append(bootstrappedParticipants, sample(numbersToDrawFrom, 8, replace = TRUE))
}
bootstrappedParticipants <- matrix(bootstrappedParticipants, nrow = 10000, ncol = 8)
bootstrappedParticipants <- as.data.frame(bootstrappedParticipants)
bootstrappedParticipants[1, ]
bootstrappedParticipants[2, ]

# count <- list()

# for (i in 1:9) {
#   count[[i]] <- 0
# }
# count
# count[[2]] = count[[2]] + 1
# count

pValues = data.frame()

for (combination in 1:10000) {
  btData <- data.frame()
  count <- list()
  for (i in 1:9) {
  count[[i]] <- 0
  }
  for (participant in bootstrappedParticipants[combination, ]) {
    addThisTime <- sortedDataAll[sortedDataAll$subject == participant, ]
    count[[participant]] <- count[[participant]] + 1
    addThisTime$subject = paste0(c(addThisTime$subject, count[[participant]]), collapse = "_")
    btData <- rbind(btData, addThisTime)
    # print(btData$subject)
  }
  # print(btData$subject)
  resultRand <- art(R ~ factor(speed) * factor(numOrAct) + Error(factor(subject)), data = btData)
  result <- anova(resultRand)
  # print(result, verbose = TRUE)
  print(result$"Pr(>F)") 
  pValues <- rbind(pValues, result$"Pr(>F)")
}
pValues[1]

#effect 1
count1 <- sum(pValues[1] < 0.05)
count1
power1 <- count1 / 10000
print(power1)

#effect 2
count2 <- sum(pValues[2] < 0.05)
count2
power2 <- count2 / 10000
print(power2)

#effect 3
count3 <- sum(pValues[3] < 0.05)
count3
power3 <- count3 / 10000
print(power3)

#######################################
############################



#Use the non-parametric method to calculate the simple main effects
#speed
speedS <- subset(sortedDataAll, speed == "s")
speedF <- subset(sortedDataAll, speed == "f")
speedS <-speedS[, c("subject", "R")]
speedF <- speedF[, c("subject", "R")]


#numOrAct
num <- subset(sortedDataAll, numOrAct == "num")
act <- subset(sortedDataAll, numOrAct == "act")
num <- num[, c("subject", "R")]
act <- act[, c("subject", "R")]

#simple main effect
#speed
speedS <- speedS[order(speedS$subject),]
speedF <- speedF[order(speedF$subject), ]
speedS <- speedS[, c("R")]
speedF <- speedF[, c("R")]
speed <- cbind(speedS, speedF)
speed <- as.data.frame(speed)
speed <- gather(data = speed, key = speed, value = R, speedS, speedF)
speed$speed = factor(speed$speed)
speed
#numOrAct
num <- num[order(num$subject), ]
act <- act[order(act$subject), ]
num <- num[, c("R")]
act <- act[, c("R")]
numOrAct <- cbind(num, act)
numOrAct <- as.data.frame(numOrAct)
numOrAct <- gather(data = numOrAct, key = numOrAct, value = R, num, act)
numOrAct$numOrAct = factor(numOrAct$numOrAct)
numOrAct





#use wilcoxon test to do multiple comparison

#speed
multiSpeed = wilcox.test(sortedDataAll[sortedDataAll$speed == "s",]$R, sortedDataAll[sortedDataAll$speed == "f",]$R, paired = TRUE)
multiSpeed
multiNumOrAct = wilcox.test(sortedDataAll[sortedDataAll$numOrAct == "num",]$R, sortedDataAll[sortedDataAll$numOrAct == "act",]$R, paired = TRUE)
multiNumOrAct

#effect size
effsizeSpeed <- wilcox_effsize(sortedDataAll, R ~ speed, paired = TRUE, conf.level = 0.95)
effsizeSpeed




library(ggplot2)
library(plyr)

# Calculate bootstrapped standard errors for each participant
se_df <- ddply(sortedDataAll, .(subject, speed, numOrAct), summarise, se = sd(R)/sqrt(length(R)))
se_df$se[is.na(se_df$se)] <- 0  # Replace NAs with zeros

# Merge the standard error data with the original data
sortedDataAll <- merge(sortedDataAll, se_df, by = c("subject", "speed", "numOrAct"))

# Plot the data with error bars
ggplot(sortedDataAll, aes(x = numOrAct, y = R, color = speed, group = interaction(speed, subject))) +
  geom_point(size = 3, position = position_dodge(width = 0.8)) +
  geom_errorbar(aes(ymin = R - se, ymax = R + se), position = position_dodge(width = 0.8), width = 0.2) +
  facet_wrap(~subject, scales = "free") +
  labs(x = "numOrAct", y = "R", color = "speed") +
  theme_classic() +
  theme(legend.position = "bottom")

