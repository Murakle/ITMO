import math
import sys


def p_Laplas(Nx, Nk, All, a):
    return math.log(Nx + a) - math.log(Nk + a * All)


def p_r_Laplas(Nx, Nk, All, a):
    return math.log(Nk + a * All - (Nx + a)) - math.log(Nk + a * All)


def getOccurence(word, occurence, c_class, c_train):
    result = 0
    for i in range(len(occurence)):
        if (c_train[i] == c_class):
            result += word in occurence[i]
    return result


def sumOfLog(L):
    M = 0
    for p in range(len(L)):
        if (L[M] < L[p]):
            M = p
    s = 0
    for p in range(len(L)):
        c = math.exp(L[p] - L[M])
        s += c
    return L[M] + math.log(s)


def join_parts(n_data, test_part):
    messages = []
    legit = []
    for i in range(len(n_data)):
        if (i != test_part):
            for msg in n_data[i][0]:
                messages.append(msg)
            for l in n_data[i][1]:
                legit.append(l)
    return [messages, legit]


def bayes(n_data, a, test_part, h_legit):
    k = 2  # classes
    h = [1.0, h_legit]
    data = join_parts(n_data, test_part)
    all_messages = data[0]
    n = len(all_messages)
    c_train = data[1]  # real class legit/spam
    p_class = [0] * k  # amount of msg with class i
    word_dict = [dict(), dict()]  # dict of words {word:amount of occ}
    word_set = set()
    for i in range(n):
        msg = all_messages[i]
        l = len(msg)
        p_class[c_train[i]] += 1
        word_list = set()
        for j in range(l):
            word_set.add(msg[j])
            word_list.add(msg[j])
        for word in word_list:
            if word in word_dict[c_train[i]]:
                word_dict[c_train[i]][word] += 1
            else:
                word_dict[c_train[i]][word] = 1
    word_list = list(word_set)
    words_amount = len(word_list)
    laplases_dict = [] * k
    r_laplases_dict = [] * k
    sum_r_laplases = [0.0] * k
    for j in range(k):
        laplases_dict.append({})
        r_laplases_dict.append({})
        for o in range(words_amount):
            c_word = word_list[o]
            nx = 0
            if c_word in word_dict[j]:
                nx = word_dict[j][c_word]
            laplas = p_Laplas(nx, p_class[j], 2, a)
            r_laplas = p_r_Laplas(nx, p_class[j], 2, a)
            laplases_dict[j][c_word] = laplas
            r_laplases_dict[j][c_word] = r_laplas
            sum_r_laplases[j] += r_laplas
    m = len(n_data[test_part][0])
    occurrence_test = [] * m
    for i in range(m):
        msg = n_data[test_part][0][i]
        l = len(msg)
        occurrence_test.append(set())
        for j in range(l):
            occurrence_test[i].add(msg[j])
    result = [[0, 0], [0, 0]]
    for i in range(m):
        p = [0.0] * k
        sum = 0.0
        real_legit = n_data[test_part][1][i]
        for j in range(k):
            p[j] = math.log(h[j] * p_class[j] / n)
            p[j] += sum_r_laplases[j]
            test_word_list = list(occurrence_test[i])
            for o in range(len(test_word_list)):
                c_word = test_word_list[o]
                if c_word in r_laplases_dict[j]:
                    p[j] -= r_laplases_dict[j][c_word]
                    p[j] += laplases_dict[j][c_word]
        sum = sumOfLog(p)
        my_legit = 0
        max_legit = 0
        for j in range(k):
            res = math.exp(p[j] - sum)
            if (res > max_legit):
                max_legit = res
                my_legit = j
        result[real_legit][my_legit] += 1
    return result
