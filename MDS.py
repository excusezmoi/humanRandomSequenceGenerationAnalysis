# Description: This file contains the code to plot the MDS
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import MDS

from utils import startToSimilarMatrix, startToReadCSVAndConvertToFloat, createMatrix2, similarityToDissimilarity, toSimilarityMatrix

class MDSPlotter:
    def __init__(self, numOrAct, totalParticipant):
        self.numOrAct = numOrAct
        self.totalParticipant = totalParticipant
        self.df = startToReadCSVAndConvertToFloat(totalParticipant, numOrAct)
        # self.similar = startToSimilarMatrix(participantNumber, numOrAct, totalParticipant)
        # self.dissimilar = similarityToDissimilarity(self.similar)

    def plotMDS(self, dissimilar):
        mds = MDS(n_components = 2, dissimilarity = "precomputed", random_state=1)
        pos = mds.fit_transform(dissimilar)
        xs, ys = pos[:, 0], pos[:, 1]

        labels = [f"{i}" for i in range(1,7)] if self.numOrAct == "n" else ["L","Q","S","W","R","J"] if self.numOrAct == "a" else None

        for x, y, label in zip(xs, ys, labels):
            plt.scatter(x, y, marker='o', color='purple')
            plt.text(x, y, label, fontsize=15, color = 'darkblue')
        plt.show()

    def plotPersonalMDS(self, participantNumber):
        similar = startToSimilarMatrix(participantNumber, self.numOrAct, self.totalParticipant)
        dissimilar = similarityToDissimilarity(similar)
        self.plotMDS(dissimilar)

    def plotMDSonSubPlots(self, dissimilar, sub):
        mds = MDS(n_components = 2, dissimilarity = "precomputed", random_state = 1)
        pos = mds.fit_transform(dissimilar)
        xs, ys = pos[:, 0], pos[:, 1]

        labels = [f"{i}" for i in range(1,7)] if self.numOrAct == "n" else ["L","Q","S","W","R","J"] if self.numOrAct == "a" else None
        labelColors = {'L': 'red', 'Q': 'orange', 'S': 'yellow', 'W': 'green', 'R': 'blue', 'J': 'purple'} if self.numOrAct == "a" else {'1': 'red', '2': 'orange', '3': 'yellow', '4': 'green', '5': 'blue', '6': 'purple'} if self.numOrAct == "n" else None

        for x, y, label in zip(xs, ys, labels):
            sub.scatter(x, y, marker='o', color=labelColors[label])

    def plotAllMDS(self):
        sideNumber = (lambda x: int(x**0.5) if x**0.5 == int(x**0.5) else int(x**0.5) + 1)(self.totalParticipant)
        fig, axs = plt.subplots(nrows=sideNumber, ncols=sideNumber, figsize=(8, 8))
        for i in range(self.totalParticipant):
            participantNumber = i + 1
            df = startToReadCSVAndConvertToFloat(self.totalParticipant, self.numOrAct)
            upperTriangle = createMatrix2(df, participantNumber, self.numOrAct)
            similar = toSimilarityMatrix(upperTriangle)
            dissimilar = similarityToDissimilarity(similar)
            row, col= i // sideNumber, i % sideNumber
            self.plotMDSonSubPlots(dissimilar, axs[row, col])
        labelColors = {'L': 'red', 'Q': 'orange', 'S': 'yellow', 'W': 'green', 'R': 'blue', 'J': 'purple'} if self.numOrAct == "a" else {'1': 'red', '2': 'orange', '3': 'yellow', '4': 'green', '5': 'blue', '6': 'purple'} if self.numOrAct == "n" else None
        handles = [plt.Line2D([], [], color=color, marker='o', linestyle='None', label=label) for label, color in labelColors.items()]
        plt.legend(handles=handles, loc='lower right')
        plt.show()

if __name__ == "__main__":
    
    participantNumber = 20
    numOrAct = "n"
    totalParticipant = 24

    mds = MDSPlotter(numOrAct, totalParticipant)
    mds.plotPersonalMDS(participantNumber)
    mds.plotAllMDS()