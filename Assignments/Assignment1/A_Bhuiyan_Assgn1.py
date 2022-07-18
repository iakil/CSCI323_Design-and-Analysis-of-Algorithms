# CSCI 323/700
# Summer 2022
# Assignment 1 - Search Algorithms
# Akil Bhuiyan

import random
import math
import time
import pandas as pd
import matplotlib.pyplot as plt

def random_list(min_num, max_num, size, do_sort, unique):
    numbers = []
    i = 0
    while i < size:
        rnd = random.randint(min_num, max_num)
        if unique and rnd in numbers:
            continue
        else:
            i += 1
            numbers.append(rnd)
    if do_sort:
        numbers.sort()

    return numbers


def python_search(arr, key):  # native_search --> python_search
    return arr.index(key)


# From https://www.geeksforgeeks.org/linear-search/
def linear_search(arr, key):
    n = len(arr)
    for i in range(0, n):
        if arr[i] == key:
            return i
    return -1


# From https://www.geeksforgeeks.org/binary-search/
def binary_search_recursive(arr, l, r, key):
    if r >= l:
        mid = l + int((r - l) / 2)
        if arr[mid] == key:
            return mid
        elif arr[mid] > key:
            return binary_search_recursive(arr, l, mid - 1, key)
        else:
            return binary_search_recursive(arr, mid + 1, r, key)
    else:
        return -1


def binary_search(arr, key):
    return binary_search_recursive(arr, 0, len(arr) - 1, key)


# From https://www.geeksforgeeks.org/randomized-binary-search-algorithm/
def randomized_binary_search_recursive(arr, l, r, key):
    if r >= l:
        mid = random.randint(l, r)
        if arr[mid] == key:
            return mid
        if arr[mid] > key:
            return randomized_binary_search_recursive(arr, l, mid - 1, key)
        return randomized_binary_search_recursive(arr, mid + 1, r, key)
    return -1


def randomized_binary_search(arr, key):
    return randomized_binary_search_recursive(arr, 0, len(arr) - 1, key)


# From https://www.geeksforgeeks.org/interpolation-search/
def interpolation_search_recursive(arr, l, r, key):

    # Find Divide by zero error (we dont need this part)
    if l == r:
        if arr[l] == key:
            return l
        else:
            return -1

    # interpolation_search_recursive
    if (l <= r) and arr[l] <= key <= arr[r]:
        pos = l + int(((r - l) / (arr[r] - arr[l]) * (key - arr[l])))
        if arr[pos] == key:
            return pos
        if arr[pos] < key:
            return interpolation_search_recursive(arr, pos + 1, r, key)
        if arr[pos] > key:
            return interpolation_search_recursive(arr, l, pos - 1, key)
    return -1


def interpolation_search(arr, key):
    return interpolation_search_recursive(arr, 0, len(arr) - 1, key)


# From https://www.geeksforgeeks.org/jump-search/
def jump_search(arr, key):
    n = len(arr)
    step = math.sqrt(n)
    prev = 0
    while arr[int(min(step, n) - 1)] < key:
        prev = step
        step += math.sqrt(n)
        if prev >= n:
            return -1
    while arr[int(prev)] < key:
        prev += 1
        if prev == min(step, n):
            return -1
    if arr[int(prev)] == key:
        return int(prev)
    return -1


# From https://www.geeksforgeeks.org/fibonacci-search/
def fibonacci_search(arr, key):
    n = len(arr)
    fib_2 = 0
    fib_1 = 1
    fib = fib_2 + fib_1
    while fib < n:
        fib_2 = fib_1
        fib_1 = fib
        fib = fib_2 + fib_1
    offset = -1
    while fib > 1:
        i = min(offset + fib_2, n - 1)
        if arr[i] < key:
            fib = fib_1
            fib_1 = fib_2
            fib_2 = fib - fib_1
            offset = i
        elif arr[i] > key:
            fib = fib_2
            fib_1 = fib_1 - fib_2
            fib_2 = fib - fib_1
        else:
            return i
    if fib_1 and arr[n-1] == key:
        return n - 1
    return -1


def plot_time(dict_searches, sizes, searches):
    search_num = 0
    plt.xticks([j for j in range (len(sizes))],[str(size) for size in sizes])
    for search in searches:
        search_num += 1
        d = dict_searches[search.__name__]
        x_axis = [j + 0.05 * search_num for j in range(len(sizes))]
        y_axis = [d[i] for i in sizes]
        plt.bar(x_axis, y_axis, width=0.05, alpha=1, label=search.__name__) # alpha is the opacity in Matplotlib
    plt.legend()
    plt.title("Run time of search algorithms")
    plt.xlabel("Number of elements")
    plt.ylabel("Time for ten trials (ms)")
    plt.savefig("Assignments/Assignment1/Assignment1.png")
    plt.show()

def main():

    # my_list = random_list(min_num=1, max_num=1000, size=20, do_sort=True, unique=True)
    # print(my_list)
    # key = my_list[10]
    # print(native_search(my_list, key))
    # print(linear_search(my_list, key))
    # print(binary_search(my_list, key))
    # print(randomized_binary_search(my_list, key))
    # print(interpolation_search(my_list, key))
    # print(jump_search(my_list, key))
    # print(fibonacci_search(my_list, key))

    # You can change 1000 to some other #, the bigger the data,
    # the more accurate image we will get
    sizes = [1000 * i for i in range(1, 11)]  # initial val  1000*i ... (1,11)
    trials = 10
    searches = [python_search, linear_search, binary_search, randomized_binary_search,
                interpolation_search, jump_search, fibonacci_search]
    dict_searches = {}
    for search in searches:
        dict_searches[search.__name__] = {}
    for size in sizes:
        for search in searches:
            dict_searches[search.__name__][size] = 0
        for trial in range(1, trials+1):
            arr = random_list(1, 1000000, size, True, True)
            idx = random.randint(1, size) - 1
            key = arr[idx]
            for search in searches:
                start_time = time.time()
                idx_2 = search(arr, key)
                end_time = time.time()
                if idx_2 != idx:
                    print("We have an error in", search.__name__, "found at", idx_2, "expected at", idx)
                net_time = end_time - start_time
                dict_searches[search.__name__][size] += 1000*net_time
    #print(dict_searches)
    pd.set_option("display.max_rows", 500)
    pd.set_option("display.max_columns", 500)
    pd.set_option("display.width", 500)
    df = pd.DataFrame.from_dict(dict_searches).T
    print(df)
    plot_time(dict_searches, sizes, searches)


if __name__ == "__main__":
    main()
