from sklearn import tree
import pandas as pd
from matplotlib import pyplot as plt


def read_file(file_name: str):
    data = pd.read_csv(file_name).values
    return data[:, :-1], data[:, -1:]


def read_data(file_index: int):
    train_file_name = "./DT_csv/" + ("0" if file_index < 10 else "") + str(file_index) + "_train.csv"
    test_file_name = "./DT_csv/" + ("0" if file_index < 10 else "") + str(file_index) + "_test.csv"
    train_X, train_Y = read_file(train_file_name)
    test_X, test_Y = read_file(test_file_name)
    return train_X, train_Y, test_X, test_Y


criterions = ["gini", "entropy"]
splitters = ["best", "random"]
if __name__ == '__main__':
    datasets_amount = 20

    max_h = 20
    d = [k for k in range(1, max_h + 1)]
    best_acc = [0.0] * datasets_amount
    opt_d = [0.0] * datasets_amount
    opt_c = [0] * datasets_amount
    opt_s = [0] * datasets_amount

    acc = [] * datasets_amount
    for i in range(1, datasets_amount + 1):
        print("Processing dataset # " + str(i) + " ...")
        train_X, train_Y, test_X, test_Y = read_data(i)
        for max_depth in range(1, max_h + 1):
            for criterion in criterions:
                for splitter in splitters:
                    clf = tree.DecisionTreeClassifier(max_depth=max_depth, criterion=criterion, splitter=splitter)
                    clf.fit(train_X, train_Y)
                    accuracy = clf.score(test_X, test_Y)
                    if accuracy > best_acc[i - 1]:
                        best_acc[i - 1] = accuracy
                        opt_d[i - 1] = clf.get_depth()
                        opt_c[i - 1] = criterion
                        opt_s[i - 1] = splitter
        # plt.plot(d, acc)
        # plt.show()
    max_d = 0
    min_d = 0
    for i in range(1, datasets_amount + 1):
        if opt_d[i - 1] > opt_d[max_d]:
            max_d = i - 1
        if opt_d[i - 1] < opt_d[min_d]:
            min_d = i - 1
    print("Maximal height of tree on dataset # ", max_d,
          " with height = ", opt_d[max_d],
          " splitter = ", opt_s[max_d],
          " criterion = ", opt_c[max_d])
    print("Minimal height of tree on dataset # ", min_d,
          " with height = ", opt_d[min_d],
          " splitter = ", opt_s[min_d],
          " criterion = ", opt_c[min_d])
    # plt.plot(d, acc[min_d], 'o-', label="minimal optimal depth (test_dataset)")
    # plt.plot(d, acc[max_d], 'o-', label="maximal optimal depth (test_dataset)")
    # MIN test
    train_X, train_Y, test_X, test_Y = read_data(min_d)
    acc = [0.0] * max_h
    for max_depth in range(1, max_h + 1):
        clf = tree.DecisionTreeClassifier(max_depth=max_depth, criterion=opt_c[min_d], splitter=opt_s[min_d])
        clf.fit(train_X, train_Y)
        accuracy = clf.score(test_X, test_Y)
        acc[max_depth - 1] = accuracy
    plt.plot(d, acc, 'o-', label="minimal optimal depth (test_dataset)")
    # MIN train
    acc = [0.0] * max_h
    for max_depth in range(1, max_h + 1):
        clf = tree.DecisionTreeClassifier(max_depth=max_depth, criterion=opt_c[min_d], splitter=opt_s[min_d])
        clf.fit(train_X, train_Y)
        accuracy = clf.score(train_X, train_Y)
        acc[max_depth - 1] = accuracy
    plt.plot(d, acc, 'o-', label="minimal optimal depth (train_dataset)")

    # MAX tst
    train_X, train_Y, test_X, test_Y = read_data(max_d)
    acc = [0.0] * max_h
    for max_depth in range(1, max_h + 1):
        clf = tree.DecisionTreeClassifier(max_depth=max_depth, criterion=opt_c[max_d], splitter=opt_s[max_d])
        clf.fit(train_X, train_Y)
        accuracy = clf.score(test_X, test_Y)
        acc[max_depth - 1] = accuracy
    plt.plot(d, acc, 'o-', label="maximal optimal depth (test_dataset)")
    # MAX train
    acc = [0.0] * max_h
    for max_depth in range(1, max_h + 1):
        clf = tree.DecisionTreeClassifier(max_depth=max_depth, criterion=opt_c[max_d], splitter=opt_s[max_d])
        clf.fit(train_X, train_Y)
        accuracy = clf.score(train_X, train_Y)
        acc[max_depth - 1] = accuracy
    plt.plot(d, acc, 'o-', label="maximal optimal depth (train_dataset)")
    plt.legend(loc='lower right', shadow=False)
    plt.set(xlabel="Accuracy", ylabel="Depth", title="Result")
    plt.show()
