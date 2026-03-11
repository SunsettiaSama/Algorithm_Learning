
from typing import List
"""
V0 例题
"""


class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        size = len(nums)
        dp = [1 for _ in range(size)]

        for i in range(size):
            for j in range(i):
                if nums[i] > nums[j]:
                    dp[i] = max(dp[i], dp[j] + 1)
        
        return max(dp)
    
"""
V0 试图手写
"""
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:

        # 此时dp[i]被定义为截至目前的最长严格递增子序列长度
        dp = [1 for i in range(len(nums))]

        for num_index in range(len(nums)):
            for update_index in range(num_index):
                if nums[num_index] > nums[update_index]: # 注意，这里题目要求删除数组中的元素，原地删除得到的序列也被定义为子序列，因此这里应该是update_index
                    dp[num_index] = max(dp[num_index], dp[update_index] + 1) # 注意是字串的最大
                    # 举个例子，dp[:2] = [1, 2, 3]
                    # 而第四个值dp[3]比前面的都大，那么就取出所有字串的最大值，再加一，也就是3 + 1
        
        return max(dp)