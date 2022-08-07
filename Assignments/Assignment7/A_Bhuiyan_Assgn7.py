# CSCI 323/700
# Summer 2022
# Assignment 7 - Shortest Path Algorithms for Graphs
# Akil Bhuiyan

import copy
import random
import re
import numpy as np
import time
import texttable
import pandas as pd
import matplotlib.pyplot as plt
from numpy import split
assn_num = 7
INF = 99999


def read_graph(file_name):
    graph = []
    with open(file_name) as file:
        for line in file.readlines():
            row = []
            s = line.split(" ")
            for ss in s:
                row.append(int(ss))
            graph.append(row)
    return graph


def random_graph(size, max_cost):
    graph = []
    for i in range(size):
        row = []
        for j in range(size):
            if i == j:
                row.append(0)
            else:
                cost = random.randint(1, max_cost)
                row.append(cost)
        graph.append(row)
    return graph


def make_non_edges_inf(graph):
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            if graph[i][j] == 0:
                graph[i][j] = INF


# From: https://www.geeksforgeeks.org/floyd-warshall-algorithm-dp-16/
def floyd_apsp(graph):
    graph_copy = copy.deepcopy(graph)
    n = len(graph_copy)
    dist = [[INF] * n for i in range(n)]
    pred = [[-1] * n for i in range(n)]
    for i in range(n):
        for j in range(n):
            dist[i][j] = graph_copy[i][j]
            pred[i][j] = i
        dist[i][i] = 0
        pred[i][i] = -1
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    pred[i][j] = pred[k][j]
    print_solution_floyd(dist, pred)


def print_solution_floyd(dist, pred):
    n = len(dist)
    for i in range(n):
        for j in range(n):
            if dist[i][j] == INF:
                return
                # print("%7s\t" % ("INF"), end=" ")
            else:
                return
                # print("%7d\t" % (dist[i][j]), end=' ')
            if j == n - 1:
                return
                # print()
    for i in range(n):
        for j in range(n):
            return
            # print("%7d\t" % (pred[i][j]), end=' ')
        return
        # print()


def print_graph(graph):
    n = len(graph)
    for i in range(n):
        for j in range(n):
            if graph[i][j] == 0:
                print("%7s\t" % ("INF"), end=" ")
            else:
                print("%7d\t" % (graph[i][j]), end=' ')
        print()


def convert_to_adj_table(graph):
    adj_table = []
    for i in range(len(graph)):
        row = graph[i]
        neighbors = []
        for j in range(len(row)):
            if graph[i][j] > 0:
                neighbors.append((j, graph[i][j]))
        adj_table.append(neighbors)
    return adj_table


def convert_to_edge_set(graph):
    edge_set = []
    for i in range(len(graph)):
        row = graph[i]
        for j in range(len(row)):
            if graph[i][j] > 0:
                edge_set.append((i, j, graph[i][j]))
    return edge_set


# From: https://www.geeksforgeeks.org/bellman-ford-algorithm-dp-23/
def bellman_ford_sssp(es, n, src):
    dist = [INF] * n
    dist[src] = 0
    for i in range(n):
        for u, v, w in es:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    for u, v, w in es:
        if dist[u] != INF and dist[u] + w < dist[v]:
            # return
            print()
    print(dist)


def bellman_ford_apsp(graph):
    transform = convert_to_edge_set(graph)
    for i in range(len(graph)):
        bellman_ford_sssp(transform, len(graph), i)


def min_distance(dist, done):
    n = len(dist)
    min_dist = INF
    min_index = -1
    for u in range(n):
        if dist[u] < min_dist and not done[u]:
            min_dist = dist[u]
            min_index = u
    return min_index


# From: https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/
def dijkstra_sssp_matrix(cm, src):
    n = len(cm)
    dist = [INF] * n
    dist[src] = 0
    done = [False] * n
    for i in range(n):
        x = min_distance(dist, done)
        done[x] = True
        for y in range(n):
            if cm[x][y] > 0 and not done[y] and dist[y] > dist[x] + cm[x][y]:
                dist[y] = dist[x] + cm[x][y]
    print(dist)


