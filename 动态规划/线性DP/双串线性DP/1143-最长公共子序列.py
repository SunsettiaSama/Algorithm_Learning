

class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        size1 = len(text1)
        size2 = len(text2)
        dp = [[0 for _ in range(size2 + 1)] for _ in range(size1 + 1)]
        for i in range(1, size1 + 1):
            for j in range(1, size2 + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        return dp[size1][size2]


"""
V0 手搓版
"""
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        

        # 相当于新建一个dp表，这个表第i、j个元素表示前i、j个元素的最大公共子串数量
        # 计算方法无二，一个是

        size1 = len(text1)
        size2 = len(text2)
        dp = [[0 for _ in range(size2 + 1)] for _ in range(size1 + 1)]

        for i in range(1, size1 + 1):
            for j in range(1, size2 + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        return dp[size1][size2]
    

"""
V1 手搓版

"""

class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        
        len_text1 = len(text1)
        len_text2 = len(text2)

        # text1的前i个字符和text2的前j个字符的最长公共子序列长度
        dp = [[0 for i in range(len_text2 + 1)] for j in range(len_text1 + 1)]

        # 两个边缘肯定是没有结果的
        for i in range(1, len_text1 + 1):
            for j in range(1, len_text2 + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        return dp[len(text1)][len(text2)]


"""
V2手搓版


"""
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        
        size1 = len(text1)
        size2 = len(text2)

        # 定义dp[i][j]为前i、j个字符串的最长公共子序列
        # 从末端开始向前推导
        dp = [[0 for _ in range(size1 + 1)] for j in range(size2 + 1)]

        for i in range(1, size1 + 1):
            for j in range(1, size2 + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j]  = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
            



        












