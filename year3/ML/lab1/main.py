import math
import sys


def p_Laplas(Nx, Nk, All, a):
    return math.log(Nx + a) - math.log(Nk + a * All)


def p_r_Laplas(Nx, Nk, All, a):
    return math.log(Nk + a * All - (Nx + a)) - math.log(Nk + a * All)


def getOccurence(word, occurence, c_class, c_train):
    result = 0
    for i in range(len(occurrence)):
        if (c_train[i] == c_class):
            result += word in occurrence[i]
    return result


def sumOfLog(L, zeroes):
    M = 0
    amountOfZeroes = 0
    for p in range(len(L)):
        if (not zeroes[p] and L[M] < L[p]):
            M = p
        if (zeroes[p]):
            amountOfZeroes+=1
    s = 0
    for p in range(len(L)):
        if (not zeroes[p]):
            c = math.exp(L[p] - L[M])
            s += c
    return L[M] + math.log(s)


if __name__ == '__main__':
    # sys.stdout = open('/Users/user/dev/ITMO/year3/ML/labs/lab3/output.txt', 'w')
    # sys.stdin = open('/Users/user/dev/ITMO/year3/ML/codeforces/input.txt', 'r')
    k = int(input())
    h = [0] * k
    h = input().split(' ')
    for i in range(k):
        h[i] = int(h[i])
    a = int(input())
    n = int(input())
    c_train = [0] * n
    w_train = [] * n
    p_class = [0] * k
    word_set = set()
    occurrence = [] * n
    for i in range(n):
        occurrence.append(set())
        row = input().split(' ')
        c_train[i] = int(row[0])
        l = int(row[1])
        w_train.append([""] * l)
        p_class[c_train[i] - 1] += 1
        for j in range(l):
            w_train[i][j] = row[2 + j]
            occurrence[i].add(w_train[i][j])
            word_set.add(w_train[i][j])
    word_list = list(word_set)
    word_list.sort()
    laplases = [] * k
    r_laplases = [] * k
    for j in range(k):
        laplases.append([0.0] * len(word_list))
        r_laplases.append([0.0] * len(word_list))
        for o in range(len(word_list)):
            c_word = word_list[o]
            nx = getOccurence(c_word, occurrence, j + 1, c_train)
            laplases[j][o] = p_Laplas(nx, p_class[j], 2, a)
            r_laplases[j][o] = p_r_Laplas(nx, p_class[j], 2, a)

    m = int(input())
    w_test = [] * m
    occurrence_test = [] * m
    for i in range(m):
        row = input().split(' ')
        l = int(row[0])
        occurrence_test.append(set())
        w_test.append([""] * l)
        for j in range(l):
            w_test[i][j] = row[1 + j]
            occurrence_test[i].add(w_test[i][j])
    for i in range(m):
        p = [0.0] * k
        zeroes = [False] * k
        sum = 0.0
        for j in range(k):
            if (p_class[j] != 0):
                p[j] = math.log(p_class[j]) - math.log(n)
                for o in range(len(word_list)):
                    c_word = word_list[o]
                    adder = 0
                    if (c_word in occurrence_test[i]):
                        adder = laplases[j][o]
                    else:
                        adder = r_laplases[j][o]
                    p[j] += adder
                p[j] += math.log(h[j])
            else:
                zeroes[j] = True
        sum = sumOfLog(p, zeroes)
        for j in range(k):
            if(zeroes[j]):
                print(0.0, end=' ')
            else:
                res = p[j] - sum
                print(math.exp(res), end=' ')
        print()