





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



"""
V1 手搓版

"""

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:

        char_set = set()
        
        slow_index = 0
        max_res = 0

        # 快慢指针，维护子区间
        for fast_index in range(len(s)):

            # 往前挪动快指针，检查新的字符是否有重复
            # 如果没有重复，则向前挪，扩大维护区间
            # ERROR: 没有把当前的字符加入清单,包错的
            if s[fast_index] not in char_set:
                max_res = max(max_res, fast_index - slow_index) # ERROR:索引计算错误,还要加一才对
            # 如果重复，缩小左区间，直到不再重复为止
            else:
                while s[fast_index] in char_set:
                    char_set.remove(s[slow_index])
                    slow_index += 1
        
        return max_res

"""
V1 修复版

"""

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:

        char_set = set()  # 记录“当前窗口里的字符”（摆货的清单）
        slow_index = 0    # 滑动窗口的左边界（货架左边）
        max_res = 0       # 记录最长长度（记下来最长的货架长度）

        # fast_index是滑动窗口的右边界（货架右边），一步步往右挪
        for fast_index in range(len(s)):
            while s[fast_index] in char_set:
                char_set.remove(s[slow_index])
                slow_index += 1
            
            char_set.add(s[fast_index])

            current_length = fast_index - slow_index + 1
            max_res = max(max_res, current_length)

        return max_res
