from ngramm import ngramm
from read_data import read_data
from bayes import bayes
from matplotlib import pyplot as plt
import itertools


def get_ngramm(text: str, n: int):
    current_words = [] * n
    all_words = text.split()
    ngramms = []
    start_index = 1  # remove "Subject:" word
    for i in range(start_index, n + start_index):
        current_words.append(int(all_words[i]))
    for i in range(n + start_index, len(all_words)):
        ngramms.append(ngramm(current_words.copy()))
        current_words.pop(0)
        current_words.append(int(all_words[i]))
    ngramms.append(ngramm(current_words.copy()))
    return ngramms


def get_f1(tp, fp, fn, tn):
    return tp / (tp + (fp + fn) / 2)


def get_tpr(tp, fp, fn, tn):
    return tp / (tp + fn)


def get_fpr(tp, fp, fn, tn):
    return 1 - tn / (tn + fp)


if __name__ == '__main__':
    data = read_data()  # part i -> msg, legit
    mina = 0.1
    max_n = 3
    a_array = [1e-3, 1e-2, 1e-1, 1e-0]
    a_amount = len(a_array)
    f = [] * max_n
    tpr = []
    fpr = []
    '''
    for n in range(1, max_n + 1):
        n_data = []
        for i in range(len(data)):
            ngramms = []
            for j in range(len(data[i][0])):
                msg = data[i][0][j]
                ngramms.append(get_ngramm(msg, n))
            n_data.append([ngramms, data[i][1]])
        f.append([0.0] * a_amount)
        for a_index in range(a_amount):
            a = a_array[a_index]
            print("a =", a, ", n =", n)
            f_res = [[0, 0], [0, 0]]
            for test_part in range(10):
                res = bayes(n_data, a, test_part, 1)
                for q in range(2):
                    for w in range(2):
                        f_res[q][w] += res[q][w]
            c_f = get_f1(f_res[0][0], f_res[0][1], f_res[1][0], f_res[1][1])
            f[n - 1][a_index] = c_f
            tpr.append(get_tpr(f_res[0][0], f_res[0][1], f_res[1][0], f_res[1][1]))
            fpr.append(get_fpr(f_res[0][0], f_res[0][1], f_res[1][0], f_res[1][1]))
            print(f_res)
        plt.plot(a_array, f[n - 1])
        plt.title("n =" + str(n))
        plt.show()
    # '''
    # '''
    best_a = 0.001
    best_n = 3
    hh = [ 1e5, 1e6, 1e7, 1e8]
    n_data = []
    for i in range(len(data)):
        ngramms = []
        for j in range(len(data[i][0])):
            msg = data[i][0][j]
            ngramms.append(get_ngramm(msg, best_n))
        n_data.append([ngramms, data[i][1]])

    for h in hh:
        print(h)
        f_res = [[0, 0], [0, 0]]
        for test_part in range(10):
            res = bayes(n_data, best_a, test_part, h)
            for q in range(2):
                for w in range(2):
                    f_res[q][w] += res[q][w]
        tpr.append(get_tpr(f_res[0][0], f_res[0][1], f_res[1][0], f_res[1][1]))
        fpr.append(get_fpr(f_res[0][0], f_res[0][1], f_res[1][0], f_res[1][1]))
        print(f_res)
    # '''
    # fpr.append(0.0)
    # tpr.append(0.0)
    # fpr.append(1.0)
    # tpr.append(1.0)
    new_fpr, new_tpr = zip(*sorted(zip(fpr, tpr)))
    plt.plot(new_fpr, new_tpr)
    plt.title("ROC")
    plt.show()
    # '''
