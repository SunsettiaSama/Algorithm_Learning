
from typing import List

class Solution:
    def rob(self, nums: List[int]) -> int: 

        if len(nums) == 1:
            return nums[0]
        if len(nums) == 2:
            return max(nums)

        # dp[i]: 偷到前i间房子的最高金额数目
        dp = [i for i in range(len(nums))]
        dp[0] = nums[0]  # 只偷第一个房子
        dp[1] = nums[1]  # 只偷第二个房子    # ERROR: DP定义问题,这里应该偷更有钱的那个,也就是max(...[0], ...[1])

        for i in range(2, len(nums)):
            # 前一个房子如果偷了，那么本房子就不能偷
            # 如果前一个房子没偷，那么本房子就可以偷
            dp[i] = max(dp[i - 1], dp[i - 2] + nums[i])
        
        return dp[-1]


"""
豆包错误指出

"""

class Solution:
    def rob(self, nums: List[int]) -> int: 

        if len(nums) == 1:
            return nums[0]
        if len(nums) == 2:
            return max(nums)

        dp = [0] * len(nums)  # 优化初始化，比你原来的写法更简洁
        dp[0] = nums[0]  
        dp[1] = max(nums[0], nums[1])  # 只改这一行！

        for i in range(2, len(nums)):
            dp[i] = max(dp[i - 1], dp[i - 2] + nums[i])
        
        return dp[-1]