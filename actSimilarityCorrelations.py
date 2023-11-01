import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import scipy.stats as stats

from utils import configFilePath, startToSimilarMatrix, matrixCorr
from Markov import MarkovChainAll


def googleMatrix():
    return np.array(
    [[854000,35100,494000,30100,17700,12100], 
    [54400,1660000,4010000,44800,28100,409000], 
    [897000,131000,15000000,166000,27800,111000],
    [337000,399000,1050000,57100000,1090000,2160000], 
    [126000,144000,76400,11000000,16700000,3070000],
    [75700,170000,450000,1290000,481000,18400000]])

def subSequenceCorrPlot(totalParticipant, dropOut):
    theAnswer = MarkovChainAll(totalParticipant, configFilePath("FOLDER","responseFileFolder"))
    recordS = []

    for participant in range(1, totalParticipant + 1):
        if participant in dropOut:
            continue
        ma = getattr(theAnswer, "p" + str(participant)).sact.MarkovMatrix
        sub = startToSimilarMatrix(participant, "a", totalParticipant)
        recordS.append(matrixCorr(ma, sub)[0])
    # print(record)
    # plt.bar(range(totalParticipant), record)
    plt.hist(recordS, bins = 10, ec = "black", alpha = 0.5, label = "slow")

    recordF = []

    for participant in range(1, totalParticipant + 1):
        if participant in dropOut:
            continue
        ma = getattr(theAnswer, "p" + str(participant)).fact.MarkovMatrix
        sub = startToSimilarMatrix(participant, "a", totalParticipant)
        recordF.append(matrixCorr(ma, sub)[0])
    # print(record)
    # plt.bar(range(totalParticipant), record)
    plt.hist(recordF, bins = 10, ec = "black", alpha = 0.5, label = "fast")

    plt.legend(loc='upper right')
    plt.title('Subjective and Markov Matrix Correlation Distribution')
    plt.show()

    # res = stats.wilcoxon(recordS, recordF)
    # print(res)
    accuracy = sum(i < j for i, j in zip(recordS, recordF)) / len(recordS)
    print(accuracy)


def googleSequenceCorrPlot(totalParticipant, dropOut):
    theAnswer = MarkovChainAll(totalParticipant, configFilePath("FOLDER","responseFileFolder"))
    recordS = []
    google = googleMatrix()
    for participant in range(1, totalParticipant + 1):
        if participant in dropOut:
            continue
        ma = getattr(theAnswer, "p" + str(participant)).sact.MarkovMatrix
        recordS.append(matrixCorr(ma, google)[0])
    # print(record)
    # plt.bar(range(totalParticipant), record)
    plt.hist(recordS, bins = 10, ec = "black", alpha = 0.5, label = "slow")


    recordF = []
    google = googleMatrix()
    for participant in range(1, totalParticipant + 1):
        if participant in dropOut:
            continue
        ma = getattr(theAnswer, "p" + str(participant)).fact.MarkovMatrix
        recordF.append(matrixCorr(ma, google)[0])
    # print(record)
    # plt.bar(range(totalParticipant), record)
    plt.hist(recordF, bins = 10, ec = "black", alpha = 0.5, label = "fast")

    plt.legend(loc='upper right')
    plt.title('Google and Markov Matrix Correlation Distribution')
    plt.show()

    # res = stats.wilcoxon(recordS, recordF)
    # print(res)
    accuracy = sum(i < j for i, j in zip(recordS, recordF)) / len(recordS)
    print(accuracy)

def subGoogleCorrPlot(totalParticipant, dropOut):
    subAndGoogle = []
    for participantNumber in range(1,totalParticipant+1):
        matrix1 = startToSimilarMatrix(participantNumber, "a", totalParticipant)
        matrix2 = googleMatrix()
        subAndGoogle.append(matrixCorr(matrix1, matrix2)[0])
    
    plt.hist(subAndGoogle, bins = 10, ec = "black", alpha = 0.5, label = "subAndGoogle")
    plt.title('Google and Subjective Similarity Matrix Correlation Distribution')
    plt.show()

if __name__ == "__main__":
    totalParticipant = 24
    dropOut = {3,14,24}

    # subSequenceCorrPlot(totalParticipant, dropOut) 
    # WilcoxonResult(statistic=40.0, pvalue=0.0009626150131225586)
    # accuracy: 0.83333

    # googleSequenceCorrPlot(totalParticipant, dropOut) 
    #WilcoxonResult(statistic=34.0, pvalue=0.0004298686981201172)
    #accuracy: 0.83333

    # subGoogleCorrPlot(totalParticipant, dropOut)