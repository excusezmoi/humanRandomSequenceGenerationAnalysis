import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import configparser
import os
import seaborn as sns
from sklearn.manifold import MDS
from sklearn.cluster import KMeans


def configFilePath(section='FILES', path='subjectiveFile'):
    '''Reads the configuration file "config.ini" to get the file paths'''
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), 'config.ini'), encoding='utf-8') #reads the configuration file
    return config.get(section, path)

#Read the csv file
def readCSVFile():
    df = pd.read_csv(configFilePath())
    return df

#Convert the values in the range iloc[1:,2:] of the dataframe to intger
def convertValuesToFloat(df, currentNumberOfParticipants):
    df.iloc[0:currentNumberOfParticipants*2,2:17] = df.iloc[0:currentNumberOfParticipants*2,2:17].astype(int)/1000
    print(df)
    return df

#Integrate the above two functions
def startToReadCSVAndConvertToFloat(currentNumberOfParticipants):
    df = readCSVFile()
    convertValuesToFloat(df, currentNumberOfParticipants)
    return df

#
def correctDict(df, participantNumber, numOrAct):

    numOrAct = {"a": 1, "n": 0}[numOrAct]
    numberOfRow = (participantNumber - 1) * 2 + numOrAct
    
    if numOrAct:
        actSequenceAll = {
                "as1":{1:"l",2:"q",3:"s",4:"w",5:"r",6:"j"},
                "as2":{1:"w",2:"l",3:"q",4:"r",5:"j",6:"s"},
                "as3":{1:"r",2:"s",3:"l",4:"j",5:"w",6:"q"},
                "as4":{1:"s",2:"w",3:"j",4:"l",5:"q",6:"r"},
                "as5":{1:"q",2:"j",3:"r",4:"s",5:"l",6:"w"},
                "as6":{1:"j",2:"r",3:"w",4:"q",5:"s",6:"l"}
        }
        actSequence = actSequenceAll[f"as{7-(participantNumber % 6) if participantNumber % 6 else 1}"]
        actStandard = {a: n for n, a in actSequenceAll["as1"].items()}

        columnConvert = {f"({i}, {j})": f"({actSequence[i]}, {actSequence[j]})" for i in range(1,7) for j in range(1,7) if i<j}
        # print(columnConvert,"\n")

        df = df.rename(columns = columnConvert)
        # print(df)
        columnConvert2 = {columnConvert[key]: f"({actStandard[columnConvert[key][1]]}, {actStandard[columnConvert[key][4]]})" if actStandard[columnConvert[key][1]]<actStandard[columnConvert[key][4]] else f"({actStandard[columnConvert[key][4]]}, {actStandard[columnConvert[key][1]]})" for key in columnConvert}
        # print(columnConvert2)
        df = df.rename(columns = columnConvert2)
        # print(df)

    goodDict = df.iloc[numberOfRow,2:17].to_dict()
    print(goodDict)
    return df, goodDict

def createMatrix(df, participantNumber, numOrAct):

    numOrAct = {"a": 1, "n": 0}[numOrAct]
    numberOfRow = (participantNumber-1)*2 + numOrAct

    if numOrAct == 1:
        actSequenceAll = {"as1":{1:"l",2:"q",3:"s",4:"w",5:"r",6:"j"},
                "as2":{1:"w",2:"l",3:"q",4:"r",5:"j",6:"s"},
                "as3":{1:"r",2:"s",3:"l",4:"j",5:"w",6:"q"},
                "as4":{1:"s",2:"w",3:"j",4:"l",5:"q",6:"r"},
                "as5":{1:"q",2:"j",3:"r",4:"s",5:"l",6:"w"},
                "as6":{1:"j",2:"r",3:"w",4:"q",5:"s",6:"l"}
        }
        actSequence = actSequenceAll[f"as{7-(participantNumber % 6) if participantNumber % 6 else 1}"]
        actStandard = {a: n for n, a in actSequenceAll["as1"].items()}

        columnConvert = {f"({i}, {j})": f"({actSequence[i]}, {actSequence[j]})" for i in range(1,7) for j in range(1,7) if i<j}
        # print(columnConvert,"\n")

        df = df.rename(columns=columnConvert)
        # print(df)
        columnConvert2 = {columnConvert[key]: f"({actStandard[columnConvert[key][1]]}, {actStandard[columnConvert[key][4]]})" if actStandard[columnConvert[key][1]]<actStandard[columnConvert[key][4]] else f"({actStandard[columnConvert[key][4]]}, {actStandard[columnConvert[key][1]]})" for key in columnConvert}
        # print(columnConvert2)
        df = df.rename(columns=columnConvert2)
        # print(df)

    #Create a 6X6 matrix, fill it with 0
    upperTriangle = np.zeros((6,6))

    for i in range(1,7):
        for j in range(1,7):
            if i<j:
                upperTriangle[i-1,j-1] = df.loc[numberOfRow,f"({i}, {j})"]
    print(upperTriangle)
    return upperTriangle