def dijkstra_asap_matrix(graph):
    for i in range(len(graph)):
        dijkstra_sssp_matrix(graph, i)


def dijkstra_sssp_table(table, src):
    smallest = src
    left = 2 * src + 1
    right = 2 * src + 2
    if (left < table.size and
            table.array[left][1]
            < table.array[smallest][1]):
        smallest = left
    if (right < table.size and
            table.array[right][1]
            < table.array[smallest][1]):
        smallest = right
    if smallest != src:
        table.pos[table.array[smallest][0]] = src
        table.pos[table.array[src][0]] = smallest
        table.swapMinHeapNode(smallest, src)
        table.dijkstra_sssp_table(smallest)


def swapMinHeapNode(self, a, b):
    t = self.array[a]
    self.array[a] = self.array[b]
    self.array[b] = t

def dijkstra_asap_table(graph):
    for i in range(len(graph)):
        dijkstra_sssp_matrix(graph, i)



def plot_time(dict_algs, sizes, algs, trails):
    alg_num = 0
    plt.xticks([j for j in range(len(sizes))], [str(size) for size in sizes])
    for algs in algs:
        alg_num += 1
        d = dict_algs[algs.__name__]
        x_axis = [j + 0.05 * alg_num for j in range(len(sizes))]
        y_axis = [d[i] for i in sizes]
        plt.bar(x_axis, y_axis, width=0.05, alpha=1, label=algs.__name__)
    plt.legend()
    #plt.title("Run Time of Search Algorithms")
    plt.title("Shortest Path Algorithms for Graphs")
    plt.xlabel("Size of Data")
    plt.ylabel(f"Time for {trails} trail (ms)")
    plt.savefig(f"Assignments/Assignment{assn_num}/Assignment{assn_num}.png")
    plt.show()


def main():
    sizes = [10 * i for i in range(1, 11)]
    trials = 1
    algs = [floyd_apsp, bellman_ford_apsp, dijkstra_asap_matrix, dijkstra_asap_table]
    dict_algs = {}
    for alg in algs:
        dict_algs[alg.__name__] = {}
    for size in sizes:
        for alg in algs:
            dict_algs[alg.__name__][size] = 0
            am1 = random_graph(size, 100)
            if size == 10:
                print_graph(am1)
        for trial in range(1, trials + 1):
            for alg in algs:
                start_time = time.time()
                idx = alg(am1)
                end_time = time.time()
                net_time = end_time - start_time
                dict_algs[alg.__name__][size] += 1000 * net_time
    pd.set_option("display.max_rows", 500)
    pd.set_option("display.max_columns", 500)
    pd.set_option("display.width", 1000)
    df = pd.DataFrame.from_dict(dict_algs).T
    print(df)
    plot_time(dict_algs, sizes, algs, trials)


    # am1 = read_graph("graph1.txt")
    # am1 = random_graph(5, 100)
    # print("Cost Matrix:", am1)
    # at1 = convert_to_adj_table(am1)
    # print("Adjacency Table:", at1)
    # es1 = convert_to_edge_set(am1)
    # print("Edge Set:", es1)
    # print("Cost Matrix")
    # print_graph(am1)
    # print("Floyd APSP")
    # floyd_apsp(am1)
    # print("Bellman Ford SSSP")
    # for i in range(len(am1)):
    #     bellman_ford_sssp(es1, len(am1), i)
    # print("bellman_ford_apsp")
    # bellman_ford_apsp(am1)
    #
    # print("Dijkstra SSSP")
    # for i in range(len(am1)):
    #     dijkstra_sssp_matrix(am1, i)
    # print("dijkstra_asap_matrix")
    # dijkstra_asap_matrix(am1)
    #
    # print("dijkstra_asap_table")
    # dijkstra_asap_table(am1)



if __name__ == "__main__":
    main()
