def f1(recall, prec):
    return (prec * recall / (prec + recall) * 2) if (prec + recall != 0) else 0

k = int(input())
cm = []
all = 0
for i in range(k):
    row = input().split()
    for j in range(len(row)):
        row[j] = int(row[j])
        all += row[j]
    cm.append(row)
tp = [0] * k
fp = [0] * k
fn = [0] * k
tn = [0] * k
c = [0] * k
p = [0] * k
for i in range(k):
    tp[i] = cm[i][i]
    for j in range(k):
        if (i != j):
            fn[i] += cm[i][j]
            fp[i] += cm[j][i]
        c[i] += cm[i][j]
        p[j] += cm[i][j]
    tn[i] = all - tp[i] - fp[i] - fn[i]

f = [0] * k
for i in range(k):
    if tp[i] == 0 and fn[i] != 0 and fp[i] != 0:
        f[i] = 0
    elif tp[i] + fn[i] == 0 or tp[i] + fp[i] == 0:
        f[i] = 1
    else:
        recall = tp[i] / (tp[i] + fn[i])
        prec = tp[i] / (tp[i] + fp[i])
        f[i] = f1(recall, prec)
microf = 0
for i in range(k):
    microf += f[i] * c[i]
microf = microf / all
precw = 0
recallw = 0
for i in range(k):
    if p[i] != 0:
        precw += cm[i][i] * c[i] / p[i]
        recallw += cm[i][i]
    # else:
        # precw += c[i]
precw = precw / all
recallw = recallw / all
macroF = f1(recallw, precw)
print(macroF)
print(microf)
