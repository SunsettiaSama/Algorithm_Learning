
"""
V0迁移版


注意一个非常关键的问题,之前我们做的都是子序列分解,而这里不是,这里是子串,要求连续

"""


class Solution:
    def longestPalindrome(self, s: str) -> str:
        size = len(s)
        if size == 0:
            return ""
        
        # dp[i][j] = s[i..j]是否是回文子串（布尔型）
        dp = [[False]*size for _ in range(size)]
        max_len = 1  # 最长回文子串长度
        start = 0    # 最长回文子串起始索引
        
        # 单个字符都是回文
        for i in range(size):
            dp[i][i] = True
        
        # 你的核心滑窗：先短后长，双指针
        for length in range(2, size + 1):
            for slow in range(size):
                fast = slow + length - 1
                if fast >= size:
                    break
                
                if s[slow] == s[fast]:
                    # 长度为2时，直接是回文；长度>2时，看中间是否是回文
                    if length == 2:
                        dp[slow][fast] = True
                    else:
                        dp[slow][fast] = dp[slow+1][fast-1]
                else:
                    dp[slow][fast] = False  # 子串必须连续，不等就不是回文
                
                # 更新最长回文子串
                if dp[slow][fast] and length > max_len:
                    max_len = length
                    start = slow
        
        return s[start:start+max_len]
    

"""
V0战损版

"""

class Solution:
    def longestPalindrome(self, s: str) -> str:
        size = len(s)
        if size == 0:
            return ""
        
        # dp[i][j] = s[i..j]是否是回文子串（布尔型）
        dp = [[False]*size for _ in range(size)]
        max_len = 1  # 最长回文子串长度
        start = 0    # 最长回文子串起始索引
        
        # 单个字符都是回文
        for i in range(size):
            dp[i][i] = True
        
        # 你的核心滑窗：先短后长，双指针
        for length in range(2, size + 1):
            for slow in range(size):
                fast = slow + length - 1
                if fast >= size:
                    break
                
                if s[slow] == s[fast]:
                    if length == 2:
                        dp[slow][fast] = True
                    else:
                        dp[slow][fast] = dp[slow+1][fast-1]
                else:
                    dp[slow][fast] = False

                if dp[slow][fast] and length > max_len:
                    max_len = length
                    start = slow
        
        return s[start: start + max_len]

