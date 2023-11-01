import numpy as np
import csv

from utils import configFilePath, responseFileReadingDecorator

class MarkovChain:
    def __init__(self, txtFile):
        self.txtFile = txtFile
        self.lengthTXTFile = len(txtFile)
        self.MarkovDict = self.createMarkovDict()
        self.MarkovMatrix = self.generateMarkovMatrix()

        #the following two are only applicable to number conditions
        self.MarkovMatrixWithWeighting = self.generateMarkovMatrixWithWeighting()
        self.averageObjectiveDistance = self.calculateAverageObjectiveDistance()

    def createMarkovDict(self):
        MarkovDict = {}
        for order, current in enumerate(self.txtFile):
            if order:
                MarkovDict[(lastOne, current)] = MarkovDict.get((lastOne, current), 0) + 1
            lastOne = current
        return MarkovDict

    def generateMarkovMatrix(self):
        MarkovMatrix = np.zeros((6, 6))
        for pair, occurrences in self.MarkovDict.items():
            I = int(pair[0]) - 1
            J = int(pair[1]) - 1
            MarkovMatrix[I, J] = occurrences
        return MarkovMatrix

    def generateMarkovMatrixWithWeighting(self):
        objectiveWeighting = np.array([[i for i in range(6)], [1, 0, 1, 2, 3, 4], [2, 1, 0, 1, 2, 3], [3, 2, 1, 0, 1, 2], [4, 3, 2, 1, 0, 1], [5, 4, 3, 2, 1, 0]])
        MarkovMatrixWithWeighting = self.MarkovMatrix * objectiveWeighting
        return MarkovMatrixWithWeighting

    def calculateAverageObjectiveDistance(self):
        averageObjectiveDistance = np.sum(self.MarkovMatrixWithWeighting) / (self.lengthTXTFile - 1)
        return averageObjectiveDistance

@responseFileReadingDecorator
def createMarkovChain(txtFile):
    return MarkovChain(txtFile)

class Participant:
    pass

class MarkovChainAll:
    def __init__(self, totalParticipant, txtFileFolder):
        self.totalParticipant = totalParticipant
        self.txtFileFolder = txtFileFolder

        for participant in range(1, self.totalParticipant + 1):
            # print(participant)
            setattr(self, "p" + str(participant), Participant()) #set the attribute of the class MarkovChainAll to be MarkovChain, with the name being p1, p2, p3, etc.
            for condition in ["snum", "fnum", "sact", "fact"]:

                setattr(getattr(self, "p" + str(participant)), 
                        str(condition), 
                        createMarkovChain(participantNumber = participant, 
                                          condition = condition,  
                                          txtFileFolder = self.txtFileFolder))
                # print(getattr(getattr(getattr(self, "p" + str(participant)), str(condition)),"txtFile"))


if __name__ == "__main__":
    
    totalParticipant = 24
    txtFileFolder = configFilePath("FOLDER","responseFileFolder")

    theAnswer = MarkovChainAll(totalParticipant, txtFileFolder)
    # theAnswer.p1 contains two attributes that are MarkovChain objects for participant 1:
    # theAnswer.p1.snum and theAnswer.p1.fnum

    print(1, theAnswer.p17.snum.MarkovMatrix)
    print(1, theAnswer.p7.fnum.averageObjectiveDistance)

    # print(theAnswer.p1.snum.txtFile == theAnswer.p2.snum.txtFile)
    # print(theAnswer.p1 == theAnswer.p2)


    # print(theAnswer.p17.snum.averageObjectiveDistance)
    # print(theAnswer.p20.fnum.averageObjectiveDistance)
    # print(theAnswer.p20.snum.MarkovMatrixWithWeighting)

    # participant = 17
    # condition = "snum"
    # pp17 = createMarkovChain(participantNumber = participant, 
    #                                       condition = condition,  
    #                                       txtFileFolder = txtFileFolder)
    # print(pp17.txtFile)



    # a = MarkovChain
    # print(a.txtFile)