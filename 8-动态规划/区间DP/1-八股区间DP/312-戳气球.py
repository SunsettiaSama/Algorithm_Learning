"""
下次一定

"""
from typing import List

class Solution:
    def maxCoins(self, nums: List[int]) -> int:

        # 初始化
        size = len(nums)
        arr = [0 for _ in range(size + 2)]
        arr[0] = arr[size + 1] = 1
        for i in range(1, size + 1):
            arr[i] = nums[i - 1]
        
        # dp的定义：戳破所有气球i与气球j之间的气球，所能获取的最多硬币数
        dp = [[0 for _ in range(size + 2)] for _ in range(size + 2)]

        # 一定是左区间到右区间
        # 其中,不能从大区间开始算,需要从小区间开始算
        # 这里和贪婪算法类似,必须从小区间开始算,大区间就是寄
        for length in range(3, size + 3): # ERROR size + 3 防越界
            for slow_index in range(0, size + 2): # ERROR 从0开始
                fast_index = slow_index + length - 1
                if fast_index >= size + 2:
                    break

                for k in range(slow_index + 1, fast_index): # 不能戳区间点上的
                    dp[slow_index][fast_index] = max(dp[slow_index][fast_index], 
                                                     dp[slow_index][k] + dp[k][fast_index] + arr[slow_index] * arr[fast_index] * arr[k])
            
        return dp[0][size + 1]
    


class Solution:
    def maxCoins(self, nums: List[int]) -> int:

        n = len(nums)
        m = n + 2
        vals = [1] + nums + [1]
        # dp[i][j]被定义为开区间i、j之间的最优解
        dp = [[0 for i in range(m)] for j in range(m)]

        # 那么，假设存在k，其左右刚好为i和j（新增的一个气球），那么戳破后的状态转移方程
        # 更新的方向：从短区间到长区间
        for length in range(2, m):
            for i in range(0, m - length):
                j = i + length
                for k in range(i + 1, j): # 开区间
                    
                    dp[i][j] = max(dp[i][j], 
                                   dp[i][k] + dp[k][j] + vals[i] * vals[k] * vals[j])

        return dp[0][m - 1]

