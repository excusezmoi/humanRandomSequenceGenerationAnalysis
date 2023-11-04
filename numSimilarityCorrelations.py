import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from convenient import getNestedAttr
from utils import startToSimilarMatrix, matrixCorr, configFilePath
from MarkovAdvanced import MarkovChainAll

def objectiveDistanceMatrix():
    fullMatrix = np.array([[5 for i in range(6)] for j in range(6)])
    # print(fullMatrix)
    objDisMatrix = fullMatrix - np.array([[i for i in range(6)], [1, 0, 1, 2, 3, 4], [2, 1, 0, 1, 2, 3], [3, 2, 1, 0, 1, 2], [4, 3, 2, 1, 0, 1], [5, 4, 3, 2, 1, 0]])
    # print(objDisMatrix)
    return objDisMatrix

def objectiveMatrixList(totalParticipant, dropOut):
    return [objectiveDistanceMatrix() for _ in range(totalParticipant - len(dropOut))]

def subjectiveList(numOrAct, totalParticipant, dropOut):
    return [startToSimilarMatrix(participant, numOrAct, totalParticipant) for participant in range(1, totalParticipant + 1) if participant not in dropOut]

def sequenceList(theAnswer,slowOrFast, numOrAct, totalParticipant, dropOut, interval = 0):
    return [getNestedAttr(theAnswer, f"p{participant}.{slowOrFast}{'num' if numOrAct == 'n' else 'act' if numOrAct == 'a' else None}.i{interval}.MarkovMatrix") for participant in range(1, totalParticipant + 1) if participant not in dropOut]

def matrixCorrList(list1, list2):
    return [matrixCorr(i, j)[0] for i, j in zip(list1, list2)] #return a list of correlation coefficients

def drawCorr(list1, list2, label):
    plt.hist(matrixCorrList(list1, list2), bins = 10, ec = "black", alpha = 0.5, label = label)

def plotCorr(title = ''):
    plt.legend(loc='upper right')
    plt.title(title)
    plt.show()

def subSequenceCorrPlot(numOrAct, totalParticipant, dropOut, interval = 0):
    theAnswer = MarkovChainAll(totalParticipant, configFilePath("FOLDER","responseFileFolder"))
    drawCorr(subjectiveList(numOrAct, totalParticipant, dropOut), sequenceList(theAnswer, "s", numOrAct, totalParticipant, dropOut, interval), "slow")
    drawCorr(subjectiveList(numOrAct, totalParticipant, dropOut), sequenceList(theAnswer, "f", numOrAct, totalParticipant, dropOut, interval), "fast")
    plotCorr('Subjective and Markov Matrix Correlation Distribution')

def objSequenceCorrPlot(numOrAct, totalParticipant, dropOut, interval = 0):
    theAnswer = MarkovChainAll(totalParticipant, configFilePath("FOLDER","responseFileFolder"))
    drawCorr(objectiveMatrixList(totalParticipant, dropOut), sequenceList(theAnswer, "s", numOrAct, totalParticipant, dropOut, interval), "slow")
    drawCorr(objectiveMatrixList(totalParticipant, dropOut), sequenceList(theAnswer, "f", numOrAct, totalParticipant, dropOut, interval), "fast")
    plotCorr('Objective and Markov Matrix Correlation Distribution')

def subObjCorrPlot(numOrAct, totalParticipant, dropOut, interval = 0):
    drawCorr(subjectiveList(numOrAct, totalParticipant, dropOut), objectiveMatrixList(totalParticipant, dropOut), None)
    plotCorr('Subjective and Objective Similarity Matrix Correlation Distribution') 

def sfSeparationRate(numOrAct, totalParticipant, dropOut, interval = 0):
    theAnswer = MarkovChainAll(totalParticipant, configFilePath("FOLDER","responseFileFolder"))
    sSubSeq = matrixCorrList(subjectiveList(numOrAct, totalParticipant, dropOut), sequenceList(theAnswer, "s", numOrAct, totalParticipant, dropOut, interval))
    fSubSeq = matrixCorrList(subjectiveList(numOrAct, totalParticipant, dropOut), sequenceList(theAnswer, "f", numOrAct, totalParticipant, dropOut, interval))
    
    subSeqRate = sum(i < j for i, j in zip(sSubSeq, fSubSeq)) / len(sSubSeq)
    # print("Subjective Sequence Separation Rate: ", subSeqRate)

    sObjSeq = matrixCorrList(objectiveMatrixList(totalParticipant, dropOut), sequenceList(theAnswer, "s", numOrAct, totalParticipant, dropOut, interval))
    fObjSeq = matrixCorrList(objectiveMatrixList(totalParticipant, dropOut), sequenceList(theAnswer, "f", numOrAct, totalParticipant, dropOut, interval))

    objSeqRate = sum(i < j for i, j in zip(sObjSeq, fObjSeq)) / len(sObjSeq)
    # print("Objective Sequence Separation Rate: ", objSeqRate)

    return subSeqRate, objSeqRate

if __name__ == "__main__":

    numOrAct = "n"
    totalParticipant = 24
    dropOut = {}
    interval = 20

    # subSequenceCorrPlot2(numOrAct, totalParticipant, dropOut, interval)
    # objSequenceCorrPlot2(numOrAct, totalParticipant, dropOut, interval)
    # subObjCorrPlot2(numOrAct, totalParticipant, dropOut, interval)

    # separation rate
    separation = [sfSeparationRate(numOrAct, totalParticipant, dropOut, inter) for inter in range(interval)]
    subSeqRate, objSeqRate = zip(*separation)

    xValues = [i for i in range(interval)]
    plt.plot(xValues, subSeqRate, label = "Subjective")
    plt.plot(xValues, objSeqRate, label = "Objective")
    plt.legend(loc='upper right')
    plt.title('Sequence Separation Rate')
    plt.show()