
from typing import List

class Solution:
    def fib(self, n: int) -> int:
        # 使用数组保存已经求解过的 f(k) 的结果
        memo = [0 for _ in range(n + 1)]
        return self.my_fib(n, memo)

    def my_fib(self, n: int, memo: List[int]) -> int:
        if n == 0:
            return 0
        if n == 1:
            return 1
        
        # 已经计算过结果
        if memo[n] != 0:
            return memo[n]
        
        # 没有计算过结果
        # 递归的记忆化实现
        memo[n] = self.my_fib(n - 1, memo) + self.my_fib(n - 2, memo)
        return memo[n]
    

"""
记忆化搜索：自顶向下
递推：自底向上

"""




"""
V1

"""

# 其实如果用dp解这题，根本不需要进行记忆化搜索
MOD = 10 ** 9 + 7


class Solution:
    def fib(self, n: int) -> int:
        if n == 0:
            return 0
        if n == 1:
            return 1
        
        dp = [0 for i in range(n + 1)]

        # 初始化状态0和状态1
        dp[0] = 0 
        dp[1] = 1

        for i in range(2, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]
        
        return dp[n] % MOD # 注意取模这个操作，一定注意