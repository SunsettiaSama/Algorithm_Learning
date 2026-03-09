
"""
V0 例题
"""

class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        # 状态定义：dp[i][j]表示从(0,0)到(i,j)的不同路径数
        dp = [[0 for _ in range(n)] for _ in range(m)]

        # 初始化：第一行所有列路径数为1（只能从左到右走）
        for j in range(n):
            dp[0][j] = 1
        
        # 初始化：第一列所有行路径数为1（只能从上到下走）
        for i in range(m):
            dp[i][0] = 1
        
        # 遍历顺序：从(1,1)开始，保证依赖的dp[i-1][j]和dp[i][j-1]已计算
        for i in range(1, m):
            for j in range(1, n):
                # 状态转移：当前路径数 = 上方路径数 + 左方路径数（只能向右/向下走）
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
            
        # 注意：返回右下角位置，索引为(m-1, n-1)（数组索引从0开始）
        return dp[m - 1][n - 1]