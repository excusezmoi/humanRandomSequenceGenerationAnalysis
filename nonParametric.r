library(ARTool)
library(tidyr)
library(rcompanion)
library(rstatix)

#read csv file
dataRandom <- read.csv("W:/Me/Research/心理/0427報告/rgCalcResults/rgCalcResults.csv", header = TRUE, sep = ",")
print(dataRandom)

#extract (s or f) and (num or act) respectively as two variables 
speed = c()
numOrAct = c()
for (i in dataRandom$type) {
  speed = append(speed, substr(i, 1, 1))
  numOrAct = append(numOrAct, substr(i, 2, 4))
}



dataRandom2 = data.frame(dataRandom$subject, speed, numOrAct, dataRandom$R)


dataRandomTry = data.frame(dataRandom[1], speed, numOrAct, dataRandom[,c(4:60)])

colnames(dataRandom2)[1] <- "subject"
colnames(dataRandom2)[4] <- "R"


#踢掉董
dataRandom <- subset(dataRandom, subject != "3")
dataRandom2 <- subset(dataRandom2, subject != "3")



#art analysis and effect size
resultRand <- art(R ~ factor(speed)*factor(numOrAct) + Error(factor(subject)), data=dataRandom2)
result = anova(resultRand)
print(result, verbose = TRUE)

result$eta.sq.part = with(result, `Sum Sq`/(`Sum Sq` + `Sum Sq.res`))
result
#The interaction is significant and both main effects are significant.

#Use the non-parametric method to calculate the simple main effects
#speed
speedS = subset(dataRandom2, speed == "s")
speedF = subset(dataRandom2, speed == "f")
speedS = speedS[,c("subject","R")]
speedF = speedF[,c("subject","R")]


#numOrAct
num = subset(dataRandom2, numOrAct == "num")
act = subset(dataRandom2, numOrAct == "act")
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
multiSpeed = wilcox.test(dataRandom2[dataRandom2$speed == "s",]$R, dataRandom2[dataRandom2$speed == "f",]$R, paired = TRUE)
multiSpeed
multiNumOrAct = wilcox.test(dataRandom2[dataRandom2$numOrAct == "num",]$R, dataRandom2[dataRandom2$numOrAct == "act",]$R, paired = TRUE)
multiNumOrAct

#effect size
effsizeSpeed <- wilcox_effsize(dataRandom2, R ~ speed, paired = TRUE, conf.level = 0.95)
effsizeSpeed




library(ggplot2)
library(plyr)

# Calculate bootstrapped standard errors for each participant
se_df <- ddply(dataRandom2, .(subject, speed, numOrAct), summarise, se = sd(R)/sqrt(length(R)))
se_df$se[is.na(se_df$se)] <- 0  # Replace NAs with zeros

# Merge the standard error data with the original data
dataRandom2 <- merge(dataRandom2, se_df, by = c("subject", "speed", "numOrAct"))

# Plot the data with error bars
ggplot(dataRandom2, aes(x = numOrAct, y = R, color = speed, group = interaction(speed, subject))) +
  geom_point(size = 3, position = position_dodge(width = 0.8)) +
  geom_errorbar(aes(ymin = R - se, ymax = R + se), position = position_dodge(width = 0.8), width = 0.2) +
  facet_wrap(~subject, scales = "free") +
  labs(x = "numOrAct", y = "R", color = "speed") +
  theme_classic() +
  theme(legend.position = "bottom")

