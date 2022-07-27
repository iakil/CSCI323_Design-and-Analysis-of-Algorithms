# CSCI 323/700
# Summer 2022
# Assignment 5 - Palindromic Substrings and Subsequences
# Akil Bhuiyan

# import 
import re
import time
import texttable

# From https://englishgrammarhere.com/example-sentences/50-examples-of-simple-sentences/
# From https://www.scarymommy.com/palindrome-sentences
def process_file(file_name):
    results = []
    #with open(file_name) as file:
    with open(file_name, encoding="latin-1") as file:
        lines = file.readlines()
        for line in lines:
            line = line.upper() # convert to upper case
            line = re.sub(r'[^A-Z]', '', line) # remove all non-alphabet chars
            start_time = time.time()
            st = lpsst(line)
            end_time = time.time()
            time_st = end_time - start_time
            start_time = time.time()
            sq = lpssq(line)[0]
            end_time = time.time()
            time_sq = end_time - start_time
            results.append([line, len(line), st, len(st), time_st, sq, len(sq), time_sq]) 
    return results

# From https://www.geeksforgeeks.org/longest-palindrome-substring-set-1/
# From https://www.geeksforgeeks.org/longest-palindromic-substring-set-2/ 
def lpsst(s: str) -> str:
    n = len(s)
    dp = [1]*n
    starts = [0]*n
    ends = [0]*n
    for i in range(1, n):
        _max = 0
        for j in range(0, i):
            k = 0
            while(s[j+k] == s[i-k] and j+k < i-k):
                k += 1
            if s[j+k] == s[i-k]:
                if j+k == i-k:
                    if _max < k*2+1:
                        _max = k*2+1
                        starts[i] = j
                        ends[i] = i
                if j+k == i-k+1:
                    if _max < k*2:
                        _max = k*2
                        starts[i] = j
                        ends[i] = i
        if _max > dp[i-1]:

            dp[i] = _max
        else:
            starts[i] = starts[i-1]
            ends[i] = ends[i-1]
            dp[i] = dp[i-1]
    #print(dp[n-1])
    return s[starts[n-1]: ends[n-1]+1]


# From https://www.geeksforgeeks.org/print-longest-palindromic-subsequence/
def lpssq_helper(X, Y, m, n, lookup):
    if m == 0 or n == 0:
        return ""
    if X[m - 1] == Y[n - 1]:
        return lpssq_helper(X, Y, m - 1, n - 1, lookup) + X[m - 1]
 
    if lookup[m - 1][n] > lookup[m][n - 1]:
        return lpssq_helper(X, Y, m - 1, n, lookup)

    return lpssq_helper(X, Y, m, n - 1, lookup)
 
# From https://www.geeksforgeeks.org/longest-common-subsequence-dp-4/ 
def LCSLength(X, Y, n, lookup):
 
   
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                lookup[i][j] = lookup[i - 1][j - 1] + 1
            else:
                lookup[i][j] = max(lookup[i - 1][j], lookup[i][j - 1])
 
    return lookup[n][n]
 
# From https://www.techiedelight.com/longest-palindromic-subsequence-using-dynamic-programming/
def lpssq(X):
    
    Y = X[::-1]
    lookup = [[0 for x in range(len(X) + 1)] for y in range(len(X) + 1)]
    lpssq_helper(X, Y, len(X), len(X), lookup)
    LCSLength(X, Y, len(X), lookup)
    return [lpssq_helper(X, Y, len(X), len(X), lookup),LCSLength(X, Y, len(X), lookup)]


# Wrapper test func
def test_lpsst_and_lpssq(s):
    st = lpsst(s)
    sq = lpssq(s)
    print("The test string is ", s, "with length", len(s))
    print("Its Longest Palindromic Substring is", st, "with length", len(st))
    print("Its Longest Palindromic Subsequence is", sq[0], "with length", sq[1])

# From https://www.geeksforgeeks.org/texttable-module-in-python/
def draw(txt):
    results = process_file(txt)
    headers = ["String", "Length", "LPSST", "Length", "Time", "LPSSQ", "Length", "Time"]
    tt = texttable.Texttable(500)
    tt.set_cols_align(["l", "r", "l", "r", "r", "l", "r", "r"])
    tt.set_cols_dtype(["t", "i", "t", "i", "f", "t", "i", "f"])
    tt.add_rows(results)
    tt.header(headers)
    print(tt.draw())


def main():
    #test_lpsst_and_lpssq(input("Enter string to compute longest palindrome string \n"))
    test_lpsst_and_lpssq("QUEENSCOLLEGEOFCUNY")
    palindromes_txt = "palindromes.txt"
    sentences_txt = "sentences.txt"
    draw(palindromes_txt)
    draw(sentences_txt)


if __name__ == "__main__":
    main()