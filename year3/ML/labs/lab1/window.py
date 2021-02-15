
def fixed_window_size(all_distances_sorted, target_index, window_size):
    return window_size


def dynamic_window_size(all_distances_sorted, target_index, window_size):
    return all_distances_sorted[target_index][window_size]  # todo is +1?


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
