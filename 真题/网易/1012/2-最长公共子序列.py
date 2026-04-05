

# 很标准的dp题目啊

"""
没做出来啊，记得复习这个点

"""


import sys

def get_input():
    lines = sys.stdin.read().strip().split("\n")

    return lines

def get_max_length(string1, string2):
    # 从已知到未知

    # dp定义：前i个字符串和前j个字符串之间，有多少个最长字串
    # 是因为dp的定义吧，就是因为dp被定义成这样，所以才会要加一
    dp = [[0 for i in range(len(string1) + 1)] for j in range(len(string2) + 1)] # ERROR 为什么会这样，为什么要加一


    for i in range(1, len(string2) + 1):
        for j in range(1, len(string1) + 1):
            
            # 从头到尾遍历，如果字符相等，则更新dp值
            if string2[i - 1] == string1[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]) # 要不选你，要不选我，两个字母必须舍弃一个

    return dp[-1][-1]
    

def main():

    string1, string2 = get_input()

    print(get_max_length(string1, string2))

if __name__ == "__main__":
    main()
