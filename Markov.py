import numpy as np
import csv

from utils import readResponseTxtFile, configFilePath

#Create a Markov chain based on the sequences
def MarkovChainExeNew(totalParticipant, txtFileFolder ,conditions = ["snum", "fnum"]):

    # MarkovAll = []
    objectiveDistance = [[],[]]

    for i in range(1, totalParticipant+1):
        print("i=", i)
        for j in conditions:
            
            txtFileName = "/p" + str(i) + f" {j}.txt"
            txtFilePath = txtFileFolder + txtFileName

            txtFile, lengthTXTFile = readResponseTxtFile(txtFilePath)

            MarkovDict = {}
            for order, current in enumerate(txtFile):
                if order:
                    MarkovDict.setdefault((lastOne, current), 0)
                    MarkovDict[(lastOne, current)] += 1
                lastOne = current

            # Initialize the matrix with zeros
            matrix = np.zeros((6, 6))

            # Fill in the matrix with the dictionary values
            for pair, occurences in MarkovDict.items():
                I = int(pair[0]) - 1
                J = int(pair[1]) - 1
                matrix[I, J] = occurences

            # Print the resulting matrix
            print("Markov:\n",matrix)
            objectiveWeighting = np.array([[i for i in range(6)],[1,0,1,2,3,4],[2,1,0,1,2,3],[3,2,1,0,1,2],[4,3,2,1,0,1],[5,4,3,2,1,0]])
            sumMatrix = matrix*objectiveWeighting #turn it into the concept of distance, e.g. the same number equals zero distance
            print("Weighted:\n",sumMatrix)
            print(f"p{i},{j} sum:", np.sum(sumMatrix)/(lengthTXTFile-1)) #this is the average objective distance between each responses

            if j == "snum":
                objectiveDistance[0].append(np.sum(sumMatrix)/(lengthTXTFile-1))
            else:
                objectiveDistance[1].append(np.sum(sumMatrix)/(lengthTXTFile-1))
            # MarkovAll.append(MarkovDict)
    
            # print(MarkovDict)

    return objectiveDistance

def writeMarkovToCSV(objectiveDistance, filePath):

    with open(filePath, 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        for thing in objectiveDistance:
            writer.writerow(thing)

    #close the csv file
    csvFile.close()
###################
def MarkovChainDecorator(func):
    def wrapper(totalParticipant, txtFileFolder, conditions=["snum", "fnum"]):
        objectiveDistance = [[], []]

        for i in range(1, totalParticipant + 1):
            print("i=", i)
            for j in conditions:
                txtFileName = "/p" + str(i) + f" {j}.txt"
                txtFilePath = txtFileFolder + txtFileName

                txtFile, lengthTXTFile = readResponseTxtFile(txtFilePath)

                # Call the main function
                result = func(txtFile, lengthTXTFile, i, j)
                
                if j == "snum":
                    objectiveDistance[0].append(result)
                else:
                    objectiveDistance[1].append(result)

        return objectiveDistance

    return wrapper

@MarkovChainDecorator
def MarkovChain(txtFile, lengthTXTFile, participant, condition):

    # Create a dictionary of the Markov chain, which has the structure {(lastOne, current): occurrences}
    def createMarkovDict(txtFile):
        MarkovDict = {}
        for order, current in enumerate(txtFile):
            if order:
                MarkovDict.setdefault((lastOne, current), 0)
                MarkovDict[(lastOne, current)] += 1
            lastOne = current
        return MarkovDict

    def MarkovMatrix(MarkovDict):
        # Initialize the matrix with zeros
        matrix = np.zeros((6, 6))

        # Fill in the matrix with the dictionary values
        for pair, occurrences in MarkovDict.items():
            I = int(pair[0]) - 1
            J = int(pair[1]) - 1
            matrix[I, J] = occurrences

        return matrix

    def MarkovMatrixWithWeighting(MarkovMatrix):
        objectiveWeighting = np.array([[i for i in range(6)], [1, 0, 1, 2, 3, 4], [2, 1, 0, 1, 2, 3], [3, 2, 1, 0, 1, 2], [4, 3, 2, 1, 0, 1], [5, 4, 3, 2, 1, 0]])
        sumMatrix = MarkovMatrix * objectiveWeighting
        return sumMatrix
    
    def averageObjectiveDistance(sumMatrix):
        AOD = np.sum(sumMatrix) / (lengthTXTFile - 1)
        return AOD

    MarkovDict = createMarkovDict(txtFile)
    MarkovMatrix = MarkovMatrix(MarkovDict)
    MarkovMatrixWithWeighting = MarkovMatrixWithWeighting(MarkovMatrix) 
    averageObjectiveDistance = averageObjectiveDistance(MarkovMatrixWithWeighting)
    
    return averageObjectiveDistance


###################
if __name__ == "__main__":
    
    totalParticipant = 9
    txtFileFolder = configFilePath("FOLDER","responseFileFolder")
    
    objectiveDistance = MarkovChainExeNew(totalParticipant, txtFileFolder, conditions = ["snum", "fnum"])
    
    # #write to file
    # writeFilePath = "W:/Me/Research/心理/0427報告/originalDistance.csv"
    # writeMarkovToCSV(objectiveDistance, writeFilePath)

    objectiveDistance2 = MarkovChain(totalParticipant, txtFileFolder, conditions = ["snum", "fnum"])
    print(objectiveDistance2)
