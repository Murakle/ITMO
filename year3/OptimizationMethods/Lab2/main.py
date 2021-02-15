import methods
import functions
import matplotlib.pyplot as plt
import sys

methods_names = ["Покоординатный", "Наискорейший"]

if __name__ == '__main__':
    functionsAmount = functions.getFunctionsAmount()
    epsAmount = 6 # 7
    distanseAmount = 6
    answers = [] * distanseAmount
    methods_amount = methods.getMethodsAmount()
    x = [0.0] * epsAmount
    original_stdout = sys.stdout
    # print(methods.brent(3, 1e-7, True))
    start_point = [-0.2, -0.2, -0.2, -0.2]

    with open('method_output.txt', 'w+') as f:
        sys.stdout = f
        eps = 0.1 ** 4
        for j in range(0, distanseAmount): #, epsAmount + 1):
            x[j] = start_point[0]
            matrix = [] * (functionsAmount)
            # print(eps)
            for i in range(0, functionsAmount):
                row = [] * methods_amount
                for k in range(methods_amount):
                    res = methods.getM(k, i, 1000000, eps, start_point)
                    while (res[1] > 1000000):
                        res = methods.getM(k, i, 1000000, eps, start_point)
                    row.append(res)
                    # print(row)
                print("Func " + str(i) + " eps=" + str(eps))
                print(row)
                matrix.append(row)
            answers.append(matrix)
            for i in range(4):
                start_point[i] = -0.2 * (j + 2)
        sys.stdout = original_stdout
    print(x)
    # for i in range(methods_amount - 1):
    #     print(methods.getMethodName(i))
    #     for j in range(functions_amount):
    #         result, calls = methods.getM(i, j, 1000000, 1e-6)
    #         print(result, calls, functions.get_distance_to_real_min(j, result))
    for k in range(0, methods_amount):
        for i in range(0, functionsAmount):
            y = [0.0] * distanseAmount
            for j in range(distanseAmount ):
                y[j] = answers[j][i][k][1]
            l = 'f' + str(i + 1)
            plt.plot(x, y, marker='o', label=l)
        plt.xlabel('Xi')
        plt.ylabel('Количество вызовов функции')
        plt.title('Метод ' + methods_names[k])
        plt.legend()
        plt.show()
    # 1
    for k in range(0, methods_amount):
        y = [0.0] * epsAmount
        for j in range(distanseAmount):
            sum = 0
            for i in range(0, functionsAmount):
                sum += answers[j][i][k][1] #** 2
            # y[j - 1] = sqrt(sum/ functionsAmount)
            y[j - 1] = sum / functionsAmount
        plt.plot(x, y, marker='o', label='Метод ' + methods_names[k])
    plt.xlabel('Xi')
    # plt.yscale('log', basey=2)
    plt.ylabel('Средне количество вызовов функции')
    plt.title('График зависимости среднего количества \nвызовов функции от начальной точки')
    plt.legend()
    plt.show()
    # '''

