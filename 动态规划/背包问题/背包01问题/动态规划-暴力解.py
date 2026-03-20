

class Solution:
    # 思路 1：动态规划（二维数组）
    def zeroOnePackMethod1(self, weight, value, W: int) -> int:
        """
        0-1 背包问题二维动态规划解法
        :param weight: List[int]，每件物品的重量
        :param value: List[int]，每件物品的价值
        :param W: int，背包最大承重
        :return: int，最大可获得价值
        """
        size = len(weight)
        # dp[i][w] 表示前 i 件物品，容量不超过 W 时的最大[价值]
        dp = [[0] * (W + 1) for _ in range(size + 1)]

        # 遍历每一件物品
        for i in range(1, size + 1):
            # 遍历每一种可能的背包容量
            for w in range(W + 1):
                if w < weight[i - 1]:
                    # 当前物品放不下，继承上一个状态
                    dp[i][w] = dp[i - 1][w]
                else:
                    # 当前物品可选，取放与不放的最大值
                    dp[i][w] = max(
                        dp[i - 1][w],  # 不放当前物品
                        dp[i - 1][w - weight[i - 1]] + value[i - 1]  # 放当前物品
                    )
        # 返回前 size 件物品、容量为 W 时的最大价值
        return dp[size][W]
    


"""
V0 手搓

"""

class Solution:
    # 思路 1：动态规划（二维数组）
    def zeroOnePackMethod1(self, weight, value, W: int) -> int:
        
        # 两个维度的dp：状态和重量
        # 表示前i件物品，容量不超过W时的最大价值
        dp = [[0 for i in range(W + 1)] for j in range(len(weight))]

        for i in range(1, len(weight) + 1):
            for w in range(W + 1):
                if w < weight[i - 1]:
                    # 第 i - 1 件物品无法放入背包，继承
                    dp[i][w] = dp[i - 1][w]
                else:
                    dp[i][w] = max(
                        dp[i - 1][w],  # 不放当前物品时候的价值
                        dp[i - 1][w - weight[i - 1]] + value[i - 1]  # 放当前物品时的价值，取最大值
                    )

        return dp[len(weight)][W]