#Plot the similarity matrix
def plotMatrix(upperTriangle, numOrAct):
    
    """q: how to set the heat map of designated upper and lower limits?
        a: use vmin and vmax

        """
    sns.heatmap(upperTriangle, annot=True, cmap='Blues', vmin = 0, vmax = 1)

    ticksRangex = (i for i in range(1,7)) if numOrAct == "n" else ("L","Q","S","W","R","J") if numOrAct == "a" else None
    ticksRangey = (i for i in range(1,7)) if numOrAct == "n" else ("L","Q","S","W","R","J") if numOrAct == "a" else None

    plt.xticks(np.arange(6)+0.5,ticksRangex,
               rotation=0, fontsize="10")
    plt.yticks(np.arange(6)+0.5,ticksRangey,
               rotation=0, fontsize="10", va="center")
    plt.show()

#Convert the upper triangle matrix to a symmetric matrix
def toSimilarityMatrix(upperTriangle):
    # Extract the upper triangle of A
    upperTri = np.triu(upperTriangle)

    # Create a new matrix with the same values in the lower triangle as in the upper triangle
    similarityMatrix = upperTri + upperTri.T

    # Fill the diagonal of the new matrix with the diagonal values of the original matrix
    np.fill_diagonal(similarityMatrix, 1)
    print(similarityMatrix)
    return similarityMatrix

def startToSimilarMatrix(participantNumber, numOrAct, totalParticipant):
    df = startToReadCSVAndConvertToFloat(totalParticipant) #number of participants
    upperTriangle = createMatrix(df, participantNumber, numOrAct) #df, participantNumber, numOrAct
    plotMatrix(upperTriangle, numOrAct)
    similar = toSimilarityMatrix(upperTriangle)
    return similar

#Convert the similarity matrix to dissimilarity matrix
def similarityToDissimilarity(similarityMatrix):
    dissimilarityMatrix = 1 - similarityMatrix
    return dissimilarityMatrix

#read the random generated response from txt file
def readResponseTxtFile(filePath):
    with open(filePath, 'r') as f:
        lines = f.readline().strip()
        response = list(lines)
    return response, len(response) #response is a list with the form ['2', '1', '3']

# def responseFileReadingDecorator(func):
#     def wrapper(participantNumber, condition, totalParticipant, txtFileFolder):
#         txtFileName = "/p" + str(participantNumber) + f" {condition}.txt"
#         txtFilePath = txtFileFolder + txtFileName

#         txtFile, lengthTXTFile = readResponseTxtFile(txtFilePath)

#         return func(participantNumber, condition, totalParticipant, txtFile, lengthTXTFile)

#     return wrapper

def responseFileReadingDecorator(func):
    def wrapper(**kwargs):

        if "condition" in kwargs:
            participantNumber, condition, totalParticipant, txtFileFolder = kwargs["participantNumber"], kwargs["condition"], kwargs["totalParticipant"], kwargs["txtFileFolder"]

            txtFileName = "/p" + str(participantNumber) + f" {condition}.txt"
            txtFilePath = txtFileFolder + txtFileName

            txtFile, lengthTXTFile = readResponseTxtFile(txtFilePath)

            return func(participantNumber, condition, txtFile, lengthTXTFile)
    
        elif "numOrAct" in kwargs and "slowOrFast" in kwargs:
            participantNumber, numOrAct, slowOrFast, txtFileFolder = kwargs["participantNumber"], kwargs["numOrAct"], kwargs["slowOrFast"], kwargs["txtFileFolder"]
            
            #Read the txt file
            fileName = f'/p{participantNumber} {slowOrFast}{"act" if numOrAct == "a" else "num" if numOrAct == "n" else None}.txt'
            filePath = txtFileFolder + fileName

            txtFile, _length = readResponseTxtFile(filePath)

            return func(txtFile)
    

    return wrapper


