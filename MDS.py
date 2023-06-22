# Description: This file contains the code to plot the MDS
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import MDS

from main import startToSimilarMatrix, similarityToDissimilarity, startToReadCSVAndConvertToFloat, createMatrix, toSimilarityMatrix

#Plot the MDS
def plotMDS(dissimilar, numOrAct):
    
    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
    pos = mds.fit_transform(dissimilar)
    xs, ys = pos[:, 0], pos[:, 1]

    labels = [f"{i}" for i in range(1,7)] if numOrAct == "n" else ["L","Q","S","W","R","J"] if numOrAct == "a" else None

    for x, y, label in zip(xs, ys, labels):
        plt.scatter(x, y, marker='o', color='purple')
        plt.text(x, y, label, fontsize=15, color = 'darkblue')
    plt.show()

#Plot the MDS
def plotMDSExe(participantNumber, numOrAct, totalParticipant):
    similar = startToSimilarMatrix(participantNumber, numOrAct, totalParticipant)
    dissimilar = similarityToDissimilarity(similar)
    plotMDS(dissimilar, numOrAct)

#Plot all the MDS
def plotMDSonSubPlots(dissimilar, numOrAct, sub):
    
    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
    pos = mds.fit_transform(dissimilar)
    xs, ys = pos[:, 0], pos[:, 1]

    labels = [f"{i}" for i in range(1,7)] if numOrAct == "n" else ["L","Q","S","W","R","J"] if numOrAct == "a" else None
    labelColors = {'L': 'red', 'Q': 'orange', 'S': 'yellow', 'W': 'green', 'R': 'blue', 'J': 'purple'} if numOrAct == "a" else {'1': 'red', '2': 'orange', '3': 'yellow', '4': 'green', '5': 'blue', '6': 'purple'} if numOrAct == "n" else None

    for x, y, label in zip(xs, ys, labels):
        sub.scatter(x, y, marker='o', color=labelColors[label])

    # Plot all the MDS
def plotAllMDSExe(numOrAct, totalParticipant):
    fig, axs = plt.subplots(nrows=3, ncols=3, figsize=(8, 8))
    for i in range(totalParticipant):
        participantNumber = i+1
        df = startToReadCSVAndConvertToFloat(totalParticipant) #number of participants
        upperTriangle = createMatrix(df, participantNumber, numOrAct) #df, participantNumber, numOrAct
        similar = toSimilarityMatrix(upperTriangle)
        dissimilar = similarityToDissimilarity(similar)
        row = i // 3
        col = i % 3
        plotMDSonSubPlots(dissimilar, numOrAct, axs[row, col])
    labelColors = {'L': 'red', 'Q': 'orange', 'S': 'yellow', 'W': 'green', 'R': 'blue', 'J': 'purple'} if numOrAct == "a" else {'1': 'red', '2': 'orange', '3': 'yellow', '4': 'green', '5': 'blue', '6': 'purple'} if numOrAct == "n" else None
    handles = [plt.Line2D([], [], color=color, marker='o', linestyle='', label=label) for label, color in labelColors.items()]
    plt.legend(handles=handles)
    plt.show()

if __name__ == "__main__":
    
    participantNumber = 7
    numOrAct = "a"
    slowOrFast = "s"
    totalParticipant = 9
    
    plotMDSExe(participantNumber, numOrAct, totalParticipant)
    plotAllMDSExe(numOrAct, totalParticipant)