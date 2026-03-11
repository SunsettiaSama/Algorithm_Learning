from typing import List

"""
V0 手搓

一、代码核心问题分析
你的代码思路存在根本性逻辑错误，导致无法正确求解 “最大连续子数组和” 问题，同时时间复杂度也偏高（O (n²)）。具体问题如下：
1. 核心错误：破坏了子数组的「连续性」要求
题目要求的是连续子数组的最大和，但你的状态转移逻辑会将非连续的子数组纳入计算：
你在计算 dp[num_index] 时，用了 dp[child_array_index] + nums[num_index]（其中 child_array_index < num_index），但 dp[child_array_index] 代表 “以 child_array_index 为结尾的子数组和”，直接加 nums[num_index] 会跳过 child_array_index+1 到 num_index-1 的元素，形成非连续子数组，这完全违背题目要求。
2. 示例验证错误（直观说明）
以 nums = [-2,1,-3,4,-1,2,1,-5,4] 为例（正确答案是 6，对应连续子数组 [4,-1,2,1]）：
你的代码计算 num_index=3（nums [3]=4）时，会取 child_array_index=1（dp [1]=1），得到 1+4=5，此时 dp[3]=5。但这个 5 对应的是「非连续子数组 [1,4]」（跳过了 nums [2]=-3），并非连续子数组的和，属于错误计算。
3. 状态定义模糊
你的 dp[num_index] 没有明确的定义（既不是 “以 num_index 结尾的最大连续子数组和”，也不是 “前 num_index 个元素的最大子数组和”），导致转移逻辑无依据。

"""
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        
        # 允许的最大和子数组肯定是自己及以上的部分
        dp = [nums[i] for i in range(len(nums))]

        for num_index in range(len(nums)):
            for child_array_index in range(num_index):
                # 更新规则：
                # 比较前面所有子数组的最大值之和，加上当前的值，看谁是最大的
                dp[num_index] = max(dp[child_array_index] + nums[num_index], dp[num_index])
            
        return max(dp)
    

"""
示例

连续就可以直接迭代
非连续就不可以直接迭代，而是需要重新规划前面的解

"""

class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        if not nums:
            return 0
        
        # 状态定义：dp[i] 以nums[i]结尾的最大连续子数组和
        dp = [0] * len(nums)
        dp[0] = nums[0]  # 初始状态：第一个元素自身就是子数组
        
        # 状态转移：仅需遍历一次，保证子数组连续性
        for i in range(1, len(nums)):
            dp[i] = max(dp[i-1] + nums[i], nums[i])
        
        # 所有结尾位置的最大值就是答案
        return max(dp)