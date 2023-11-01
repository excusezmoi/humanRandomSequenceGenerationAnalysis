import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from utils import startToSimilarMatrix, matrixCorr, configFilePath
from Markov import MarkovChainAll

#similarity matrix correlation
def corOfSimilarityMatrices(numOrAct,participantNumber1, participantNumber2, totalParticipant):
    similar1 = startToSimilarMatrix(participantNumber1, numOrAct, totalParticipant)
    similar2 = startToSimilarMatrix(participantNumber2, numOrAct, totalParticipant)
    return matrixCorr(similar1, similar2)

if __name__ == "__main__":
    
    participantNumber1 = 1
    participantNumber2 = 2
    totalParticipant = 24
    numOrAct = "n"

    dropOut = {}

    # print(corOfSimilarityMatrices(numOrAct,participantNumber1, participantNumber2, totalParticipant))
    fullMatrix = np.array([[5 for i in range(6)] for j in range(6)])
    objDisMatrix = fullMatrix - np.array([[i for i in range(6)], [1, 0, 1, 2, 3, 4], [2, 1, 0, 1, 2, 3], [3, 2, 1, 0, 1, 2], [4, 3, 2, 1, 0, 1], [5, 4, 3, 2, 1, 0]])
    # print(objDisMatrix)

    def subSequenceCorrPlot():
        theAnswer = MarkovChainAll(totalParticipant, configFilePath("FOLDER","responseFileFolder"))
        recordS = []

        for participant in range(1, totalParticipant + 1):
            if participant in dropOut:
                continue
            ma = getattr(theAnswer, "p" + str(participant)).snum.MarkovMatrix
            sub = startToSimilarMatrix(participant, "n", totalParticipant)
            recordS.append(matrixCorr(ma, sub)[0])
        # print(record)
        # plt.bar(range(totalParticipant), record)
        plt.hist(recordS, bins = 10, ec = "black", alpha = 0.5, label = "slow")


        recordF = []

        

        for participant in range(1, totalParticipant + 1):
            if participant in dropOut:
                continue
            ma = getattr(theAnswer, "p" + str(participant)).fnum.MarkovMatrix
            sub = startToSimilarMatrix(participant, "n", totalParticipant)
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
        # accuracy = [i < j for i, j in zip(recordS, recordF)]
        print(accuracy)

    # subSequenceCorrPlot()

    def objSequenceCorrPlot():
        theAnswer = MarkovChainAll(totalParticipant, configFilePath("FOLDER","responseFileFolder"))
        recordS = []

        for participant in range(1, totalParticipant + 1):
            if participant in dropOut:
                continue
            ma = getattr(theAnswer, "p" + str(participant)).snum.MarkovMatrix
            recordS.append(matrixCorr(ma, objDisMatrix)[0])

        plt.hist(recordS, bins = 10, ec = "black", alpha = 0.5, label = "slow")


        recordF = []

        for participant in range(1, totalParticipant + 1):
            if participant in dropOut:
                continue
            ma = getattr(theAnswer, "p" + str(participant)).fnum.MarkovMatrix
            recordF.append(matrixCorr(ma, objDisMatrix)[0])

        plt.hist(recordF, bins = 10, ec = "black", alpha = 0.5, label = "fast")

        plt.legend(loc='upper right')
        plt.title('Objective and Markov Matrix Correlation Distribution')
        plt.show()

        # res = stats.wilcoxon(recordS, recordF)
        # print(res)
        accuracy = sum(i < j for i, j in zip(recordS, recordF)) / len(recordS)
        print(accuracy)

    objSequenceCorrPlot()

    def subObjCorrPlot():
        record = []
        for participant in range(1, totalParticipant + 1):
            if participant in dropOut:
                continue
            similar1 = startToSimilarMatrix(participant, numOrAct, totalParticipant)
            record.append(matrixCorr(similar1, objDisMatrix)[0])
        
        plt.hist(record, bins = 10, ec = "black", alpha = 0.5)
        plt.title('Subjective and Objective Similarity Matrix Correlation Distribution')
        plt.show()
    
    # subObjCorrPlot()

        