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

    def sumOccurences(countdict, le):
        return sum(countdict.values()) / le
    
    return sumOccurences(countInstances(intervalCalc(elementPlacing(li))),len(li))

if __name__ == "__main__":

    participantNumber = 4
    numOrAct = "n"
    slowOrFast = "f"
    totalParticipant = 9
    txtFileFolder = configFilePath("FOLDER", "responseFileFolder")
    
    # print(CfIndexExe(participantNumber, numOrAct, slowOrFast, totalParticipant, txtFileFolder))
    print(CfIndex(participantNumber = participantNumber, 
                        numOrAct = numOrAct, 
                        slowOrFast = slowOrFast, 
                        totalParticipant = totalParticipant, 
                        txtFileFolder = txtFileFolder))