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
