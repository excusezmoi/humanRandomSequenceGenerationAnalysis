library("rstatix")
library(ggplot2)
#library(compute.es)
library(lsr)
library(effsize)
library(ini)
library(rstudioapi)
library(stringr)

totalParticipants = 24

# Read the config file
currentFolder <- str_sub(getSourceEditorContext()$path, 1, -27) # -27 to remove the file name
configPath <- paste(currentFolder, "/config.ini", sep = "")
config <- read.ini(configPath, encoding = "UTF-8")

# Access and print the values
print(config)

#read xlsx file
data = openxlsx::read.xlsx(config$FILES$distanceDataXLSXFile)
data = data[1:totalParticipants,]

#踢人
data <- subset(data, subjectNumber != "3",subjectNumber != "14")
# 可能要踢王俊佑


sdData <- gather(data = data, key = types, value = distance, expectedAverageNumDistance,	sNumDistance,	fNumDistance,	expectedAverageActDistance,	sActDistance,	fActDistance)
sdData
class(sdData$distance)
sdData$distance = as.numeric(sdData$distance)
class(sdData$distance)


# One-way repeated measures ANOVA all: significant
anova_result <- sdData %>% anova_test(distance ~ types + Error(subjectNumber/types))

anova_result
summary(anova_result)

#data <- subset(data, !(subjectNumber %in% c("3", "4")))

#One-way in num: significant
sdDataNum <- gather(data = data, key = types, value = distance, expectedAverageNumDistance,	sNumDistance,	fNumDistance)
sdDataNum$distance = as.numeric(sdDataNum$distance)
sdDataNum$subjectNumber = as.numeric(sdDataNum$subjectNumber)
sdDataNum = sdDataNum[,c("subjectNumber","types","distance")]

#str(sdDataNum)

anova_result_num <- sdDataNum %>% anova_test(distance ~ types + Error(subjectNumber/types))
anova_result_num

#effect size of ANOVA
class(anova_result_num)
anova_result_num[3]
#rstatix::eta_squared(anova_result_num)
#rstatix::eta_squared(anova_result_num$ANOVA)

eta_squared_g <- 0.017  # Replace with your actual value

f_cohen <- sqrt(eta_squared_g / (1 - eta_squared_g))
f_cohen

#plot
# Create a new data frame with the mean and standard error for each condition
sdDataNum$types <- factor(sdDataNum$types)
means <- aggregate(distance ~ types + subjectNumber, sdDataNum, mean)
se <- aggregate(distance ~ types + subjectNumber, sdDataNum, sd) #/ sqrt(length(sdDataNum$subjectNumber))
se$distance <- se$distance/ sqrt(length(sdDataNum$subjectNumber))
means$se <- se$distance

# Plot the data


numSubLabels <- c("expected", "fast", "slow")

ggplot(means, aes(x = types, y = distance)) +
  geom_point(size = 0.5) +
  geom_line(aes(group = subjectNumber)) +
  geom_errorbar(aes(ymin = distance - sd(distance)/sqrt(length(distance)), 
                    ymax = distance + sd(distance)/sqrt(length(distance))),
                width = 0.2)+
  scale_x_discrete(labels = numSubLabels) +  # Change x-axis labels
  labs(x = "Types", y = "Subjective Distance") +
  theme_classic()










# Perform pairwise t-tests and adjust for multiple comparisons using the Holm method
posthoc_results_num <- sdDataNum %>% 
  pairwise_t_test(distance ~ types, 
                  paired = TRUE,
                  p.adjust.method = "holm")

# View the pairwise comparison results
posthoc_results_num
# significant for average VS f and average VS s

paired_t_eff <- sdDataNum %>% cohens_d(distance ~ types, paired = TRUE)
paired_t_eff

# Assuming d_cohen is your Cohen's d value and n is the number of paired observations
d_cohen <- 1.18  # Replace with your actual value
n <- 23  # Replace with your actual value

DZ <- d_cohen / sqrt(n)
DZ




#One-way in act: significant!
sdDataAct <- gather(data = data, key = types, value = distance, expectedAverageActDistance,	sActDistance,	fActDistance)
sdDataAct$distance = as.numeric(sdDataAct$distance)
sdDataAct = sdDataAct[,c("subjectNumber","types","distance")]
anova_result_act <- sdDataAct %>% anova_test(distance ~ types + Error(subjectNumber/types))
anova_result_act



