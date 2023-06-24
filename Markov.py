import numpy as np
import csv

from utils import readResponseTxtFile, configFilePath, responseFileReadingdecorator

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

        self.createMarkovDict()
        self.generateMarkovMatrix()
        self.generateMarkovMatrixWithWeighting()
        self.calculateAverageObjectiveDistance()

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

@responseFileReadingdecorator
def createMarkovChain(participant, condition, totalParticipant, txtFile, lengthTXTFile):
    markov = MarkovChain(txtFile, lengthTXTFile, participant, condition)
    return markov

class MarkovChainAll:
    def __init__(self, totalParticipant, txtFileFolder):
        self.totalParticipant = totalParticipant
        self.txtFileFolder = txtFileFolder

        for participant in range(1, self.totalParticipant + 1):
            setattr(self, "p" + str(participant), MarkovChain)
            for condition in ["snum", "fnum"]:
                setattr(getattr(self, "p" + str(participant)), condition, createMarkovChain(participant, condition, self.totalParticipant, self.txtFileFolder))


if __name__ == "__main__":
    
    totalParticipant = 9
    txtFileFolder = configFilePath("FOLDER","responseFileFolder")

    theAnswer = MarkovChainAll(totalParticipant, txtFileFolder)
    # theAnswer.p1 contains the two attributes that are MarkovChain objects for participant 1:
    # theAnswer.p1.snum and theAnswer.p1.fnum

    print(theAnswer.p1)
    print(theAnswer.p1.snum.averageObjectiveDistance)
    print(theAnswer.p3.fnum.averageObjectiveDistance)
    print(theAnswer.p9.snum.MarkovMatrixWithWeighting)