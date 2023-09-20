import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from utils import configFilePath, startToReadCSVAndConvertToFloat, readResponseTxtFile, correctDict
from utils import configFilePath, startToReadCSVAndConvertToFloat2, readResponseTxtFile, correctDict2
#calculate the average distance of true random sequence and the generated sequence 

def randomSubjectiveDistance(df, goodDict):
    #random distance: the average distance of the truly random responses according 
    # to their subjective similarity ratings
    responseDict = goodDict
    randomDistanceS = (sum(responseDict.values()) + 3) / 18
    randomDistance = 1 - randomDistanceS
    return randomDistance

def actualSequenceSubjectiveDistance(df, response, length, goodDict, numOrAct):
    #average distance: the actual average distance of the generated random sequences
    responseDict = goodDict

    distanceSumS = 0

    as1 = {"1":"l","2":"q","3":"s","4":"w","5":"r","6":"j"} if numOrAct == "a" else {f"{i}":f"{i}" for i in range(1,7)} if numOrAct == "n" else None
    for i, element in enumerate(response):
        elementReal = as1[element]
        if i:
            distanceSumS += responseDict[f"({elementReal}, {lastReal})"] if element<last else responseDict[f"({lastReal}, {elementReal})"] if element>last else 1
        last = element
        lastReal = elementReal
    
    averageDistanceS = distanceSumS / (length - 1)
    averageDistance = 1 - averageDistanceS
    return averageDistance

def printSubjectiveDistanceExe(participantNumber, numOrAct, slowOrFast, totalParticipant, fileFolder):
    #Read the txt file

    fileName = f'/p{participantNumber} {slowOrFast}{"act" if numOrAct == "a" else "num" if numOrAct == "n" else None}.txt'
    filePath = fileFolder + fileName

    response, length = readResponseTxtFile(filePath)
    print(response, length)
    df = startToReadCSVAndConvertToFloat2(totalParticipant, numOrAct)
    df, dictGood = correctDict2(df, participantNumber)
    randomDistance = randomSubjectiveDistance(df, dictGood)
    averageDistance = actualSequenceSubjectiveDistance(df, response, length, dictGood, numOrAct)
    print("the average subjective distance if the sequence is random:", randomDistance, 
          "\nthe average actual distance from their random sequence:", averageDistance)

if __name__ == "__main__":

    participantNumber = 17
    numOrAct = "n"
    slowOrFast = "s"
    totalParticipant = 24
    fileFolder = configFilePath("FOLDER", "responseFileFolder")

    printSubjectiveDistanceExe(participantNumber, numOrAct, slowOrFast, totalParticipant, fileFolder)