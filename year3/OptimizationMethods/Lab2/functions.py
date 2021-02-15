import math
import numpy as np


# 100 * (x2 −x1 ^ 2) ^ 2 +(1−x1) ^ 2
# min = 0 at (1, 1)
def f1(x):
    return 100 * (x[1] - x[0] ** 2) ** 2 + (1 - x[0]) ** 2


# (x2 −x1 ^ 2) ^ 2 +(1−x1) ^ 2
# min = 0 at (1, 1)
def f2(x):
    return (x[1] - x[0] ** 2) ** 2 + (1 - x[0]) ** 2;


# (1.5−x1(1−x2))^2+ (2.25−x1(1−x2^2))^2+ (2.625−x1(1−x2^3))^2
# min = 0 at (3, 0.5)
def f3(x):
    return (1.5 - x[0] * (1 - x[1])) ** 2 + (2.25 - x[0] * (1 - x[1] ** 2)) ** 2 + (2.625 - x[0] * (1 - x[1] ** 3)) ** 2


# min = 0 at (0, 0, 0, 0)
def f4(x):
    return (x[0] + x[1]) ** 2 + 5 * (x[2] - x[3]) ** 2 + (x[1] - 2 * x[2]) ** 4 + 10 * (x[0] - x[3]) ** 4


def f1dx0(x):
    return 2 * (200 * x[0] ** 3 - 200 * x[0] * x[1] + x[0] - 1)


def f1dx1(x):
    return 200 * (x[1] - x[0] ** 2)


def f2dx0(x):
    return 2 * (2 * x[0] ** 3 - 2 * x[0] * x[1] + x[0] - 1)


def f2dx1(x):
    return 2 * (x[1] - x[0] ** 2)


def f3dx0(x):
    return -12.75 + 3 * x[1] + 4.5 * x[1] ** 2 + 5.25 * x[1] ** 3 + 2 * x[0] * \
           (3 - 2 * x[1] - x[1] ** 2 - 2 * x[1] ** 3 + x[1] ** 4 + x[1] ** 6)


def f3dx1(x):
    return x[0] * \
           (3 + 9 * x[1] + 15.75 * x[1] ** 2 + x[0] * (-2 - 2 * x[1] - 6 * x[1] ** 2 + 4 * x[1] ** 3 + 6 * x[1] ** 5))


def f4dx0(x):
    return 2 * (x[0] + x[1] + 20 * (x[0] - x[3]) ** 3)


def f4dx1(x):
    return 2 * (x[0] + x[1] + 2 * (x[1] - 2 * x[2]) ** 3)


def f4dx2(x):
    return -8 * (x[1] - 2 * x[2]) ** 3 + 10 * (x[2] - x[3])


def f4dx3(x):
    return 10 * (-x[2] - 4 * (x[0] - x[3]) ** 3 + x[3])


functions = [f1, f2, f3, f4]
derivatives = [[f1dx0, f1dx1],
               [f2dx0, f2dx1],
               [f3dx0, f3dx1],
               [f4dx0, f4dx1, f4dx2, f4dx3]]
realMin = [
    [1, 1], [1, 1], [3, 0.5], [0, 0, 0, 0]
]


def getFunctionsAmount():
    return len(functions)


# index - index of function [0;4]
def getF(x, index):
    return functions[index](x)


# returns amount of axis(dimensions)
def getF_dimension(index):
    return len(derivatives[index])


# returns array of derivatives
def getFd(x, index):
    n = getF_dimension(index)
    c_derivatives = np.empty(n)
    for i in range(n):
        c_derivatives[i] = derivatives[index][i](x)
    return c_derivatives


def getRealMin(index):
    return realMin[index]

def get_distance_to_real_min(index, x):
    sum = 0
    for i in range(len(x)):
        sum += (x[i] - realMin[index][i]) ** 2
    return math.sqrt(sum)