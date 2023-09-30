from collections import Counter

from utils import configFilePath, responseFileReadingDecorator

@responseFileReadingDecorator
def CfIndex(li):
    def elementPlacing(li):
        dic = {}
        for order, element in enumerate(li):
            dic.setdefault(element, []).append(order)
        return dic

    def intervalCalc(dic):
        interval = [i - j for alternative in dic for i in dic[alternative] for j in dic[alternative] if i > j]
        return interval

    def countInstances(lis):
        return Counter(lis)

    def sumOccurencesAndDevideByLength(countdict, le):
        return sum(countdict.values()) / le
    
    def divideByMaxCfIndex(sumOccurencesAndDevideByLength, le):
        return sumOccurencesAndDevideByLength / ((le - 1)/2)
    
    # return sumOccurencesAndDevideByLength(countInstances(intervalCalc(elementPlacing(li))),len(li))
    return divideByMaxCfIndex(sumOccurencesAndDevideByLength(countInstances(intervalCalc(elementPlacing(li))),len(li)),len(li))

if __name__ == "__main__":

    participantNumber = 20
    numOrAct = "a"
    slowOrFast = "s"
    totalParticipant = 24
    txtFileFolder = configFilePath("FOLDER", "responseFileFolder")
    
    # print(CfIndex(participantNumber = participantNumber, 
    #                     numOrAct = numOrAct, 
    #                     slowOrFast = slowOrFast, 
    #                     totalParticipant = totalParticipant, 
    #                     txtFileFolder = txtFileFolder))
    
    for participantNumber in range(1, 1 + totalParticipant):
        print(CfIndex(participantNumber = participantNumber, 
                        numOrAct = numOrAct, 
                        slowOrFast = slowOrFast, 
                        totalParticipant = totalParticipant, 
                        txtFileFolder = txtFileFolder))
    # li = [1,4,2,1,0,5,1,2,7,6]
    # print(CfIndex(li))