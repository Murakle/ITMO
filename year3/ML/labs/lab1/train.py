import pandas as pd


def get_minmax(dataset):
    minmax = list()
    for i in range(len(dataset[0])):
        if i == len(dataset[0]) - 1:
            continue
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
        for i in range(len(row)):
            if i == len(row) - 1:  # exclude target
                continue
            if minmax[i][1] - minmax[i][0] == 0:
                row[i] = 0.0
                continue
            row[i] = (row[i] - minmax[i][0]) / (minmax[i][1] - minmax[i][0])
    return dataset


def get_unique_values(dataset):
    result = set()
    for i in range(len(dataset)):
        result.add(dataset[i][-1])
    return result


# only target value in this dataset
def one_hot_encoding(dataset):
    unique_values = list(get_unique_values(dataset))
    unique_values.sort()
    actual_vals_list = list()
    new_dataset = [] * len(dataset)
    for i in range(len(dataset)):
        new_row = dataset[i].tolist()
        last = new_row[-1]
        actual_vals_list.append(last)
        new_t = [0, 0, 0, 0]
        index = 0
        for j in range(len(unique_values)):
            if unique_values[j] == last:
                index = j
                break
        new_t[index] = 1
        for j in range(len(unique_values)):
            if j == 0:
                new_row[-1] = new_t[j]
            else:
                new_row.append(new_t[j])
        new_dataset.append(new_row)
    return unique_values, actual_vals_list, new_dataset


def train():
    filename = 'dataset.csv'
    dataset = pd.read_csv(filename)
    return one_hot_encoding(normalize(dataset.values))
