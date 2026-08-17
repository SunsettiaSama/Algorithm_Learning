

from typing import List

"""
递归解法，超过最大深度

"""

class Solution:
    def __init__(self):
        self.ans = False
        self.target_sum = 0


    def canPartition(self, nums: List[int]) -> bool:
        
        arr_sum = sum(nums)
        self.target_sum = arr_sum // 2

        # 边界条件：sum为奇数
        if arr_sum % 2 == 1:
            return False
        
        # 好，接下来的sum为偶数，dfs也能解这个题目
        return self.dfs(nums, curr_sum = 0, curr_index = 0)


    def dfs(self, arr, curr_sum, curr_index):

        if curr_index >= len(arr):
            return False
        
        # 如果搜索到答案，则返回
        if curr_sum == self.target_sum:
            return True
        
        # 在遇到第index个数时，我们有两种解法，一种是选该数，另一种是不选该数
        # 返回任何可能的结果
        return self.dfs(arr, 
                            curr_sum = curr_sum + arr[curr_index], 
                            curr_index = curr_index + 1) or \
                self.dfs(arr, 
                        curr_sum = curr_sum, 
                        curr_index = curr_index + 1)

"""
0-1背包解法

"""

class Solution:
    def canPartition(self, arr): 

        arr_sum = sum(arr)
        target_sum = arr_sum // 2
        
        # 边界条件：sum为奇数
        if arr_sum % 2 == 1:
            return False
        
        dp = [False for i in range(arr_sum // 2 + 1)]
        dp[0] = True

        for num in arr:
            # 倒序遍历：为什么要倒序呢？为什么避免多次更新最好用的其实是倒序？
            for j in range(target_sum, num - 1, -1):
                if dp[j - num]:
                    dp[j] = True
            
        if dp[target_sum]:
                return True

        return dp[target_sum]




"""
V1

"""

class Solution:
    def canPartition(self, arr): 

        size = len(arr)
        target_sum = sum(arr)
        if target_sum % 2 == 1:
            return False
        
        target = target_sum // 2

        dp = [False for i in range(target + 1)]
        # 为什么先迭代数组，后迭代dp：
        # 计算dp时，必须基于上一个状态，而不能混入当前物品的影响，这一点非常重要
        # 
        for num in arr:
            # 先迭代数组，再迭代dp
            for j in range(len(dp) - 1, 0, -1):
                if j >= num:
                    dp[j] = dp[j - num] or dp[j]
                
        return dp[target]
    

"""
V1

"""