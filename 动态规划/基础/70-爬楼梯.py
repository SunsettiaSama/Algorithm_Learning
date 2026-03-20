

"""

### 4.2.3 解题思路

#### 1. 阶段划分
我们按照台阶的阶层阶段划分，将其划分为 0～n 阶。

#### 2. 定义状态
定义状态 `dp[i]` 为：爬到第 i 阶台阶的方案数。

#### 3. 状态转移方程
根据题目大意，每次只能爬 1 或 2 个台阶。则第 i 阶楼梯只能从第 i−1 阶向上爬 1 阶上来，或者从第 i−2 阶向上爬 2 阶上来。所以可以推出状态转移方程为：
\[
dp[i] = dp[i - 1] + dp[i - 2]
\]

#### 4. 初始条件
- 第 0 层台阶方案数：可以看做 1 种方法（从 0 阶向上爬 0 阶），即 `dp[0] = 1`（注：原文此处笔误写成 `dp[1] = 1`，应为 `dp[0] = 1`）。
- 第 1 层台阶方案数：1 种方法（从 0 阶向上爬 1 阶），即 `dp[1] = 1`。
- 第 2 层台阶方案数：2 种方法（从 0 阶向上爬 2 阶，或者从 1 阶向上爬 1 阶）。

#### 5. 最终结果
根据状态定义，最终结果为 `dp[n]`，即爬到第 n 阶台阶（即楼顶）的方案数为 `dp[n]`。

虽然这道题跟上一道题的状态转移方程都是 \(dp[i] = dp[i - 1] + dp[i - 2]\)，但是两道题的考察方式并不相同，一定程度上也可以看出来动态规划相关题目的灵活多变。

"""

class Solution:
    def climbStairs(self, n: int) -> int:

        dp = [0 for _ in range(n+1)]

        dp[0] = 1
        dp[1] = 1

        for i in range(2, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]

        
        return dp[n]


"""
V0
"""
class Solution:
    def climbStairs(self, n: int) -> int:

        if n == 0:
            return 0
        if n == 1:
            return 1
        
        dp = [0 for 0 in range(n + 1)]

        dp[0] = 1
        dp[1] = 1

        for i in range(2, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]
        
        return dp[n]
    
"""
V1


"""

# 爬楼梯

class Solution:
    def climbStairs(self, n: int) -> int:
        dp = [0 for i in range(n + 1)]

        # 初始化状态0和状态1
        dp[0] = 0 # ERROR: 站在地面上没动,其实应该是一种方法,也即dp[0] = 1
        dp[1] = 1

        for i in range(2, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]
        
        return dp[n]
    

