# main.py

from train import train
import distance
from kernel import get_kernels_amount, get_kernel_name
from window import get_windows_amount, get_steps_amount, get_step, get_window_name
from f import get_f1

import predict
from matplotlib import pyplot as plt

if __name__ == '__main__':
    target_vals, actual_vals_list, dataset = train()
    dataset_length = len(dataset)
    steps_amount = get_steps_amount(dataset_length)
    distances_amount = distance.get_distances_amount()
    max_i = max_j = max_k = max_f = 0
    max_steps = [0.0] * steps_amount
    max_fs = [0.0] * steps_amount
    for i in range(distances_amount):
        all_distances = distance.get_all_distances(dataset, i)
        all_distances_sorted = [] * dataset_length
        for q in range(dataset_length):
            row = all_distances[q].copy()
            row.sort()
            all_distances_sorted.append(row)
        max_distance = predict.get_max_distance(all_distances_sorted)  # O(n^2)
        for j in range(get_kernels_amount()):
            for k in range(0, get_windows_amount()):
                print(i * get_kernels_amount() * get_windows_amount() + j * get_windows_amount() + k, end=" / ")
                print(distances_amount * get_kernels_amount() * get_windows_amount())
                f_with_diff_window = [0.0] * steps_amount
                steps = [0.0] * steps_amount
                current_step = get_step(k, dataset_length, max_distance)
                for n in range(1, steps_amount + 1):  # is here +1? # sqrt(n)
                    window_size = n * current_step
                    res = predict.predict(dataset, all_distances, all_distances_sorted, j, k,
                                          window_size)  # nn c
                    f_with_diff_window[n - 1] = get_f1(dataset, res, len(target_vals))  # O(nk)
                    steps[n - 1] = window_size
                for f in f_with_diff_window:
                    if f > max_f:
                        max_i = i
                        max_j = j
                        max_k = k
                        max_f = f
                        max_fs = f_with_diff_window
                        max_steps = steps
    plt.plot(max_steps, max_fs)
    plt.title("distance=" + distance.get_distance_name(max_i) + "\nkernel=" + get_kernel_name(
        j) + "\nwindow=" + get_window_name(k))
    plt.show()

# predict.py

from kernel import get_kernel
from window import get_window_size


def get_max_distance(all_distances):
    max_distance = 0.0
    for i in range(len(all_distances)):
        max_distance = max(max_distance, all_distances[i][-1])
    return max_distance


def predict(dataset, all_distances, all_distances_sorted, kernel_index, window_index, window_size):
    eps = 1e-12
    answers = [0.0] * len(dataset)
    for target_index in range(len(dataset)):  # n ^2 * c
        final_target = [0.0] * 4
        avg = [0.0] * 4
        real_window_size = get_window_size(all_distances_sorted, window_index, target_index, window_size) + eps
        for current_index in range(len(dataset)):  # n
            if current_index == target_index:
                continue
            current_distance = all_distances[target_index][current_index]
            current_kernel = get_kernel(kernel_index, current_distance / real_window_size)
            if current_kernel != 0:
                for j in range(4):
                    final_target[-(j + 1)] += current_kernel * dataset[current_index][-(j + 1)]
                    avg[-(j + 1)] += dataset[current_index][-(j + 1)]
        maxIndex = 0
        maxAvgIndex = 0
        sum = 0
        for j in range(4):
            sum += final_target[j]
            if final_target[j] > final_target[maxIndex]:
                maxIndex = j
            if avg[j] > avg[maxAvgIndex]:
                maxAvgIndex = j
        if (sum == 0):  # 0 elements in window
            answers[target_index] = maxAvgIndex
        else:
            answers[target_index] = maxIndex
    return answers

# train.py

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

# distance.py

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

# kernel.py
def uniform_kernel(u):
    return 1 / 2 if abs(u) <= 1 else 0


def triangular_kernel(u):
    return (1 - abs(u)) if abs(u) <= 1 else 0


def epanechnikov_kernel(u):
    return 3 / 4 * (1 - u ** 2) if abs(u) <= 1 else 0


def quartic_kernel(u):
    return 15 / 16 * (1 - u ** 2) ** 2 if abs(u) <= 1 else 0


kernels_names = ["Uniform", "Triangular", "Epanechnikov", "Quartic"]
kernels = [uniform_kernel, triangular_kernel, epanechnikov_kernel, quartic_kernel]


def get_kernel_name(index):
    return kernels_names[index]


def get_kernels_amount():
    return len(kernels)


def get_kernel(index, u):
    return kernels[index](u)

# window.py


def fixed_window_size(all_distances_sorted, target_index, window_size):
    return window_size


def dynamic_window_size(all_distances_sorted, target_index, window_size):
    return all_distances_sorted[target_index][window_size ]


windows_names = ["Fixed", "Dynamic"]
windows = [fixed_window_size, dynamic_window_size]


def get_window_name(index):
    return windows_names[index]


def get_window_size(all_distances_sorted, window_index, target_index, window_size):
    return windows[window_index](all_distances_sorted, target_index, window_size)


def get_windows_amount():
    return len(windows)


def get_steps_amount(dataset_length):
    return int(dataset_length ** 0.5)


def dynamic_step(dataset_length, max_distance):
    return 1


def fixed_step(dataset_length, max_distance):
    return max_distance / (dataset_length ** 0.5)


steps = [fixed_step, dynamic_step]


def get_step(index, dataset_length, max_distance):
    return steps[index](dataset_length, max_distance)

# f.py
def f1(recall, prec):
    return (prec * recall / (prec + recall) * 2) if (prec + recall != 0) else 0


def get_f1(dataset, res, unique_val_amount):
    cm = [] * unique_val_amount
    for j in range(unique_val_amount):
        cm.append([0] * unique_val_amount)
    for i in range(len(res)):
        real_res_index = 0
        for j in range(unique_val_amount):
            if dataset[i][-(j + 1)] != 0:
                real_res_index = unique_val_amount - j - 1
                break
        cm[res[i]][real_res_index] += 1
    microf = 0
    all = 0
    for i in range(unique_val_amount):
        fn = 0
        fp = 0
        c = 0
        tp = cm[i][i]
        for j in range(unique_val_amount):
            all += cm[i][j]
            if (i != j):
                fn += cm[i][j]
                fp += cm[j][i]
            c += cm[i][j]
        tn = all - tp - fp - fn
        f = 0
        if tp == 0 and fn != 0 and fp != 0:
            f = 0
        elif tp + fn == 0 or tp + fp == 0:
            f = 1
        else:
            recall = tp / (tp + fn)
            prec = tp / (tp + fp)
            f = f1(recall, prec)
            microf += f * c
    microf = microf / all
    return microf
