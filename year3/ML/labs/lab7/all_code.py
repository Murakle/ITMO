from kmeans import kmeans
from matplotlib import pyplot as plt
from train import train
from metrix import rand_index, silhouette
from sklearn.decomposition import IncrementalPCA
from sklearn.manifold import TSNE
import distance
import numpy as np
#import seaborn as sns; sns.set()

def draw(X, klasters):
    plt.scatter(X[:, 0], X[:, 1], c=klasters, s=15, cmap='viridis')
    plt.title("k = 3")
    plt.show()


if __name__ == '__main__':
    dataset = train()
    pca = IncrementalPCA()
    X = dataset[:,1:]
    Y = dataset[:,0]
    pca.fit(X)
    X = pca.transform(X)
    plt.scatter(X[:, 0], X[:, 1], c=Y, s=15, cmap='viridis')
    plt.title("Target")
    plt.show()
    max_rand = 0
    max_rand_i = 0
    max_rand_k = 0
    for i in range(distance.get_distances_amount()):
        k_inx = []
        ks = []
        ss = []
        for k in range(2, 10):
            klasters = kmeans(X, k, i, 1000)
            k_inx.append(k)
            rand = rand_index(klasters, dataset)
            s = silhouette(k, klasters, dataset, i)
            ss.append(s)
            ks.append(rand)
            if rand > max_rand:
                max_rand = rand
                max_rand_i = i
                max_rand_k = k
            if k == 3 and i == 0:
                plt.scatter(X[:, 0], X[:, 1], c=klasters, s=15, cmap='viridis')
                plt.title("Best variant, k = 3")
                plt.show()
        plt.plot(k_inx, ks)
        plt.title("Rand index, Distance - " + distance.get_distance_name(i))
        plt.show()
        plt.plot(k_inx, ss)
        plt.title("Siluette, Distance - " + distance.get_distance_name(i))
        plt.show()
    print(max_rand)
    print(max_rand_i)
    print(max_rand_k)

'''
kmeans.py
'''
import random
from distance import get_distance


def kmeans(dataset, k: int, distance_index: int, max_iter: int):
    centers = choose_centers(dataset, k)
    centers_old = [] * k
    for i in range(k):
        row = [0] * len(centers[0])
        centers_old.append(row)
    n = len(dataset)
    for c_iter in range(max_iter):
        for i in range(n):
            distance = [0.0] * k
            for j in range(k):
                distance[j] = get_distance(distance_index, centers[j], dataset[i])
            min_distance_index = 0
            for j in range(k):
                if distance[j] < distance[min_distance_index]:
                    min_distance_index = j
            centers[min_distance_index] = get_center(centers[min_distance_index], dataset[i])
        if compare_centers(centers, centers_old):
            break
        centers_old = centers.copy()
    klaster = [0] * n
    for i in range(n):
        distance = [0.0] * k
        for j in range(k):
            distance[j] = get_distance(distance_index, centers[j], dataset[i])
        min_distance_index = 0
        for j in range(k):
            if distance[j] < distance[min_distance_index]:
                min_distance_index = j
        klaster[i] = min_distance_index
    return klaster


def get_center(row1, row2):
    row_res = [0.0] * len(row1)
    for i in range(len(row1)):
        row_res[i] = (row1[i] + row2[i])/2
    return row_res


def choose_centers(dataset, k: int):
    n = len(dataset)
    center_indicies = []
    center = []
    for i in range(k):
        r = random.randint(0, n - 1)
        while r in center_indicies:
            r = random.randint(0, n - 1)
        center_indicies.append(r)
        center.append(dataset[r])
    return center


def compare_centers(centers, centers_old):
    for i in range(len(centers)):
        for j in range(len(centers[i])):
            if centers[i][j] != centers_old[i][j]:
                return False
    return True

'''
distance
'''
def minkovskiy_distance(row1, row2, p):
    distance = 0.0
    for i in range(len(row1)):
        if i != 0:
            distance += (row1[i] - row2[i]) ** p
    return distance ** (1 / p)


def euclidean_distance(row1, row2):
    return minkovskiy_distance(row1, row2, 2)


def manhattan_distance(row1, row2):
    return minkovskiy_distance(row1, row2, 1)


def chebishev_distance(row1, row2):
    distance = 0.0
    for i in range(len(row1)):
        if i != 0:
            distance = max(distance, abs(row1[i] - row2[i]))
    return distance


distances_names = ["Euclidean", "Chebishev"]
distances = [euclidean_distance, chebishev_distance]


def get_distance_name(index):
    return distances_names[index]


def get_distances_amount():
    return len(distances)


def get_all_distances(dataset, distance_index):
    dist = [] * len(dataset)
    for i in range(len(dataset)):
        row = [0.0] * len(dataset)
        dist.append(row)
        for j in range(0, i):
            dist[i][j] = dist[j][i]
        for j in range(i, len(dataset)):
            dist[i][j] = get_distance(distance_index, dataset[i], dataset[j])
    return dist


def get_distance(index, row1, row2):
    return distances[index](row1, row2)


'''
metrix
'''
from distance import get_distance
def rand_index(klasters, dataset):
    n = len(dataset)
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    for i in range(n):
        for j in range(n):
            if dataset[i][0] == dataset[j][0]:
                if klasters[i] == klasters[j]:
                    tp+=1
                else:
                    fp+=1
            else:
                if klasters[i] == klasters[j]:
                    tn+=1
                else:
                    fn+=1
    #unique_vals = list(get_unique_values(dataset.values))
    return (tp + fn) / (tp + tn + fp + fn)


def silhouette(k, klasters, dataset, distance_index):
    # split to clasters
    n = len(klasters)
    indicies = [] * k
    for i in range(k):
        row = [] * k
        indicies.append(row)
    for i in range(n):
        indicies[klasters[i]].append(i)
    res = 0
    for i in range(k):
        if len(indicies[i]) == 0:
            continue
        for j in indicies[i]:
            a = 0
            for h in indicies[i]:
                d = get_distance(distance_index, dataset[j], dataset[h])
                a += d
            a /= len(indicies[i])
            b = 1e9
            for p in range(k):
                if p != i and len(indicies[p]) != 0:
                    bb = 0
                    for h in indicies[p]:
                        d = get_distance(distance_index, dataset[j], dataset[h])
                        bb += d
                    bb /= len(indicies[p])
                    b = min(b, bb)
            res += (b - a) / max(a, b)
    res /= n
    return res
