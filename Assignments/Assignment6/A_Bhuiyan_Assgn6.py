# CSCI 323/700
# Summer 2022
# Assignment 6 - Sub-String Search Algorithms
# Akil Bhuiyan


import re
import time
import texttable
import pandas as pd
import matplotlib.pyplot as plt


# Native Search
def native_search(text, pattern):
    return text.find(pattern)


# Brute Force Search
# from https://www.geeksforgeeks.org/naive-algorithm-for-pattern-searching/
def brute_force_search(text, pattern):
    m = len(pattern)
    n = len(text)
    for i in range(n - m + 1):
        j = 0
        while j < m:
            if text[i + j] != pattern[j]:
                break
            j += 1
        if j == m:
            return i
    return -1


# Rabin-Karp Search
# from https://www.geeksforgeeks.org/rabin-karp-algorithm-for-pattern-searching/
def rabin_karp_search(text, pattern):
    m = len(pattern)
    n = len(text)
    j = 0
    p = 0 
    t = 0  
    h = 1
    q = 101
    d = 256 
    for i in range(m - 1):
        h = (h * d) % q
    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q
    for i in range(n - m + 1):
        if p == t:
            for j in range(m):
                if text[i + j] != pattern[j]:
                    break
                else:
                    j += 1
            if j == m:
                return i
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            if t < 0:
                t = t + q
    return -1


# Knuth-Morris-Pratt Search
#from https://www.geeksforgeeks.org/kmp-algorithm-for-pattern-searching/
def computeLPSArray(pattern, m, lps):
    len = 0  
    lps[0] 
    i = 1
    while i < m:
        if pattern[i] == pattern[len]:
            len += 1
            lps[i] = len
            i += 1
        else:
            if len != 0:
                len = lps[len - 1]
            else:
                lps[i] = 0
                i += 1

def knuth_morris_pratt_search(text, pattern):
    m = len(pattern)
    n = len(text)
    lps = [0] * m
    j = 0 
    computeLPSArray(pattern, m, lps)

    i = 0 
    while (n - i) >= (m - j):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            return i-j
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1


# Boyer-Moore Search
#from https://www.geeksforgeeks.org/boyer-moore-algorithm-for-pattern-searching/
def badCharHeuristic(string, size):
    NO_OF_CHARS = 256
    badChar = [-1] * NO_OF_CHARS
    for i in range(size):
        badChar[ord(string[i])] = i
    return badChar

def boyer_moore_search(text, pattern):
    m = len(pattern)
    n = len(text)
    badChar = badCharHeuristic(pattern, m)
    s = 0
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            return s
            s += (m - badChar[ord(text[s + m])] if s + m < n else 1)
        else:
            s += max(1, j - badChar[ord(text[s + j])])
    return -1


# Plot Time
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
    plt.title("Sub-String Search Algorithms")
    plt.xlabel("Size of data")
    plt.ylabel("Time for " + str(trails) + " trails" " (ms)")
    plt.savefig("Assignment6.png")
    plt.show()


def run_trials():
    sizes = [10 * i for i in range(1, 11)]
    trials = 100
    algs = [native_search, brute_force_search, rabin_karp_search, knuth_morris_pratt_search, boyer_moore_search]
    dict_algs = {}
    for alg in algs:
        dict_algs[alg.__name__] = {}
    for size in sizes:
        for alg in algs:
            dict_algs[alg.__name__][size] = 0
        for trial in range(1, trials + 1):
            for alg in algs:
                text = read_file1("Assignment6_Text1.txt") # copy the actual path of this txt file
                pattern = read_file2("Assignment6_Patterns.txt") # copy the actual path of this txt file
                start_time = time.time()
                for i in range(len(text)):
                    for j in range(len(pattern)):
                        alg(text[i], pattern[j])
                end_time = time.time()
                net_time = end_time - start_time
                dict_algs[alg.__name__][size] += 1000 * net_time
    pd.set_option("display.max_rows", 500)
    pd.set_option("display.max_columns", 500)
    pd.set_option("display.width", 1000)
    df = pd.DataFrame.from_dict(dict_algs).T
    print(df)
    plot_time(dict_algs, sizes, algs, trials)


def read_file1(file):
    result = []
    with open(file, encoding="latin-1") as file_text:
        texts = file_text.readlines()
        for text in texts:
            text = text.upper()  # convert to upper case
            text = re.sub(r'[^A-Z]', '', text)  # remove all non-alphabet chars
            if text == '':
                break
            result.append(text)
    return result

def read_file2(file):
    result = []
    with open(file, encoding="latin-1") as file_pattern:
        patterns = file_pattern.readlines()
        for pattern in patterns:
            pattern = pattern.upper()  # convert to upper case
            pattern = re.sub(r'[^A-Z]', '', pattern)  # remove all non-alphabet chars
            result.append(pattern)
    return result


# File Process
def process_file(file_name_text, file_name_pattern):
    results = []
    with open(file_name_text, encoding="latin-1") as file_text, open(file_name_pattern, encoding="latin-1") as file_pattern:
        texts = file_text.readlines()
        patterns = file_pattern.readlines()
        for text in texts:
            text = text.upper()  # convert to upper case
            text = re.sub(r'[^A-Z]', '', text)  # remove all non-alphabet chars
            # print(text)
            if text == '':
                break
            for pattern in patterns:
                pattern = pattern.upper()  # convert to upper case
                pattern = re.sub(r'[^A-Z]', '', pattern)  # remove all non-alphabet chars
                ns = native_search(text, pattern)
                bfs = brute_force_search(text, pattern)
                rks = rabin_karp_search(text, pattern)
                kmps = knuth_morris_pratt_search(text, pattern)
                bm = boyer_moore_search(text, pattern)
                results.append([text, pattern, len(text), ns, bfs, rks, kmps, bm])
    headers = ["String", "Pattern", "Length", "Native", "Brute Force", "Rabin Karp", "KMP", "Boyer Moore"]
    tt = texttable.Texttable(500)
    tt.set_cols_align(["l", "c", "c", "c", "c", "c", "c", "c"])
    tt.set_cols_dtype(["t", "t", "i", "i", "i", "i", "i", "i"])
    tt.add_row(results[0])
    tt.add_rows(results)
    tt.header(headers)
    print(tt.draw())
    return results


# Main
def main():
    run_trials()
    process_file("Assignment6_Text1.txt", "Assignment6_Patterns.txt") 
    process_file("Assignment6_Text2.txt", "Assignment6_Patterns.txt") # copy the actual path of this txt file

'''
    # Test
    # run_trials()
    text = 'loopsdjbeiwm'
    pattern = 'jdb'
    idx1 = native_search(text, pattern, True)
    idx2 = brute_force_search(text, pattern, True)
    idx3 = rabin_karp_search(text, pattern, True)
    # ...
    print(idx1, idx2, idx3)
'''


if __name__ == "__main__":
    main()
