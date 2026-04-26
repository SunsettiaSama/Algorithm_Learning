



class Solution:
    def numSquares(self, n: int) -> int:
        # dp[i] 表示组成 i 的最少完全平方数个数
        dp = [float('inf')] * (n + 1)
        dp[0] = 0  # 组成0不需要任何数

        # 外层循环遍历背包容量，正序以允许重复使用物品
        for target_sum in range(1, n + 1):
            # 内层循环遍历所有可能的完全平方数
            j = 1
            while j * j <= target_sum:
                # 状态转移方程
                dp[target_sum] = min(dp[target_sum], dp[target_sum - j * j] + 1)
                j += 1

        return dp[n]