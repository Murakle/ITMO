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
