import numpy as np
from functools import reduce

from utils import configFilePath, responseFileReadingDecorator

class MarkovChain:
    def __init__(self, txtFile):
        self.txtFile = txtFile
        self.lengthTXTFile = len(txtFile)
        self.initInterval(self.txtFile, self.lengthTXTFile)

    def initInterval(self, txtFile, lengthTXTFile):
        for inter in range(lengthTXTFile-1):
            setattr(self, "i" + str(inter), Interval(txtFile, interval=inter))

class Interval:
    def __init__(self, txtFile, interval):
        self.txtFile = txtFile
        self.lengthTXTFile = len(txtFile)
        self.MarkovDict = self.createMarkovDict(self.txtFile,interval)
        self.MarkovMatrix = self.generateMarkovMatrix(self.MarkovDict)
        self.MarkovMatrixWithWeighting = self.generateMarkovMatrixWithWeighting(self.MarkovMatrix)
        self.averageObjectiveDistance = self.calculateAverageObjectiveDistance(self.MarkovMatrixWithWeighting)

    def createMarkovDict(self,txtFile, interval=0):

        def updateMarkovDict(accumulator, current, idx, interval):
            if idx > interval:
                lastOne = self.txtFile[idx - (interval + 1)]
                accumulator[(lastOne, current)] = accumulator.get((lastOne, current), 0) + 1
            return accumulator

        # Using reduce to build the Markov dictionary
        MarkovDict = reduce(lambda acc, val: updateMarkovDict(acc, val[1], val[0], interval), enumerate(txtFile), {})
        return MarkovDict

    def generateMarkovMatrix(self, MarkovDict):
        MarkovMatrix = np.zeros((6, 6))
        for pair, occurrences in MarkovDict.items():
            I = int(pair[0]) - 1
            J = int(pair[1]) - 1
            MarkovMatrix[I, J] = occurrences
        return MarkovMatrix

    def generateMarkovMatrixWithWeighting(self, MarkovMatrix):
        objectiveWeighting = np.array([[i for i in range(6)], 
                                       [1, 0, 1, 2, 3, 4], 
                                       [2, 1, 0, 1, 2, 3], 
                                       [3, 2, 1, 0, 1, 2], 
                                       [4, 3, 2, 1, 0, 1],
                                       [5, 4, 3, 2, 1, 0]])
        MarkovMatrixWithWeighting = MarkovMatrix * objectiveWeighting
        return MarkovMatrixWithWeighting

    def calculateAverageObjectiveDistance(self, MarkovMatrixWithWeighting):
        averageObjectiveDistance = np.sum(MarkovMatrixWithWeighting) / (self.lengthTXTFile - 1)
        return averageObjectiveDistance

@responseFileReadingDecorator
def createMarkovChain(txtFile):
    return MarkovChain(txtFile)

class MarkovChainAll:
    def __init__(self, totalParticipant, txtFileFolder):
        self.totalParticipant = totalParticipant
        self.txtFileFolder = txtFileFolder

        class Participant:
            pass

        for participant in range(1, self.totalParticipant + 1):
            # print(participant)
            setattr(self, "p" + str(participant), Participant())
            for condition in ["snum", "fnum", "sact", "fact"]:
                setattr(getattr(self, "p" + str(participant)), 
                        str(condition), 
                        createMarkovChain(participantNumber = participant, 
                                          condition = condition,  
                                          txtFileFolder = self.txtFileFolder))
                # print(getattr(getattr(getattr(self, "p" + str(participant)), str(condition)),"txtFile"))


if __name__ == "__main__":
    
    totalParticipant = 1
    txtFileFolder = configFilePath("FOLDER","responseFileFolder")

    theAnswer = MarkovChainAll(totalParticipant, txtFileFolder)
    # theAnswer.p1 contains two attributes that are MarkovChain objects for participant 1:
    # theAnswer.p1.snum and theAnswer.p1.fnum

    # print(1, theAnswer.p17.snum.MarkovMatrix)
    # print(1, theAnswer.p7.fnum.averageObjectiveDistance)

    # print(1, theAnswer.p1.snum.averageObjectiveDistance)
    # theAnswer.p1.snum.initInterval(theAnswer.p1.snum.txtFile, theAnswer.p1.snum.lengthTXTFile)
    print(1, theAnswer.p1.snum.i0.averageObjectiveDistance)
    print(1, theAnswer.p1.snum.i87.averageObjectiveDistance)