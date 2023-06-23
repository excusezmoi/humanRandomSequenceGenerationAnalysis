import numpy as np
import csv

from utils import readResponseTxtFile, configFilePath

#Create a markov chain based on the sequences
def markovChainExeNew(totalParticipant, txtFileFolder ,conditions = ["snum", "fnum"]):

    # markovAll = []
    objectiveDistance = [[],[]]

    for i in range(1, totalParticipant+1):
        print("i=", i)
        for j in conditions:
            
            txtFileName = "/p" + str(i) + f" {j}.txt"
            txtFilePath = txtFileFolder + txtFileName

            txtFile, lengthTXTFile = readResponseTxtFile(txtFilePath)

            markovDict = {}
            for order, current in enumerate(txtFile):
                if order:
                    markovDict.setdefault((lastOne, current), 0)
                    markovDict[(lastOne, current)] += 1
                lastOne = current

            # Initialize the matrix with zeros
            matrix = np.zeros((6, 6))

            # Fill in the matrix with the dictionary values
            for pair, occurences in markovDict.items():
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
            # markovAll.append(markovDict)
    
            # print(markovDict)

    return objectiveDistance

def writeMarkovToCSV(objectiveDistance, filePath):

    with open(filePath, 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        for thing in objectiveDistance:
            writer.writerow(thing)

    #close the csv file
    csvFile.close()

if __name__ == "__main__":
    
    totalParticipant = 9
    txtFileFolder = configFilePath("FOLDER","responseFileFolder")
    
    objectiveDistance = markovChainExeNew(totalParticipant, txtFileFolder, conditions = ["snum", "fnum"])
    
    # #write to file
    # writeFilePath = "W:/Me/Research/心理/0427報告/originalDistance.csv"
    # writeMarkovToCSV(objectiveDistance, writeFilePath)

