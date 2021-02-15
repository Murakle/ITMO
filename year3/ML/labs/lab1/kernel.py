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
