

class Solution:
    def fib(self, n: int) -> int:

        # 问题分解，可以把第n项分级为第n-1项与第n-2项和

        # 利用哈希表存储结果
        count = dict()

        def dfs_sum(a):
            if a in count.keys():
                return count[a]
            if a == 0:
                return 1
            if a == 1:
                return 1
            
            result = dfs_sum(a - 1) + dfs_sum(a - 2)
            count[a] = result

            return result
        
        return dfs_sum(n)
    
"""
V0 修复版本
"""


class Solution:
    def fib(self, n: int) -> int:

        # 问题分解，可以把第n项分级为第n-1项与第n-2项和

        # 利用哈希表存储结果（记忆化递归，思路是对的）
        count = dict()

        def dfs_sum(a):
            # 优化点（非错误）：count.keys() 无需显式调用，直接 if a in count 即可
            if a in count.keys():
                return count[a]
            
            # 错误1：基准条件完全错误（核心问题）
            # 标准斐波那契：fib(0)=0，fib(1)=1；此处都返回1，导致所有结果错误
            if a == 0:
                return 0
            if a == 1:
                return 1
            
            result = dfs_sum(a - 1) + dfs_sum(a - 2)
            count[a] = result

            return result
        
        return dfs_sum(n)
    

"""
DP解法

"""

class Solution:
    def fib(self, n: int) -> int:
        # 动态规划-自底向上实现斐波那契：拆解子问题+存储子问题解+递推原问题
        # 初始条件（Base Case）：最小子问题的解，DP的计算起点
        if n <= 1: 
            return n
        
        # 状态定义：dp[i]表示斐波那契数列第i项的值，存储子问题解避免重复计算（优化重叠子问题）
        dp = [0 for _ in range(n + 1)]
        dp[0] = 0  # 初始化基础状态
        dp[1] = 1  # 初始化基础状态

        # 遍历顺序：从小到大，保证计算dp[i]时依赖的dp[i-1]/dp[i-2]已计算（无后效性）
        for i in range(2, n + 1):
            # 状态转移方程：当前子问题的解 = 更小的两个子问题解的和（最优子结构）
            dp[i] = dp[i - 2] + dp[i - 1]

        # 返回原问题的解：第n项的子问题结果
        return dp[n]

"""
V0


"""
class Solution:
    def fib(self, n: int) -> int:

        if n == 0:
            return 0
        if n == 1:
            return 1
        
        # 初始化dp
        dp = [0 for i in range(n)] # 索引边界：注意，dp[n]，这里的计算结果应该是n，而不是n+1
        dp[0] = 0
        dp[1] = 1

        for i in range(2, n):
            dp[i] = dp[i - 1] + dp[i - 2]
        
        return dp[n] # 问题同上
    


"""
V1
"""
class Solution:
    def fib(self, n: int) -> int:

        if n == 0:
            return 0
        if n == 1:
            return 1
        
        dp = [0 for i in range(n + 1)]
        dp[0] = 0
        dp[1] = 1

        for i in range(2, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]
        
        return dp[n]

