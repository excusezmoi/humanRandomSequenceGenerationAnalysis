# clustering elbow method: failed
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans

from utils import startToSimilarMatrix, startToReadCSVAndConvertToFloat, createMatrix, toSimilarityMatrix

def clusteringElbowMethodExe(numOrAct, totalParticipant):
    #kmeans clustering of subjective similarity matrices
    
    similarityMatrixAll = []

    for i in range(totalParticipant):
        participantNumber = i + 1
        similarityMatrixAll.append(startToSimilarMatrix(participantNumber, numOrAct, totalParticipant))

    # create a numpy array to store the similarity matrices
    similarity_matrix_array = np.array(similarityMatrixAll)

    # Load data and convert to numpy array
    data = similarity_matrix_array
    n_samples, n_features, _ = data.shape
    data_2d = data.reshape((n_samples, n_features * n_features))
    
    # Define range of cluster numbers to try
    cluster_range = range(1, totalParticipant + 1)

    # Calculate WCSS for each cluster number
    wcss = []
    for n_clusters in cluster_range:
        kmeans = KMeans(n_clusters=n_clusters)
        kmeans.fit(data_2d)
        wcss.append(kmeans.inertia_)

    # Plot WCSS as a function of cluster number
    plt.plot(cluster_range, wcss, '-o')
    plt.xlabel('Number of clusters')
    plt.ylabel('WCSS action')
    plt.show()

#clustering analysis no need: sad
def clusteringAnalysisExe(numOrAct, totalParticipant, numOfClusters):
    #kmeans clustering of subjective similarity matrices  
    similarityMatrixAll = []

    for i in range(totalParticipant):
        participantNumber = i+1
        df = startToReadCSVAndConvertToFloat(totalParticipant) #number of participants
        upperTriangle = createMatrix(df, participantNumber, numOrAct) #df, participantNumber, numOrAct
        # plotMatrix(upperTriangle, numOrAct)
        similarityMatrixAll.append(toSimilarityMatrix(upperTriangle))

    # create a numpy array to store the similarity matrices
    similarity_matrix_array = np.stack([matrix.flatten() for matrix in similarityMatrixAll])

    # run k-means clustering
    kmeans = KMeans(n_clusters=numOfClusters, random_state=0).fit(similarity_matrix_array)

    # get the cluster centers and labels
    cluster_centers = kmeans.cluster_centers_
    labels = kmeans.labels_

    # analyze the results
    for i in range(numOfClusters):
        cluster_samples = np.where(labels == i)[0]  # get the indices of samples in the cluster
        print(f"Cluster {i}: {cluster_samples}")

if __name__ == "__main__":
    
    numOrAct = "a"
    totalParticipant = 9
    numOfClusters = 3

    clusteringElbowMethodExe(numOrAct, totalParticipant)
    clusteringAnalysisExe(numOrAct, totalParticipant, numOfClusters)