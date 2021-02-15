from distance import get_distance
def rand_index(klasters, dataset):
    n = len(dataset)
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    for i in range(n):
        for j in range(n):
            if dataset[i][0] == dataset[j][0]:
                if klasters[i] == klasters[j]:
                    tp+=1
                else:
                    fp+=1
            else:
                if klasters[i] == klasters[j]:
                    tn+=1
                else:
                    fn+=1
    #unique_vals = list(get_unique_values(dataset.values))
    return (tp + fn) / (tp + tn + fp + fn)


def silhouette(k, klasters, dataset, distance_index):
    # split to clasters
    n = len(klasters)
    indicies = [] * k
    for i in range(k):
        row = [] * k
        indicies.append(row)
    for i in range(n):
        indicies[klasters[i]].append(i)
    res = 0
    for i in range(k):
        if len(indicies[i]) == 0:
            continue
        for j in indicies[i]:
            a = 0
            for h in indicies[i]:
                d = get_distance(distance_index, dataset[j], dataset[h])
                a += d
            a /= len(indicies[i])
            b = 1e9
            for p in range(k):
                if p != i and len(indicies[p]) != 0:
                    bb = 0
                    for h in indicies[p]:
                        d = get_distance(distance_index, dataset[j], dataset[h])
                        bb += d
                    bb /= len(indicies[p])
                    b = min(b, bb)
            res += (b - a) / max(a, b)
    res /= n
    return res
