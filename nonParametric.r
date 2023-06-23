library(ARTool)
library(tidyr)
library(rcompanion)
library(rstatix)
library(ini)
library(rstudioapi)
library(stringr)

# Read the config file
currentFolder <- str_sub(getSourceEditorContext()$path, 1, -17) # -17 to remove the file name
print(currentFolder)
configPath <- paste(currentFolder, "/config.ini", sep = "")
config <- read.ini(configPath, encoding = "UTF-8")

# Access and print the values
# print(config)

#read csv file
rgCalcData <- read.csv(config$FILES$rgCalcResultsCSVFile, header = TRUE, sep = ",")
print(rgCalcData)

#extract (s or f) and (num or act) respectively as two variables 
speed = c(); numOrAct = c()
for (i in rgCalcData$type) {
  speed = append(speed, substr(i, 1, 1))
  numOrAct = append(numOrAct, substr(i, 2, 4))
}

sortedDataR = data.frame(rgCalcData$subject, speed, numOrAct, rgCalcData$R)

sortedDataAll = data.frame(rgCalcData[1], speed, numOrAct, rgCalcData[,c(4:60)])

colnames(sortedDataR)[1] <- "subject"
colnames(sortedDataR)[4] <- "R"

#踢掉董
rgCalcData <- subset(rgCalcData, subject != "3")
sortedDataR <- subset(sortedDataR, subject != "3")

#art analysis and effect size
resultRand <- art(R ~ factor(speed) * factor(numOrAct) + Error(factor(subject)), data = sortedDataR)
result <- anova(resultRand)
print(result, verbose = TRUE)

result$eta.sq.part = with(result, `Sum Sq`/(`Sum Sq` + `Sum Sq.res`))
result
#The interaction is significant and both main effects are significant.

#Use the non-parametric method to calculate the simple main effects
#speed
speedS = subset(sortedDataR, speed == "s")
speedF = subset(sortedDataR, speed == "f")
speedS = speedS[,c("subject","R")]
speedF = speedF[,c("subject","R")]


#numOrAct
num = subset(sortedDataR, numOrAct == "num")
act = subset(sortedDataR, numOrAct == "act")
num = num[,c("subject","R")]
act = act[,c("subject","R")]

#simple main effect
#speed
speedS = speedS[order(speedS$subject),]
speedF = speedF[order(speedF$subject),]
speedS = speedS[,c("R")]
speedF = speedF[,c("R")]
speed = cbind(speedS, speedF)
speed = as.data.frame(speed)
speed = gather(data = speed, key = speed, value = R, speedS, speedF)
speed$speed = factor(speed$speed)
speed
#numOrAct 
num = num[order(num$subject),]
act = act[order(act$subject),]
num = num[,c("R")]
act = act[,c("R")]
numOrAct = cbind(num, act)
numOrAct = as.data.frame(numOrAct)
numOrAct = gather(data = numOrAct, key = numOrAct, value = R, num, act)
numOrAct$numOrAct = factor(numOrAct$numOrAct)
numOrAct





#use wilcoxon test to do multiple comparison

#speed
multiSpeed = wilcox.test(sortedDataR[sortedDataR$speed == "s",]$R, sortedDataR[sortedDataR$speed == "f",]$R, paired = TRUE)
multiSpeed
multiNumOrAct = wilcox.test(sortedDataR[sortedDataR$numOrAct == "num",]$R, sortedDataR[sortedDataR$numOrAct == "act",]$R, paired = TRUE)
multiNumOrAct

#effect size
effsizeSpeed <- wilcox_effsize(sortedDataR, R ~ speed, paired = TRUE, conf.level = 0.95)
effsizeSpeed




library(ggplot2)
library(plyr)

# Calculate bootstrapped standard errors for each participant
se_df <- ddply(sortedDataR, .(subject, speed, numOrAct), summarise, se = sd(R)/sqrt(length(R)))
se_df$se[is.na(se_df$se)] <- 0  # Replace NAs with zeros

# Merge the standard error data with the original data
sortedDataR <- merge(sortedDataR, se_df, by = c("subject", "speed", "numOrAct"))

# Plot the data with error bars
ggplot(sortedDataR, aes(x = numOrAct, y = R, color = speed, group = interaction(speed, subject))) +
  geom_point(size = 3, position = position_dodge(width = 0.8)) +
  geom_errorbar(aes(ymin = R - se, ymax = R + se), position = position_dodge(width = 0.8), width = 0.2) +
  facet_wrap(~subject, scales = "free") +
  labs(x = "numOrAct", y = "R", color = "speed") +
  theme_classic() +
  theme(legend.position = "bottom")
