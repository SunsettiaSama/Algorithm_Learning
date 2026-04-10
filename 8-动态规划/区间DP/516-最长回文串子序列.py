

# dp[i][j] 第i个字母到第j个字母这一小段中，最长的回文串序列有多长
# 对于区间i, j边界上的字符进行讨论，则它
# 1. 要么加入si可以组成更长的回文子序列长度
# 2. 要么加入sj可以组成更长的.......

class Solution:
    def longestPalindromeSubseq(self, s: str) -> int:

        size = len(s)
        dp = [[0 for _ in range(size)] for __ in range(size)]
        # 初始化区间，对角线上的字串最大值为它自己，其他的都是0
        for i in range(size):
            dp[i][i] = 1
        
        for i in range(size - 1, -1, -1):
            for j in range(i + 1, size):
                # 这样就维护了一个可能的全序列区间
                # 回文串的核心逻辑
                if s[i] == s[j]:
                    dp[i][j] = dp[i + 1][j - 1] + 2
                else:
                    dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])

        return dp[0][size - 1]

"""
V0手搓：
最关键的地方在于，一定是从中间向两边扩
但是因为边界问题，动的是右指针

"""

class Solution:
    def longestPalindromeSubseq(self, s: str) -> int:
        size = len(s)

        dp = [[0 for _ in range(size)] for __ in range(size)]
        # 第i、j个状态表示区间i、j内的最长回文字串长度
        # 对角线上的回文串长度已知
        # 从中间向外扩张
        for i in range(size):
            dp[i][i] = 1

        for i in range(size): # ERROR i：从右向左扫一遍
            for j in range(size): # ERROR j：必须在i的右边

                if s[i] == s[j]:
                    dp[i][j] = dp[i - 1][j - 1] + 2# ERROR 忘记加2
                else:
                    dp[i][j] = max(dp[i + 1][j] + dp[i][j - 1])

        return dp[size - 1][size - 1] # ERROR 根据定义，我们应该取得从0~size大小的最长回文串长度，重点在这里

"""
V0修复版

"""

class Solution:
    def longestPalindromeSubseq(self, s: str) -> int:
        size = len(s)

        dp = [[0 for _ in range(size)] for __ in range(size)]
        for i in range(size):
            dp[i][i] = 1  # ✅ 这行完全对！单个字母就是1，没毛病

        # ✅ 这两个循环也全对！i倒着走，j在i右边，老聪明了
        for i in range(size - 1, -1, -1): 
            for j in range(i + 1, size): 

                if s[i] == s[j]:
                    # 🔴【第一个致命错误】你写了 i-1，直接越界崩溃！
                    # dp[i][j] = dp[i - 1][j - 1] + 2 
                    # ✅ 改正：必须是 i+1（取中间的小段），不是i-1！
                    dp[i][j] = dp[i + 1][j - 1] + 2 
                else:
                    # 🔴【第二个错误】1. 用了+号（应该是逗号）2. 多余的[]
                    # dp[i][j] = max([dp[i + 1][j] + dp[i][j - 1]])
                    # ✅ 改正：max选大的，用逗号分隔，删掉[]
                    dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])

        return dp[0][size - 1]  # ✅ 返回值完全正确！
    
"""
V0 豆包给出的顺向遍历，避免逆向遍历这种逆天思路

"""
class Solution:
    def longestPalindromeSubseq(self, s: str) -> int:
        size = len(s)
        dp = [[0]*size for _ in range(size)]
        
        # 1. 单个字符，长度1（还是老样子）
        for i in range(size):
            dp[i][i] = 1

        # ==========================================
        # 🔴 重点！全是顺着跑！没有倒着的循环了！
        # 1. 先算 长度为2的，再算3的，4的... 顺着数长度！
        # 2. 左指针 i 从 0 开始 顺着往右跑！
        # 3. 右指针 j 跟着 i 走，永远在右边！
        # ==========================================
        for length in range(2, size + 1):  # 顺着算长度：2,3,4...直到整个字符串
            for i in range(size - length + 1): # 左指针i：顺着从左往右跑！
                j = i + length - 1  # 右指针j：跟着i，保证在右边
                
                # 👇 规则完全没变！还是原来的配方！
                if s[i] == s[j]:
                    dp[i][j] = dp[i+1][j-1] + 2  # 两头相等，中间+2
                else:
                    dp[i][j] = max(dp[i+1][j], dp[i][j-1]) # 不等，选大的

        return dp[0][size-1]


"""
V1 手搓版

"""

class Solution:
    def longestPalindromeSubseq(self, s: str) -> int:
        size = len(s)

        # 初始化，dp[i][j]代表该区间内的最长回文串子序列
        dp = [[0 for i in range(size)] for j in range(size)]
        for i in range(size):
            dp[i][i] = 1

        # 区间dp最重要的点：小区间到大区间
        for length in range(2, size + 1): # ERROR，最短长度为2

            for slow_index in range(size):
                fast_index = slow_index + length - 1

                if fast_index >= size:
                    break

                if s[slow_index] == s[fast_index]:
                    dp[slow_index][fast_index] = dp[slow_index + 1][fast_index - 1] + 2
                else:
                    dp[slow_index][fast_index] = max(dp[slow_index + 1][fast_index], dp[slow_index][fast_index - 1])

        return dp[0][size - 1]



