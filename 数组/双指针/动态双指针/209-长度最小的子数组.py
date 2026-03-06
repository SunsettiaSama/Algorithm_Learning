from typing import List

"""
V0 错误版本
"""

class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        
        if sum(nums) < target:
            return 0

        slow_index = 0  # ERROR: 后续被for循环重新定义，初始赋值无意义
        fast_index = 1  # ERROR: 后续被for循环重新定义，初始赋值无意义

        length_counts = []

        # 枚举，遍历剩下的所有解
        for slow_index in range(len(nums)):
            for fast_index in range(slow_index + 1, len(nums)):

                # ERROR1: 题目要求「和 ≥ target」，此处写成「== target」，漏掉大量符合条件的子数组
                # ERROR2: sum(nums[slow_index: fast_index]) 每次循环求和，时间复杂度O(n²)，且切片是左闭右开，fast_index只到len(nums)-1，漏掉包含最后一个元素的子数组
                if sum(nums[slow_index: fast_index]) == target:
                    length_counts.append(fast_index - slow_index)
        
        # ERROR3: 若没有和等于target的子数组（但有和≥target的），length_counts为空，调用min会抛出空列表异常
        return min(length_counts)
    


"""
V0 错误版本
"""

class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        
        n = len(nums)

        min_len = float('inf')
        slow = 0
        window_sum = 0

        for fast in range(n):
            window_sum += nums[fast]

            while window_sum >= target:
                min_len = min(min_len, fast - slow + 1)

                window_sum -= nums[slow]
                slow += 1

        return min_len if min_len != float('inf') else 0
    

"""
V0 修复版
"""

class Solution:
    def minSubArrayLen(self, target, nums):

        n = len(nums)

        min_len = float('inf')
        slow = 0
        window_sum = 0

        # 固定右扩
        for fast in range(n):
            window_sum += nums[fast]

            # 动态左收
            # 动态双指针
            while window_sum >= target:

                min_len = min(min_len, fast - slow + 1)
                window_sum -= nums[slow]

                slow += 1
        
        return min_len if min_len != float('inf') else 0



