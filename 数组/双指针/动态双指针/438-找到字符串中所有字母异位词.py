
"""
V0手搓版

"""
from typing import List

class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        if not s or not p:
            return []

        # 是这样的，我们需要维护一个区间，然后需要写一个区间检查
        res = []

        for slow_index in range(len(s)):
            if slow_index + len(p) > len(s):
                continue

            fast_index = slow_index + len(p)
            # 维护该区间
            
            if self.check(s, p, slow_index, fast_index):
                res.append(slow_index)

        return res


    def check(self, s, p, slow_index, fast_index):

        for check_s in p:
            if not check_s in s[slow_index: fast_index]:
                return False
            
        for check_s in s[slow_index: fast_index]:
            if not check_s in p:
                return False
        
        return True
        
"""
V0 豆包优化版
哈希表统计词频,以达到判断条件

"""


from typing import List

class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        res = []
        len_s, len_p = len(s), len(p)
        
        # 边界：s比p短，直接返回空
        if len_s < len_p:
            return res
        
        # 初始化26个字母的计数数组（a-z对应索引0-25）
        p_count = [0] * 26
        s_count = [0] * 26
        
        # 第一步：统计p的货单 + 统计s前len_p个字符的货单
        for i in range(len_p):
            # 把字符转成索引：ord('a')=97，所以ord(c)-97就是0-25
            p_count[ord(p[i]) - ord('a')] += 1
            s_count[ord(s[i]) - ord('a')] += 1
        
        # 先检查第一个窗口（0到len_p-1）
        if p_count == s_count:
            res.append(0)
        
        # 第二步：滑动窗口（左边界从1开始，右边界=左+len_p-1）
        for slow_index in range(1, len_s - len_p + 1):
            # 1. 去掉左边界左边的旧字符（窗口挪走了，货单减1）
            left_char = s[slow_index - 1]
            s_count[ord(left_char) - ord('a')] -= 1
            
            # 2. 加上右边界的新字符（窗口挪过来，货单加1）
            right_char = s[slow_index + len_p - 1]
            s_count[ord(right_char) - ord('a')] += 1
            
            # 3. 货单一致，记录左边界
            if p_count == s_count:
                res.append(slow_index)
        
        return res
    