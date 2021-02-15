def minkovskiy_distance(row1, row2, p):
    distance = 0.0
    for i in range(len(row1) - 4):
        distance += (row1[i] - row2[i]) ** p
    return distance ** (1 / p)


def euclidean_distance(row1, row2):
    return minkovskiy_distance(row1, row2, 2)


def manhattan_distance(row1, row2):
    return minkovskiy_distance(row1, row2, 1)


def chebishev_distance(row1, row2):
    distance = 0.0
    for i in range(len(row1) - 4):
        distance = max(distance, abs(row1[i] - row2[i]))
    return distance


distances_names = ["Euclidean", "Manhattan", "Chebishev"]
distances = [euclidean_distance, manhattan_distance, chebishev_distance]


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
