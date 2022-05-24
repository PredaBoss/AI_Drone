import csv
import math
from random import sample, seed

import numpy as np
from scipy.spatial.distance import cdist
from sklearn.decomposition import PCA
from tqdm import trange
import matplotlib.pyplot as plt

NUMBER_OF_CLUSTERS = 4

def euclidean_distance(a,b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def readPoints():
    data = {}
    first = True
    with open('dataset.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if first:
                first = False
                continue
            data[(float(row[1]),float(row[2]))] = row[0]
            # Complete appending point (row1, row2) to points list
    return data

def assignPointsToCentroids(points, centroids):
    assigned = {}
    for centroid in centroids:
        assigned[centroid] = []

    for point in points:
        lowestDistance = np.inf
        chosenCentroid = None

        for centroid in centroids:
            dist = math.sqrt((centroid[0] - point[0]) ** 2 + (centroid[1] - point[1]) ** 2)
            if dist < lowestDistance:
                lowestDistance = dist
                chosenCentroid = centroid

        assigned[chosenCentroid].append(point)

    return assigned

def changeCentroids(clusters):
    newCentroids = []

    for centroid in clusters.keys():
        currentCluster = clusters[centroid]
        newCentroid = (np.mean([point[0] for point in currentCluster]), np.mean([point[1] for point in currentCluster]))
        newCentroids.append(newCentroid)

    return newCentroids

def get_statistics(clusters, initialData):
    centroids = list(clusters.keys())

    centroidA = min(centroids, key=lambda x: x[0])
    centroids.remove(centroidA)

    centroidC = max(centroids, key=lambda x: x[0])
    centroids.remove(centroidC)

    centroidD = min(centroids, key=lambda x: x[1])
    centroids.remove(centroidD)

    mappedCentroids = {centroidA: 'A', centroids[0]: 'B', centroidC: 'C', centroidD: 'D'}

    nrOfCorrectlyComputed = 0
    correctForLabel = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    totalForLabel = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    totalInitialLabel = {'A': 0, 'B': 0, 'C': 0, 'D': 0}

    for key, value in clusters.items():
        for val in value:
            if initialData[val] == mappedCentroids[key]:
                nrOfCorrectlyComputed += 1
                correctForLabel[initialData[val]] += 1
            totalForLabel[mappedCentroids[key]] += 1
            totalInitialLabel[initialData[val]] += 1

    accuracyIndex = nrOfCorrectlyComputed / len(initialData)
    print("Accuracy index:", accuracyIndex)

    precision = {}
    rappel = {}
    score = {}
    for key in ['A', 'B', 'C', 'D']:
        precision[key] = correctForLabel[key] / totalForLabel[key]
        rappel[key] = correctForLabel[key] / totalInitialLabel[key]
        score[key] = 2 * precision[key] * rappel[key] / (precision[key] + rappel[key] + 1)

    print("\nPrecision:")
    for key, val in precision.items():
        print(key,"->",val)
    print("\nRappel:")
    for key, val in rappel.items():
        print(key,"->",val)
    print("\nScore:")
    for key, val in score.items():
        print(key,"->",val)

if __name__ == "__main__":
    # load data
    data = readPoints()
    points = data.keys()

    ansDunnIndex = -np.inf
    ansClusters = {}

    for i in range(100):
        seed(i+1)
        initial_centroids = sample(points, NUMBER_OF_CLUSTERS)

        # Assign points to centroids...
        clusters = assignPointsToCentroids(points,initial_centroids)
        newCentroids = changeCentroids(clusters)

        # Until centroids do not change anymore
        centroids = initial_centroids
        while centroids != newCentroids:
            centroids = newCentroids
            clusters = assignPointsToCentroids(points, centroids)
            newCentroids = changeCentroids(clusters)

        # Calculating the Dunn index
        interDistance = min([euclidean_distance(centroids[a], centroids[b]) for a in range(NUMBER_OF_CLUSTERS) for b in range(a+1, NUMBER_OF_CLUSTERS)])
        intraDistance = max([euclidean_distance(point, centroid) for centroid in clusters.keys() for point in clusters[centroid]])
        obtainedDunnIndex = interDistance / intraDistance

        if ansDunnIndex < obtainedDunnIndex:
            ansDunnIndex = obtainedDunnIndex
            ansClusters = clusters


    colours = ['red', 'green', 'blue', 'yellow']
    index = 0
    for key in ansClusters:
        plt.scatter([point[0] for point in ansClusters[key]], [point[1] for point in ansClusters[key]], c = colours[index])
        index += 1
    plt.scatter([centroid[0] for centroid in ansClusters], [centroid[1] for centroid in ansClusters], c='black')
    plt.show()

    get_statistics(ansClusters, data)
