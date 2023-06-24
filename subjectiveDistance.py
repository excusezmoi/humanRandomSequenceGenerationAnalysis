import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from utils import configFilePath, startToReadCSVAndConvertToFloat, readResponseTxtFile, correctDict

#calculate the average distance of true random sequence and the generated sequence 

def randomSubjectiveDistance(df, goodDict):
    #random distance: the average distance of the truly random responses according 
    # to their subjective similarity ratings
    responseDict = goodDict
    randomDistanceS = (sum(responseDict.values()) + 3) / 18
    randomDistance = 1 - randomDistanceS
    return randomDistance

def actualSequenceSubjectiveDistance(df, response, length, goodDict):
    #average distance: the actual average distance of the generated random sequences
    responseDict = goodDict
    distanceSumS = 0
    for i, element in enumerate(response):
        if i:
            distanceSumS += responseDict[f"({element}, {last})"] if element<last else responseDict[f"({last}, {element})"] if element>last else 1
        last = element
    
    averageDistanceS = distanceSumS / (length - 1)
    averageDistance = 1 - averageDistanceS
    return averageDistance

def printSubjectiveDistanceExe(participantNumber, numOrAct, slowOrFast, totalParticipant, fileFolder):
    #Read the txt file

    fileName = f'/p{participantNumber} {slowOrFast}{"act" if numOrAct == "a" else "num" if numOrAct == "n" else None}.txt'
    filePath = fileFolder + fileName

    response, length = readResponseTxtFile(filePath)
    print(response, length)
    df = startToReadCSVAndConvertToFloat(totalParticipant)
    df, dictGood = correctDict(df, participantNumber, numOrAct)
    randomDistance = randomSubjectiveDistance(df, dictGood)
    averageDistance = actualSequenceSubjectiveDistance(df, response, length, dictGood)
    print("the average subjective distance if the sequence is random:", randomDistance, 
          "\nthe average actual distance from their random sequence:", averageDistance)

if __name__ == "__main__":

    participantNumber = 7
    numOrAct = "a"
    slowOrFast = "s"
    totalParticipant = 9
    fileFolder = configFilePath("FOLDER", "responseFileFolder")

    printSubjectiveDistanceExe(participantNumber, numOrAct, slowOrFast, totalParticipant, fileFolder)