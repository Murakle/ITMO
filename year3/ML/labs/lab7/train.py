import pandas as pd


def get_minmax(dataset):
    minmax = list()
    for i in range(len(dataset[0])):
        value_max = 0.0
        value_min = 1e9
        for j in range(len(dataset)):
            value_min = min(value_min, dataset[j][i])
            value_max = max(value_max, dataset[j][i])
        minmax.append([value_min, value_max])
    return minmax


def normalize(dataset):
    minmax = get_minmax(dataset)
    for row in dataset:
        for i in range(len(row) - 1):
            if i == 0:
                continue
            if minmax[i][1] - minmax[i][0] == 0:
                row[i] = 0.0
                continue
            row[i] = (row[i] - minmax[i][0]) / (minmax[i][1] - minmax[i][0])
    return dataset


def get_unique_values(dataset):
    result = set()
    for i in range(len(dataset)):
        result.add(dataset[i][0])
    return result



def train():
    filename = 'dataset.csv'
    dataset = pd.read_csv(filename)
    return normalize(dataset.values)
