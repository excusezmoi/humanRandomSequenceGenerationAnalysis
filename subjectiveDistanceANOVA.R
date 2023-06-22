library("rstatix")
library(ggplot2)
#library(compute.es)
library(lsr)
library(effsize)
data = openxlsx::read.xlsx("W:/Me/Research/心理/初步資料.xlsx")
data = data[1:9,]

#踢人
data <- subset(data, subjectNumber != "3")


sdData <- gather(data = data, key = types, value = distance, expectedAverageNumDistance,	sNumDistance,	fNumDistance,	expectedAverageActDistance,	sActDistance,	fActDistance)
sdData
class(sdData$distance)
sdData$distance = as.numeric(sdData$distance)
class(sdData$distance)


# One-way repeated measures ANOVA all
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


#plot
# Create a new data frame with the mean and standard error for each condition
sdDataNum$types <- factor(sdDataNum$types)
means <- aggregate(distance ~ types + subjectNumber, sdDataNum, mean)
se <- aggregate(distance ~ types + subjectNumber, sdDataNum, sd) #/ sqrt(length(sdDataNum$subjectNumber))
se$distance <- se$distance/ sqrt(length(sdDataNum$subjectNumber))
means$se <- se$distance

# Plot the data

ggplot(means, aes(x = types, y = distance)) +
  geom_point(size = 0.5) +
  geom_line(aes(group = subjectNumber)) +
  geom_errorbar(aes(ymin = distance - sd(distance)/sqrt(length(distance)), 
                    ymax = distance + sd(distance)/sqrt(length(distance))),
                width = 0.2)+
    
  labs(x = "Types", y = "Distance") +
  theme_classic()

# Perform one-way repeated measures ANOVA on the data
anova_result_num <- sdDataNum %>% anova_test(distance ~ types + Error(subjectNumber/types))

# Perform pairwise t-tests and adjust for multiple comparisons using the Holm method
posthoc_results <- sdDataNum %>% 
  pairwise_t_test(distance ~ types, 
                  paired = TRUE,
                  p.adjust.method = "holm")

# View the pairwise comparison results
posthoc_results







#One-way in act: not significant
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
ggplot(means, aes(x = types, y = distance)) +
  geom_point(size = 0.5) +
  geom_line(aes(group = subjectNumber)) +
  geom_errorbar(aes(ymin = distance - sd(distance)/sqrt(length(distance)), 
                    ymax = distance + sd(distance)/sqrt(length(distance))),
                width = 0.2)+
  
  labs(x = "Types", y = "Distance") +
  theme_classic()



#realdata: not a good idea
realData <- gather(data = data, key = realTypes, value = realDistance, mu, sNumPrac, fNumPrac)
#$mu <- as.numeric(realData$mu)
#realData$sNumPrac <- as.numeric(realData$sNumPrac)
realData$realDistance <- as.numeric(realData$realDistance)

realData <- subset(realData, subjectNumber != "3")

#realData2 <- subset(realData)

anovaRealResult <- realData %>% anova_test(realDistance ~ realTypes + Error(subjectNumber/realTypes))
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



realData2 <- gather(data = data, key = realTypes, value = realDistance, sNumPrac, fNumPrac)
realData2 <- subset(realData2, subjectNumber != "3")
realData2$realDistance <- as.numeric(realData2$realDistance)
realData2 = realData2[,c("subjectNumber","realTypes","realDistance")]
#plot
# Create a new data frame with the mean and standard error for each condition
realData2$realTypes <- factor(realData2$realTypes)
means <- aggregate(realDistance ~ realTypes + subjectNumber, realData2, mean)
se <- aggregate(realDistance ~ realTypes + subjectNumber, realData2, sd) #/ sqrt(length(realData$subjectNumber))
se$realDistance <- se$realDistance/ sqrt(length(realData2$subjectNumber))
means$se <- se$realDistance

# Plot the data
ggplot(means, aes(x = realTypes, y = realDistance)) +
  geom_point(size = 0.5) +
  geom_line(aes(group = subjectNumber)) +
  geom_errorbar(aes(ymin = realDistance - sd(realDistance)/sqrt(length(realDistance)), 
                    ymax = realDistance + sd(realDistance)/sqrt(length(realDistance))),
                width = 0.2)+
  geom_hline(yintercept = 1.94444, linetype = "dotted") +
  
  labs(x = "realTypes", y = "realDistance") +
  theme_classic()


