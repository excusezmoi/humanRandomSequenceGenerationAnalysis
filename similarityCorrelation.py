import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from main import startToSimilarMatrix

#Calculate the correlation of two similarity matrices
def corOfMatrices(similarityMatrix1, similarityMatrix2):
    return np.corrcoef(similarityMatrix1.flatten(), similarityMatrix2.flatten())[0,1]

#similarity matrix correlation
def corOfSimilarityMatrices(numOrAct,participantNumber1, participantNumber2, totalParticipant):
    similar1 = startToSimilarMatrix(participantNumber1, numOrAct, totalParticipant)
    similar2 = startToSimilarMatrix(participantNumber2, numOrAct, totalParticipant)
    return corOfMatrices(similar1, similar2)

if __name__ == "__main__":
    
    participantNumber1 = 1
    participantNumber2 = 2
    totalParticipant = 10
    numOrAct = "n"

    print(corOfSimilarityMatrices(numOrAct,participantNumber1, participantNumber2, totalParticipant))