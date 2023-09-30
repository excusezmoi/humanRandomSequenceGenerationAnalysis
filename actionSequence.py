from Markov import MarkovChainAll
from utils import configFilePath, startToSimilarMatrix2
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import scipy.stats as stats


def googleMatrix():
    return np.array(
    [[854000,35100,494000,30100,17700,12100], 
    [54400,1660000,4010000,44800,28100,409000], 
    [897000,131000,15000000,166000,27800,111000],
    [337000,399000,1050000,57100000,1090000,2160000], 
    [126000,144000,76400,11000000,16700000,3070000],
    [75700,170000,450000,1290000,481000,18400000]])

def matrixCorr(matrix1, matrix2):
    matrix1Flat = matrix1.flatten()
    matrix2Flat = matrix2.flatten()
    return stats.spearmanr(matrix1Flat, matrix2Flat)




if __name__ == "__main__":
    totalParticipant = 24
    txtFileFolder = configFilePath("FOLDER","responseFileFolder")

    theAnswer = MarkovChainAll(totalParticipant, txtFileFolder)

    dropOut = {}

    def plotCorrSequenceGoogle():
        recordS = []
        google = googleMatrix()
        for participant in range(1, totalParticipant + 1):
            if participant in dropOut:
                continue
            ma = getattr(theAnswer, "p" + str(participant)).sact.MarkovMatrix
            recordS.append(matrixCorr(ma, google)[0])
        # print(record)
        # plt.bar(range(totalParticipant), record)
        plt.hist(recordS, bins = 10, ec = "black", alpha = 0.5, label = "sact")


        recordF = []
        google = googleMatrix()
        for participant in range(1, totalParticipant + 1):
            if participant in dropOut:
                continue
            ma = getattr(theAnswer, "p" + str(participant)).fact.MarkovMatrix
            recordF.append(matrixCorr(ma, google)[0])
        # print(record)
        # plt.bar(range(totalParticipant), record)
        plt.hist(recordF, bins = 10, ec = "black", alpha = 0.5, label = "fact")

        plt.legend(loc='upper right')
        plt.title('Sequence and Google Correlation Distribution')
        plt.show()

        # res = stats.wilcoxon(recordS, recordF)
        # print(res)
        accuracy = sum(i < j for i, j in zip(recordS, recordF)) / len(recordS)
        print(accuracy)

    def plotCorrSubGoogle():
        subAndGoogle = []
        for participantNumber in range(1,totalParticipant+1):
            matrix1 = startToSimilarMatrix2(participantNumber, "a", totalParticipant)
            matrix2 = googleMatrix()
            subAndGoogle.append(matrixCorr(matrix1, matrix2)[0])
        
        plt.hist(subAndGoogle, bins = 10, ec = "black", alpha = 0.5, label = "subAndGoogle")
        plt.show()

    def plotCorrSequenceSub():
        recordS = []

        for participant in range(1, totalParticipant + 1):
            if participant in dropOut:
                continue
            ma = getattr(theAnswer, "p" + str(participant)).sact.MarkovMatrix
            sub = startToSimilarMatrix2(participant, "a", totalParticipant)
            recordS.append(matrixCorr(ma, sub)[0])
        # print(record)
        # plt.bar(range(totalParticipant), record)
        plt.hist(recordS, bins = 10, ec = "black", alpha = 0.5, label = "sact")


        recordF = []

        for participant in range(1, totalParticipant + 1):
            if participant in dropOut:
                continue
            ma = getattr(theAnswer, "p" + str(participant)).fact.MarkovMatrix
            sub = startToSimilarMatrix2(participant, "a", totalParticipant)
            recordF.append(matrixCorr(ma, sub)[0])
        # print(record)
        # plt.bar(range(totalParticipant), record)
        plt.hist(recordF, bins = 10, ec = "black", alpha = 0.5, label = "fact")

        plt.legend(loc='upper right')
        plt.title('Sequence and Subjective Correlation Distribution')
        plt.show()

        # res = stats.wilcoxon(recordS, recordF)
        # print(res)
        accuracy = sum(i < j for i, j in zip(recordS, recordF)) / len(recordS)
        print(accuracy)

    plotCorrSequenceGoogle() 
    #WilcoxonResult(statistic=34.0, pvalue=0.0004298686981201172)
    #accuracy: 0.83333

    # plotCorrSequenceSub() 
    # WilcoxonResult(statistic=40.0, pvalue=0.0009626150131225586)
    # accuracy: 0.83333
