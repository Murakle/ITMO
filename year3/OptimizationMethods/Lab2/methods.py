import functions
import math
import numpy as np
import functions
import random


def print_with_tabs(*arg):
    for a in arg:
        print(str(a).replace(".", ","), end="\t")
    print("")


def norm(x):
    sum = 0
    for i in range(len(x)):
        sum += x[i] ** 2
    return math.sqrt(sum)


"""
   :arg     index - index of function [0;4], eps - accuracy, beta < eps/2
   :return  { center of interval of length eps, amount of F calls}
"""


def сoordinate_descent(func_index, max_iter, eps, start_point):
    n = functions.getF_dimension(func_index)
    x = start_point
    step = 1
    cf = functions.getF(x, func_index)
    func_calls = 1
    while (func_calls < max_iter):
        j = random.randint(0, n -1 )
        d = functions.getFd(x, func_index)
        func_calls += n
        if (norm(d) < eps):
            return x, func_calls
        c = step
        next_x = np.copy(x)
        next_x[j] = x[j] - d[j] * c
        next_f = functions.getF(next_x, func_index)
        func_calls += 1
        while (next_f >= cf):
            if (c < 1e-9):
                next_x = np.copy(x)
                for i in range(n):
                    next_x[i] += (random.random() * 2 - 1) * eps
                break
            c /= 2
            next_x[j] = x[j] - d[j] * c
            next_f = functions.getF(next_x, func_index)
            func_calls += 1
        x = next_x
        cf = next_f
    return x, func_calls


def fastest_descent(func_index, max_iter, eps, start_point):
    n = functions.getF_dimension(func_index)
    x = start_point[0:n]
    cf = functions.getF(x, func_index)
    func_calls = 1
    while (func_calls < max_iter):
        # a = functions.getF(x, func_index)
        # print(a)
        d = functions.getFd(x, func_index)
        func_calls += n
        if (norm(d) < eps):
            break
        c, calls = golden_ratio(func_index, 1e-6, x, d)
        func_calls += calls
        if (c < 1e-9):
            for i in range(n):
                x[i] += (random.random() * 2 - 1) * eps
        else:
            x = x - d * c
    return x, func_calls


def conjugate_descent(func_index, max_iter, eps):
    n = functions.getF_dimension(func_index)
    x = np.ones((n))
    x *= -1
    k = 0
    grad = functions.getFd(x, func_index)
    func_calls = n
    p = -grad
    while (func_calls < max_iter):
        alpha, calls = golden_ratio(func_index, eps, x, -p)
        func_calls += calls
        a = functions.getF(x, func_index)
        # print(x, -p, alpha, calls, a)
        if (alpha < 1e-6):
            for i in range(n):
                x[i] += random.random() * 2 - 1
            grad = functions.getFd(x, func_index)
            p = -grad
            k = 0
            continue
        next_x = x + alpha * p
        next_grad = functions.getFd(next_x, func_index)
        func_calls += n
        if (norm(next_grad) < eps):
            x = next_x
            break
        if (k + 1 == n):
            k = 0
            x = next_x
            grad = next_grad
            p = -next_grad
            continue
        beta = norm(next_grad) ** 2 / (norm(grad) ** 2)
        next_p = -next_grad + beta * p
        x = next_x
        p = next_p
        grad = next_grad
        k += 1
    return x, func_calls


def golden_ratio(index, eps, start, direction):
    a = 0
    b = 1
    A = start
    B = start - direction * b
    c = (math.sqrt(5) - 1) / 2
    x2 = a + c * (b - a)
    x1 = b - c * (b - a)
    X1 = start - direction * x1
    X2 = start - direction * x2
    f1 = functions.getF(X1, index)
    f2 = functions.getF(X2, index)
    function_calls = 2
    while b - a > eps:
        if x1 > x2:
            x1, x2 = x2, x1
            X1, X2 = X2, X1
            f1, f2 = f2, f1
        if f1 > f2:
            a = x1
            x1 = x2
            f1 = f2
            x2 = b - (x1 - a)
            if b - a <= eps:
                break
            X2 = start - direction * x2
            f2 = functions.getF(X2, index)
            function_calls += 1
        else:
            b = x2
            x2 = x1
            f2 = f1
            x1 = a + (b - x2)
            if b - a <= eps:
                break
            X1 = start - direction * x1
            f1 = functions.getF(X1, index)
            function_calls += 1
    return (a + b) / 2, function_calls
    # return function_calls


def change(constants, index_of_non_constant, value):
    vals = [0.0] * len(constants)
    vals = [constants[i] for i in range(len(constants))]
    vals[index_of_non_constant] = value
    return vals


def brent_method_1d(func_index, max_iter, eps, index_of_non_constant, a, b, constants):  # todo vector brent_method
    A = change(constants, index_of_non_constant, a)
    B = change(constants, index_of_non_constant, b)
    fa = functions.getFd(A, func_index)[index_of_non_constant]
    fb = functions.getFd(B, func_index)[index_of_non_constant]
    func_calls = 2
    C = A
    c = a
    fc = fa
    mflag = True
    d = 0
    s = 0
    for i in range(max_iter):
        if (b - a < eps):
            break
        if (fa != fc and fb != fc):
            s = a * fb * fc / ((fa - fb) * (fa - fc)) \
                + b * fa * fc / ((fb - fa) * (fb - fc)) \
                + c * fa * fb / ((fc - fa) * (fc - fb))
        else:
            s = b - fb * (b - a) / (fb - fa)
        if ((s < (3 * a + b) / 4 or s > b)
                or (mflag and abs(b - s) >= abs(b - c) / 2)
                or (not mflag and abs(b - s) >= abs(d - c) / 2)
                or (mflag and abs(b - c) < eps)
                or (not mflag and abs(c - d) < eps)):
            s = (a + b) / 2
            mflag = True
        else:
            mflag = False
        S = change(constants, index_of_non_constant, s)
        fs = functions.getFd(S, func_index)[index_of_non_constant]
        func_calls += 1
        d = c
        c = b
        fc = fb
        if (fa * fs < 0):
            b = s
            fb = fs
        else:
            a = s
            fa = fs
    return s, func_calls


methods_list = [сoordinate_descent, fastest_descent] #, conjugate_descent]


def getM(method_index, func_index, max_iter, eps, start_point):
    return methods_list[method_index](func_index, max_iter, eps, start_point)


def getMethodsAmount():
    return len(methods_list)


methodNames = [
    "Coordinate gradient descent", "Fastest gradient descent", "Conjugate gradient descent"
]


def getMethodName(index):
    return methodNames[index]
