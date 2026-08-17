

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



"""
V1 观摩

"""

class Solution:
    def zeroOnePackMethod1(self, weight, value, W: int) -> int:


        size = len(weight)

        # dp[i][w] 表示前i个物品中，容量不超过w时的最大价值
        dp = [[0  for w in range(W + 1)] for j in range(value)]

        for i in range(1, size + 1):
            for w in range(W + 1):

                if w < weight[i - 1]:
                    dp[i][w] = dp[i - 1][w]
                else:
                    dp[i][w] = max(
                        dp[i - 1][w], 
                        dp[i - 1][w - weight[i - 1]] + value[i - 1]
                    )

        return dp[size][W]
    

"""
V1 手搓

"""

class Solution:
    def zeroOnePackMethod1(self, weight, value, W: int) -> int:

        size = len(weight)
        # dp[w][i] 被定义成前i个物品，容量不超过W时的最大价值，dp的最大价值
        dp = [[0] * (W + 1) for i in range(size + 1)]

        for i in range(size + 1):
            for w in range(W + 1):
                # 如果拿不下，则不考虑
                if w < weight[i]:
                    dp[i][w] = dp[i - 1][w]
                else:
                    # 先记住：拿这件新东西，必须遵守一个死规矩
                    # 规矩：想拿新东西，必须先给它腾地方！
                    # 袋子就这么大，你要把新东西装进去，就得空出和它一样重的空间，空不出来就别拿。
                    dp[i][w] = max(
                        dp[i - 1][w],
                        dp[i - 1][w - weight[i - 1]] + value[i - 1]
                    )
        
        return dp[W][size]

"""
V1 手搓2

"""

class Solution:
    def zeroOnePackMethod1(self, weight, value, W: int) -> int:

        size = len(weight)
        # 前i件物品中，重量不超过W的最大价值
        dp = [[0] * (W + 1) for i in range(size + 1)]

        # ERROR: 从1开始到size结束
        for i in range(size + 1):
            for w in range(W + 1):
                if w < weight[i]: # 前i个物品
                    dp[i][w] = dp[i - 1][w]
                else:
                    dp[i][w] = max(
                        dp[i - 1][w],
                        dp[i - 1][w - weight[i]] + value[i]
                    )
        
        return dp[size][W]



"""
V1 空间优化
"""

class Solution:
    # 思路 2：动态规划 + 滚动数组优化
    def zeroOnePackMethod2(self, weight, value, W: int) -> int:
        """
        0-1 背包问题的滚动数组优化解法
        :param weight: List[int]，每件物品的重量
        :param value: List[int]，每件物品的价值
        :param W: int，背包最大承重
        :return: int，背包可获得的最大价值
        """
        size = len(weight)
        # dp[w] 表示容量为 w 时背包可获得的最大价值
        dp = [0] * (W + 1)

        # 遍历每一件物品
        for i in range(size):
            # 必须逆序遍历容量，防止状态被提前覆盖
            for w in range(W, weight[i] - 1, -1):
                # 状态转移：不选第 i 件物品 or 选第 i 件物品
                # dp[w] = max(不选, 选)
                dp[w] = max(dp[w], dp[w - weight[i]] + value[i])
                # 解释：
                # dp[w]：不选第 i 件物品，价值不变
                # dp[w - weight[i]] + value[i]：选第 i 件物品，容量减少，相应加上价值

        return dp[W]




