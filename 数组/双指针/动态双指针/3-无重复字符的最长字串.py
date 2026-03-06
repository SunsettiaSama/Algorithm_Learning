





# 判定是否重复

"""
V0
"""

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        

        slow = 0
        fast = 0

        for fast in range(len(s)):
            
            curr_s = s[fast]
            # ERROR1: 窗口范围错误！当前窗口应是 [slow, fast)（左闭右开），你写成 fast-1 会漏掉前一个字符，且fast=0时fast-1=-1，切片直接出错
            # ERROR2: 无重复判断逻辑（curr_s 是否在窗口内），这是滑动窗口的核心
            # ERROR3: 无 slow 指针收缩逻辑（发现重复时，slow 需跳到重复字符的下一位）
            # ERROR4: 无最长长度记录变量（如 max_len），无法统计结果
            # ERROR5: 无返回语句，函数缺少核心输出
            temp_s = s[slow : fast - 1]



""" 
V0 修复版
"""

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        
        char_set = set()
        slow = 0
        max_len = 0

        for fast in range(len(s)):

            curr_char = s[fast]

            while curr_char in char_set:
                char_set.remove(s[slow])
                slow += 1

            char_set.add(curr_char)

            max_len = max(max_len, fast - slow + 1)

        return max_len






