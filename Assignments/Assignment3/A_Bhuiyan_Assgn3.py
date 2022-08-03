# CSCI 323/700
# Summer 2022
# Assignment 3 - Empirical Performance of Matrix Multiplication
# Akil Bhuiyan

# Imports
import numpy as np
import random
import time
from tabulate import tabulate
import pandas as pd
import matplotlib.pyplot as plt
asgnNum = 3


def print_matrix(matrix):
    print('\n'.join([''.join(['{:4}'.format(item) for item in row])for row in matrix]) + "\n")


def random_matrix(mn, mx, rows, cols):
    matrix = [[random.randint(mn, mx) for col in range(0, cols)] for row in range(0, rows)]
    return np.array(matrix)


def native_mult(m1, m2):
    return np.dot(m1, m2)

# From https://www.geeksforgeeks.org/c-program-multiply-two-matrices/
def simple_mult(m, n):
    rows = len(m)
    cols = len(n[0])
    temp = [[0 for x in range(cols)]for y in range(rows)]
    for i in range(rows):
        for j in range(cols):
            temp[i][j] = 0
            for x in range(cols):
                temp[i][j] += m[i][x] * m[x][j]
    return temp

# Ref https://www.geeksforgeeks.org/strassens-matrix-multiplication/
# From https://www.interviewbit.com/blog/strassens-matrix-multiplication/
def strassen_mult(m1, m2):
    if len(m1) == 1 or len(m2) == 1:
        return m1 * m2
    n = m1.shape[0]
    if n % 2 == 1:
        m1 = np.pad(m1, (0, 1), mode='constant')
        m2 = np.pad(m2, (0, 1), mode='constant')
    m = int(np.ceil(n / 2))
    a = m1[: m, : m]
    b = m1[: m, m:]
    c = m1[m:, : m]
    d = m1[m:, m:]
    e = m2[: m, : m]
    f = m2[: m, m:]
    g = m2[m:, : m]
    h = m2[m:, m:]
    p1 = strassen_mult(a, f - h)
    p2 = strassen_mult(a + b, h)
    p3 = strassen_mult(c + d, e)
    p4 = strassen_mult(d, g - e)
    p5 = strassen_mult(a + d, e + h)
    p6 = strassen_mult(b - d, g + h)
    p7 = strassen_mult(a - c, e + f)
    result = np.zeros((2 * m, 2 * m), dtype=np.int32)
    result[: m, : m] = p5 + p4 - p2 + p6
    result[: m, m:] = p1 + p2
    result[m:, : m] = p3 + p4
    result[m:, m:] = p1 + p5 - p3 - p7
    return result[: n, : n]

def plot_time(dict_matrixLst, sizes, matrixLst, trials):
    x_num = 0
    plt.xticks([j for j in range(len(sizes))], [str(size) for size in sizes])
    for matrixLst in matrixLst:
        x_num += 1
        d = dict_matrixLst[matrixLst.__name__]
        x_axis = [j + 0.05 * x_num for j in range(len(sizes))]
        y_axis = [d[i] for i in sizes]
        plt.bar(x_axis, y_axis, width=0.05, alpha=1, label=matrixLst.__name__)
    plt.legend()
    plt.title("Run Time of Matrix Multiplication")
    plt.xlabel("Size of Matrix")
    plt.ylabel(f"Time for {trials} trial (ms)")
    plt.savefig(f"Assignments/Assignment{asgnNum}/Assignment{asgnNum}.png")
    plt.show()

def matt(mn, nx, rows, cols):
    matrix = [[1 for col in range(0, cols)] for row in range(0, rows)]
    return np.array(matrix)

def main():
    #sizes = [10, 100, 1000, 10000]
    sizes = [10*i for i in range(1, 11)]
    trials = 1
    matrixLst = [native_mult, simple_mult, strassen_mult]
    dict_matrixLst= {}
    for x in matrixLst:
        dict_matrixLst[x.__name__] = {}
    for size in sizes:
        for x in matrixLst:
            dict_matrixLst[x.__name__][size] = 0
        for trial in range(1, trials + 1):
            m1 = matt(-1, 1, size, size)
            m2 = matt(-1, 1, size, size)
            #m1 = random_matrix(-1, 1, size, size)
            #m2 = random_matrix(-1, 1, size, size)
            for x in matrixLst:
                start_time = time.time()
                m3 = x(m1, m2)
                end_time = time.time()
                net_time = end_time - start_time
                dict_matrixLst[x.__name__][size] += 1000 * net_time
    pd.set_option("display.max_rows", 500)
    pd.set_option("display.max_columns", 500)
    pd.set_option("display.width", 1000)
    df = pd.DataFrame.from_dict(dict_matrixLst).T
    #print(df)
    print(tabulate(df, headers='keys', tablefmt='psql'))
    plot_time(dict_matrixLst, sizes, matrixLst, trials)


if __name__ == "__main__":
    main()
