from collections import Counter

from utils import configFilePath, readResponseTxtFile


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

#read file and calculate CfIndex
def CfIndexExe(participantNumber, numOrAct, slowOrFast, totalParticipant, fileFolder):
    
    #Read the txt file
    fileName = f'/p{participantNumber} {slowOrFast}{"act" if numOrAct == "a" else "num" if numOrAct == "n" else None}.txt'
    filePath = fileFolder + fileName

    response, _length = readResponseTxtFile(filePath)

    return CfIndex(response)
    
if __name__ == "__main__":

    participantNumber = 7
    numOrAct = "n"
    slowOrFast = "f"
    totalParticipant = 9
    fileFolder = configFilePath("FOLDER", "responseFileFolder")
    
    print(CfIndexExe(participantNumber, numOrAct, slowOrFast, totalParticipant, fileFolder))