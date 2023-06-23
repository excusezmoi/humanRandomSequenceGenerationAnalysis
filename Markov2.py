import numpy as np
import csv

from utils import readResponseTxtFile, configFilePath

class MarkovChain:
    def __init__(self, txtFile, lengthTXTFile, participant, condition):
        self.txtFile = txtFile
        self.lengthTXTFile = lengthTXTFile
        self.participant = participant
        self.condition = condition
        self.MarkovDict = None
        self.MarkovMatrix = None
        self.MarkovMatrixWithWeighting = None
        self.averageObjectiveDistance = None

    def createMarkovDict(self):
        MarkovDict = {}
        for order, current in enumerate(self.txtFile):
            if order:
                MarkovDict.setdefault((lastOne, current), 0)
                MarkovDict[(lastOne, current)] += 1
            lastOne = current
        self.MarkovDict = MarkovDict

    def generateMarkovMatrix(self):
        self.MarkovMatrix = np.zeros((6, 6))
        for pair, occurrences in self.MarkovDict.items():
            I = int(pair[0]) - 1
            J = int(pair[1]) - 1
            self.MarkovMatrix[I, J] = occurrences

    def generateMarkovMatrixWithWeighting(self):
        objectiveWeighting = np.array([[i for i in range(6)], [1, 0, 1, 2, 3, 4], [2, 1, 0, 1, 2, 3], [3, 2, 1, 0, 1, 2], [4, 3, 2, 1, 0, 1], [5, 4, 3, 2, 1, 0]])
        self.MarkovMatrixWithWeighting = self.MarkovMatrix * objectiveWeighting

    def calculateAverageObjectiveDistance(self):
        self.averageObjectiveDistance = np.sum(self.MarkovMatrixWithWeighting) / (self.lengthTXTFile - 1)

def MarkovChainExe(participant, condition, totalParticipant, txtFileFolder):

    txtFileName = "/p" + str(participant) + f" {condition}.txt"
    txtFilePath = txtFileFolder + txtFileName

    txtFile, lengthTXTFile = readResponseTxtFile(txtFilePath)

    markov = MarkovChain(txtFile, lengthTXTFile, participant, condition)
    markov.createMarkovDict()
    markov.generateMarkovMatrix()
    markov.generateMarkovMatrixWithWeighting()
    markov.calculateAverageObjectiveDistance()

    return markov

def MarkovChainExeAll(totalParticipant, txtFileFolder):

    markovList = []
    for participant in range(1, totalParticipant + 1):
        for condition in ["snum", "fnum"]:
            markovList.append(MarkovChainExe(participant, condition, totalParticipant, txtFileFolder))

    return markovList

class MarkovChainAll:
    def __init__(self, totalParticipant, txtFileFolder):
        self.totalParticipant = totalParticipant
        self.txtFileFolder = txtFileFolder

    def structuring(self):
        for participant in range(1, totalParticipant + 1):
            setattr(self, "p" + str(participant), [])
            for condition in ["snum", "fnum"]:
                getattr(self, "p" + str(participant)).append(MarkovChainExe(participant, condition, totalParticipant, txtFileFolder))


if __name__ == "__main__":
    
    totalParticipant = 9
    txtFileFolder = configFilePath("FOLDER","responseFileFolder")

    theAnswer = MarkovChainAll(totalParticipant, txtFileFolder)
    theAnswer.structuring()
    print(theAnswer.p1[0].averageObjectiveDistance)
    # theAnswer.p1 contains the two MarkovChain object for participant 1:
    # the slow condition if the first one, the fast condition is the second one
    # The attributes of the individual MarkovChain object can then be accessed

