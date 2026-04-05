

class Solution:


    def maxProfit(self, prices):
        n = len(prices)
        if n <= 1:
            return 0
        
        # 定义二维DP数组
        dp = [[0] * 2 for _ in range(n)]
        
        # 初始状态
        dp[0][0] = 0
        dp[0][1] = -prices[0]
        
        # 状态转移
        for i in range(1, n):
            dp[i][0] = max(dp[i-1][0], dp[i-1][1] + prices[i])
            dp[i][1] = max(dp[i-1][1], -prices[i])
        
        # 最后一天不持有股票的最大利润
        return dp[-1][0]




"""
V0 手搓

"""


class Solution:
    def maxProfit(self, prices):

        n = len(prices)
        if n <= 1:
            return 0
        
        # 持有和非持有的净利润
        dp = [[0 for i in range(2)] for j in range(n)]

        # 不持有肯定是0，持有则是1
        dp[0][0] = 0
        dp[0][1] = -prices[0]

        for i in range(1, len(prices)): # ERROR 第一天已经做了初始化了
            # 要么买入要么不买如
            # 前一天持有，不卖，开摆
            dp[i][0] = max(dp[i - 1][0], dp[i - 1][1] + prices[i])
            # 这个题目设计是第一次买入，他就一定是简单的-prices，而不允许多次买入卖出
            dp[i][1] = max(dp[i - 1][1], - prices[i])

        return dp[-1][0]



"""
V1 手搓




"""











