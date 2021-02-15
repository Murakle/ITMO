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
        for j in range(0, get_kernels_amount()):
            for k in range(0, get_windows_amount()):
                print(i * get_kernels_amount() * get_windows_amount() + j * get_windows_amount() + k, end=" / ")
                print(distances_amount * get_kernels_amount() * get_windows_amount())
                f_with_diff_window = [0.0] * steps_amount
                steps = [0.0] * steps_amount
                current_step = get_step(k, dataset_length, max_distance)
                for n in range(1, steps_amount + 1):
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
