import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from utils import configFilePath, startToReadCSVAndConvertToFloat, readResponseTxtFile, correctDict
from utils import configFilePath, startToReadCSVAndConvertToFloat2, readResponseTxtFile, correctDict2
from Markov import MarkovChainAll
from actionSequence import googleMatrix

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
    # print(response, length)
    df = startToReadCSVAndConvertToFloat2(totalParticipant, numOrAct)
    df, dictGood = correctDict2(df, participantNumber)
    randomDistance = randomSubjectiveDistance(df, dictGood)
    averageDistance = actualSequenceSubjectiveDistance(df, response, length, dictGood, numOrAct)
    print("the average subjective distance if the sequence is random:", randomDistance, 
          "\nthe average actual distance from their random sequence:", averageDistance)

def subjectiveDistanceDict(participantNumber, totalParticipant, fileFolder):
    #Read the txt file

    distanceDict = {}
    distanceDict["subjectNumber"] = participantNumber

    for numOrAct in ["n", "a"]:
        cond = f"{'Num' if numOrAct == 'n' else 'Act'}"
        for slowOrFast in ["s", "f"]:
            fileName = f'/p{participantNumber} {slowOrFast}{"act" if numOrAct == "a" else "num" if numOrAct == "n" else None}.txt'
            filePath = fileFolder + fileName

            response, length = readResponseTxtFile(filePath)
            df = startToReadCSVAndConvertToFloat2(totalParticipant, numOrAct)
            df, dictGood = correctDict2(df, participantNumber)
            randomDistance = randomSubjectiveDistance(df, dictGood)
            averageDistance = actualSequenceSubjectiveDistance(df, response, length, dictGood, numOrAct)

            distanceDict[f"{slowOrFast}{cond}Distance"] = averageDistance

        
        distanceDict[f"expectedAverage{cond}Distance"] = randomDistance
    
      
    return distanceDict

def allDistanceDict(participantNumber, totalParticipant, fileFolder):
    theAnswer = MarkovChainAll(totalParticipant, fileFolder)
    allDistanceDict = subjectiveDistanceDict(participantNumber, totalParticipant, fileFolder)
    allDistanceDict["sNumPrac"] = getattr(getattr(theAnswer, "p" + str(participantNumber)), "snum").averageObjectiveDistance
    allDistanceDict["fNumPrac"] = getattr(getattr(theAnswer, "p" + str(participantNumber)), "fnum").averageObjectiveDistance
    allDistanceDict["realNumDistance"] = (allDistanceDict["sNumPrac"] + allDistanceDict["fNumPrac"]) / 2

    allDistanceDict["sActPrac"] = np.multiply(getattr(getattr(theAnswer, "p" + str(participantNumber)), "sact").MarkovMatrix, googleMatrix()).sum()
    allDistanceDict["fActPrac"] = np.multiply(getattr(getattr(theAnswer, "p" + str(participantNumber)), "fact").MarkovMatrix, googleMatrix()).sum()
    return allDistanceDict

def dictToXLSX(dic, file):
    # add the dictionary as an additional row to an existing xlsx file with keys being existing column names
    # and values being the values of the new row without using pandas

    # Load the existing Excel file
    existing_file_path = file
    df_existing = pd.read_excel(existing_file_path)
    # print(df_existing,"\n\n\n")

    # Your new dictionary
    new_dict = dic

    # Convert the dictionary to a DataFrame
    df_new = pd.DataFrame([new_dict])

    # Append the new DataFrame to the existing DataFrame
    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    # print(df_combined)

    # Save the combined DataFrame back to the Excel file
    df_combined.to_excel(existing_file_path, index=False)


if __name__ == "__main__":

    participantNumber = 1
    numOrAct = "a"
    slowOrFast = "s"
    totalParticipant = 24
    fileFolder = configFilePath("FOLDER", "responseFileFolder")
    outputFile = configFilePath("FILES", "distanceDataXLSXFile")

    # printSubjectiveDistanceExe(participantNumber, numOrAct, slowOrFast, totalParticipant, fileFolder)
    # print(subjectiveDistanceDict(participantNumber, totalParticipant, fileFolder))

    # Dici = allDistanceDict(participantNumber, totalParticipant, fileFolder)
    # print(Dici)

    
    for participantNumber in range(1, totalParticipant+1):
        Dici = allDistanceDict(participantNumber, totalParticipant, fileFolder)
        dictToXLSX(Dici, outputFile)
    print("done")