#plot
# Create a new data frame with the mean and standard error for each condition
sdDataAct$types <- factor(sdDataAct$types)
means <- aggregate(distance ~ types + subjectNumber, sdDataAct, mean)
se <- aggregate(distance ~ types + subjectNumber, sdDataAct, sd) #/ sqrt(length(sdDataAct$subjectNumber))
se$distance <- se$distance/ sqrt(length(sdDataAct$subjectNumber))
means$se <- se$distance

# Plot the data
numSubLabels <- c("expected", "fast", "slow")
ggplot(means, aes(x = types, y = distance)) +
  geom_point(size = 0.5) +
  geom_line(aes(group = subjectNumber)) +
  geom_errorbar(aes(ymin = distance - sd(distance)/sqrt(length(distance)), 
                    ymax = distance + sd(distance)/sqrt(length(distance))),
                width = 0.2)+
  
  scale_x_discrete(labels = numSubLabels) + 
  labs(x = "Types", y = "Subjective Distance") +
  theme_classic()


# Perform one-way repeated measures ANOVA on the data
anova_result_act <- sdDataAct %>% anova_test(distance ~ types + Error(subjectNumber/types))

# Perform pairwise t-tests and adjust for multiple comparisons using the Holm method
posthoc_results_act <- sdDataAct %>% 
  pairwise_t_test(distance ~ types, 
                  paired = TRUE,
                  p.adjust.method = "holm")

# View the pairwise comparison results
posthoc_results_act
# significant for f VS s

paired_t_eff <- sdDataAct %>% cohens_d(distance ~ types, paired = TRUE)
paired_t_eff





#realdata: not a good idea
realData <- gather(data = data, key = realTypes, value = realNumDistance, mu, sNumPrac, fNumPrac)
#$mu <- as.numeric(realData$mu)
#realData$sNumPrac <- as.numeric(realData$sNumPrac)
realData$realNumDistance <- as.numeric(realData$realNumDistance)

realData <- subset(realData, subjectNumber != "3",subjectNumber != "14")

#realData2 <- subset(realData)

anovaRealResult <- realData %>% anova_test(realNumDistance ~ realTypes + Error(subjectNumber/realTypes))
anovaRealResult

#t-test between mu and sNumPrac
t.test(data$sNumPrac, mu = 1.9444444)
cohen.d(data$sNumPrac, mu = 1.9444444, f=NA)

#t-test between mu and fNumPrac
t.test(data$fNumPrac, mu = 1.9444444)
cohen.d(data$fNumPrac, f = NA, mu = 1.9444444)

#t-test between sNumPrac and fNumPrac
t.test(data$sNumPrac, data$fNumPrac, paired = TRUE)
#cohensD(data$sNumPrac, data$fNumPrac)
cohen.d(data$sNumPrac, data$fNumPrac, paired = TRUE)



realData2 <- gather(data = data, key = realTypes, value = realNumDistance, sNumPrac, fNumPrac)
realData2 <- subset(realData2, subjectNumber != "3", subjectNumber != "14")
realData2$realNumDistance <- as.numeric(realData2$realNumDistance)
realData2 = realData2[,c("subjectNumber","realTypes","realNumDistance")]
#plot
# Create a new data frame with the mean and standard error for each condition
realData2$realTypes <- factor(realData2$realTypes)
means <- aggregate(realNumDistance ~ realTypes + subjectNumber, realData2, mean)
se <- aggregate(realNumDistance ~ realTypes + subjectNumber, realData2, sd) #/ sqrt(length(realData$subjectNumber))
se$realNumDistance <- se$realNumDistance/ sqrt(length(realData2$subjectNumber))
means$se <- se$realNumDistance

# Plot the data
tTestLabel <- c("fast", "slow")
ggplot(means, aes(x = realTypes, y = realNumDistance)) +
  geom_point(size = 0.5) +
  geom_line(aes(group = subjectNumber)) +
  geom_errorbar(aes(ymin = realNumDistance - sd(realNumDistance)/sqrt(length(realNumDistance)), 
                    ymax = realNumDistance + sd(realNumDistance)/sqrt(length(realNumDistance))),
                width = 0.2)+
  geom_hline(yintercept = 1.94444, linetype = "dotted") +
  scale_x_discrete(labels = tTestLabel) + 
  labs(x = "Types", y = "Objective Distance") +
  theme_classic()
























# correlation between subjective distance and objective distance in number conditions
print(data$sNumPrac)
cor(data$sNumDistance, data$sNumPrac)
cor(data$fNumDistance, data$fNumPrac)
