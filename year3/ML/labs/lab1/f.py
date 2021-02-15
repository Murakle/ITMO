def f1(recall, prec):
    return (prec * recall / (prec + recall) * 2) if (prec + recall != 0) else 0


def get_f1(dataset, res, unique_val_amount):
    cm = [] * unique_val_amount
    for j in range(unique_val_amount):
        cm.append([0] * unique_val_amount)
    for i in range(len(res)):
        real_res_index = 0
        for j in range(unique_val_amount):
            if dataset[i][-(j + 1)] != 0:
                real_res_index = unique_val_amount - j - 1
                break
        cm[res[i]][real_res_index] += 1
    microf = 0
    all = 0
    for i in range(unique_val_amount):
        fn = 0
        fp = 0
        c = 0
        tp = cm[i][i]
        for j in range(unique_val_amount):
            all += cm[i][j]
            if (i != j):
                fn += cm[i][j]
                fp += cm[j][i]
            c += cm[i][j]
        tn = all - tp - fp - fn
        f = 0
        if tp == 0 and fn != 0 and fp != 0:
            f = 0
        elif tp + fn == 0 or tp + fp == 0:
            f = 1
        else:
            recall = tp / (tp + fn)
            prec = tp / (tp + fp)
            f = f1(recall, prec)
            microf += f * c
    microf = microf / all
    return microf
