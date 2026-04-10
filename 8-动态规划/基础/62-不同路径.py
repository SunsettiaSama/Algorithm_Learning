
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
    

"""
V1
"""


class Solution:
    def uniquePaths(self, m: int, n: int) -> int:

        # 使用dp解
        # 显然，这里需要初始化一个网格状的dp解，并进行贪心搜索
        dp = [[0 for i in range(n)] for j in range(m)]

        # 很显然，向右或者向下只有一条路径
        # 初始化
        for i in range(m):
            dp[i][0] = 1

        for i in range(n):
            dp[0][i] = 1
        
        # 动态规划核心：状态转移
        for row_index in range(1, m):
            for col_index in range(1, n):
                dp[row_index][col_index] = dp[row_index - 1][col_index] + dp[row_index][col_index - 1]

        return dp[m - 1][n - 1]
    

"""

V2
"""
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        # 能够显式建立状态方程,使用dp做解

        # 每一个格子被定义为到达当前位置的路径可能数量
        dp = [[0 for i in range(n)] for j in range(m)]

        # 初始化0行，0列，因为不可能向上走，所以可能路径为1
        for i in range(m):
            dp[i][0] = 1
        for j in range(n):
            dp[0][j] = 1

        # 状态转移过程
        # 第i、j个位置，仅有可能为i-1的位置和j-1的位置挪过来
        for i in range(1, m):
            for j in range(1, n):
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1]

        return dp[m - 1][n - 1]


