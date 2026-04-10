
from typing import List

class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        size = len(nums)

        def dfs(i, cur_sum):
            if i == size:
                if cur_sum == target:
                    return 1
                else:
                    return 0
            ans = dfs(i + 1, cur_sum - nums[i]) + dfs(i + 1, cur_sum + nums[i])
            return ans
        
        return dfs(0, 0)

class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        size = len(nums)
        table = dict()

        def dfs(i, cur_sum):
            if i == size:
                if cur_sum == target:
                    return 1
                else:
                    return 0
                    
            if (i, cur_sum) in table:
                return table[(i, cur_sum)]
            
            cnt = dfs(i + 1, cur_sum - nums[i]) + dfs(i + 1, cur_sum + nums[i])
            table[(i, cur_sum)] = cnt
            return cnt

        return dfs(0, 0)
    
"""
V1
试图烧烤，但是失败
"""

class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:

        total = sum(nums)

        if abs(target) > total or (target + total) % 2 != 0:
            return 0
        
        # 区间对折
        sum_pos = (target + total) // 2

        dp = [0 for i in range(sum_pos + 1)]
        dp[0] = 1

        for num in nums:
            for j in range(sum_pos, num - 1, -1):
                dp[j] += dp[j - num]
        
        return dp[sum_pos]

