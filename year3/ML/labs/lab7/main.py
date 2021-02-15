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
            klasters = kmeans(X, k, i, 51)
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

