# CSCI 323/700
# Summer 2022
# Assignment 4 - Empirical Performance of Search Structures
# Akil Bhuiyan

#imports
import numpy as np
import random
import time
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate
from math import floor, sqrt

def cuckoo_insert(key, table_num, cnt, table_size, pos, hash_table):
    if cnt == table_size:
        print("unpositioned:", key)
        print("Cycle present. REHASH.")
        return
    ver = len(hash_table)
    for i in range(ver):
        pos[i] = my_hash(i + 1, key, table_size)
        if hash_table[i][pos[i]] == key:
            return
    if hash_table[table_num][pos[table_num]] != -1: 
        dis = hash_table[table_num][pos[table_num]]
        hash_table[table_num][pos[table_num]] = key
        cuckoo_insert(dis, (table_num + 1) % ver, cnt + 1, table_size, pos, hash_table)
    else:
        hash_table[table_num][pos[table_num]] = key

def get_random_sublist(data, size):
    return [data[random.randint(0, len(data) - 1)] for i in range(size)]

def build_double_hash(data):
    tableSize = 7
    Hash = DoubleHashing(tableSize)
    for i in data:
        Hash.dHasing(i)

HashTable = [[] for _ in range(100)]
def build_quadratic_hash(data):
    arr = data
    N = 100
    tsize = 100
    table = HashTable
    for i in range(N):
        hv = arr[i] % tsize
        if table[hv] == -1:
            table[hv] = arr[i]
        else:
            for j in range(tsize):
                t = (hv + j * j) % tsize
                if table[t] == -1:
                    table[t] = arr[i]
                    break

def build_changing_hash(data):
    for i in data:
        has_key = i % len(HashTable)
        HashTable[has_key].append(data)

def pseudo_random_list(n):
    data = [0]
    for i in range(1, n):
        data.append(data[i - 1] + random.randint(1, 10))
    random.shuffle(data)
    return data

# From https://www.geeksforgeeks.org/double-hashing/
class DoubleHashing:
    def __init__(self, TableSize=1111):
        self.ts = TableSize
        self.List = [None] * self.ts
        self.count = 0  

    def nearestPrime(self):
        for l in range((self.ts - 1), 1, -1):
            flag = True
            for i in range(2, int(l ** 0.5) + 1):
                if l % i == 0:
                    flag = False
                    break
            if flag:
                return l
        return 3

    def Hx1(self, key):
        return key % self.ts

    def Hx2(self, key):
        return self.nearestPrime() - (key % self.nearestPrime())

    def dHasing(self, key):
        if self.count == self.ts:
            return self.List
        elif self.List[self.Hx1(key)] is None:
            self.List[self.Hx1(key)] = key
            self.count += 1
        else:
            comp = False
            i = 1
            while not comp:
                index = (self.Hx1(key) + i * self.Hx2(key)) % self.ts
                if self.List[index] is None:
                    self.List[index] = key
                    comp = True
                    self.count += 1
                else:
                    i += 1

def build_cuckoo_hash(data):
    size = len(data)
    table_size = size * 10
    num_tables = 2
    hash_table = [None] * num_tables
    hash_table[0] = [-1] * table_size
    hash_table[1] = [-1] * table_size
    pos = [None] * num_tables

def my_hash(func_num, key, size):
    if func_num == 1:
        return key % size
    else:
        return int(key / size) % size

def prime(n):
    if n & 1:
        n -= 2
    else:
        n -= 1
    i, j = 0, 3
    for i in range(n, 2, -2):
        if i % 2 == 0:
            continue
        while j <= floor(sqrt(i)) + 1:
            if i % j == 0:
                break
            j += 2

        if j > floor(sqrt(i)):
            return i
    return 2

def search_changing_hash(data, item):
    for i in HashTable:
        if i == item:
            return True
    return False

def search_quadratic_hash(data, item):
    for i in HashTable:
        if i == item:
            return True
    return False

def search_double_hash(data, item):
    for i in HashTable:
        if i == item:
            return True
    return False

def search_cuckoo_hash(data, item):
    for i in HashTable:
        if i == item:
            return True
    return False

def plot_time(dict_algs, sizes, algs, trials, ct):
    alg_num = 0
    plt.xticks([j for j in range(len(sizes))], [str(size) for size in sizes])
    for alg in algs:
        alg_num += 1
        d = dict_algs[alg.__name__]
        x_axis = [j + 0.05 * alg_num for j in range(len(sizes))]
        y_axis = [d[i] for i in sizes]
        plt.bar(x_axis, y_axis, width=0.05, alpha=1, label=alg.__name__)
    plt.legend()
    plt.title("Empirical Performance of Search Structures")
    plt.xlabel("Size of data")
    plt.ylabel("Time for ten trials (ms)")
    plt.savefig("Assignments/Assignment4/Assignment4" + ct + ".png")
    plt.show()

def main():
    sizes = [100 * i for i in range(1, 11)]
    trials = 10
    build_functions = [build_changing_hash, build_quadratic_hash, build_double_hash, build_cuckoo_hash]
    search_functions = [search_changing_hash, search_quadratic_hash, search_double_hash, search_cuckoo_hash]
    dict_build = {}
    dict_search = {}
    for build in build_functions:
        dict_build[build.__name__] = {}
    for search in search_functions:
        dict_search[search.__name__] = {}
    for size in sizes:
        for build in build_functions:
            dict_build[build.__name__][size] = 0
        for search in search_functions:
            dict_search[search.__name__][size] = 0
        for trial in range(1, trials + 1):
            data = pseudo_random_list(size)
            sublist = get_random_sublist(data, 100)
            hash_table = []
            for build in build_functions:
                stat_time = time.time()
                hash_table.append(build(data))
                end_time = time.time()
                net_time = end_time - stat_time
                dict_build[build.__name__][size] += 1000 * net_time
            for i in range(len(search_functions)):
                search = search_functions[i]
                table = hash_table[i]
                stat_time = time.time()
                for item in sublist:
                    search(table, item)
                end_time = time.time()
                net_time = end_time - stat_time
                dict_search[search.__name__][size] += 1000 * net_time
    pd.set_option("display.max_rows", 500)
    pd.set_option("display.max_columns", 500)
    pd.set_option("display.width", 1000)
    df = pd.DataFrame.from_dict(dict_build).T
    print(tabulate(df, headers='keys', tablefmt='psql'))
    dd = pd.DataFrame.from_dict(dict_search).T
    print(tabulate(dd, headers='keys', tablefmt='psql'))
    plot_time(dict_build, sizes, build_functions, trials, "a") # Graph For Build Functions
    plot_time(dict_search, sizes, search_functions, trials, "b") # Graph For Search Functions


if __name__ == "__main__":
    main()