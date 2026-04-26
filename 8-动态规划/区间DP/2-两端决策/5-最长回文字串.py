
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


"""
V1 学习版


"""

class Solution:
    def longestPalindrome(self, s: str) -> str:

        size = len(s)

        if size == 0 or size == 1:
            return s
        
        dp = [[i for i in range(size + 1)] for j in range(size + 1)]

        start_idx = 0
        end_idx = 0

        # 这其实也是一个变相的快慢指针，不是O（n^2）
        for j in range(1, size):
            for i in range(j):

                # 如果是回文
                if s[i] == s[j]:
                    if j - i <= 2:
                        dp[i][j] = True
                    else:
                        dp[i][j] = dp[i - 1][j - 1] # ERROR: 状态转移方程错误
                    # 判定并记录区间两侧
                    # ===========问题=================
                    # 1. 此时不能保证该值一定为真，即不能确信是否为回文，因此无法确定
                    # 2. 即使能确定，我们的区间长度也应该加一
                    # 3. 并且注意,在我们的定义下,末端的索引应该加一才对,不然最后一个值会被抛弃
                    # ============================
                    if dp[i][j] and j - i + 1 > end_idx - start_idx : 
                        start_idx = i
                        end_idx = j

                # 如果不是回文，则直接否决
                # ===========问题=================
                # 1. 初始化的时候应该保证值为False
                # ============================
                else:
                    dp[i][j] = False

        return s[start_idx: end_idx]

    
"""
V1 修复版

"""

class Solution:
    def longestPalindrome(self, s: str) -> str:

        size = len(s)

        if size == 0 or size == 1:
            return s
        
        dp = [[False for i in range(size + 1)] for j in range(size + 1)]

        start_idx = 0
        end_idx = 1

        # 这其实也是一个变相的快慢指针，不是O（n^2）
        for j in range(1, size):
            for i in range(j):

                # 如果是回文
                if s[i] == s[j]:
                    if j - i <= 2:
                        dp[i][j] = True
                    else:
                        dp[i][j] = dp[i + 1][j - 1] 

                    if dp[i][j] and j - i + 1 > end_idx - start_idx: 
                        start_idx = i
                        end_idx = j + 1

        return s[start_idx: end_idx]



class Solution:
    def expandAroundCenter(self, s: str, left: int, right: int) -> int:
        """从中心向两侧扩展，返回回文子串的长度"""
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        # 循环结束时，s[left+1:right] 是有效的回文子串
        return right - left - 1

    def longestPalindrome(self, s: str) -> str:
        if not s:
            return ""
        
        start, end = 0, 0
        for i in range(len(s)):
            # 情况1：以当前字符为中心的奇数长度回文
            len1 = self.expandAroundCenter(s, i, i)
            # 情况2：以当前字符和下一个字符之间的间隙为中心的偶数长度回文
            len2 = self.expandAroundCenter(s, i, i + 1)
            # 取两种情况下的最大长度
            max_len = max(len1, len2)
            # 如果找到更长的回文，则更新起止索引
            if max_len > (end - start):
                start = i - (max_len - 1) // 2
                end = i + max_len // 2
        return s[start:end+1]
    