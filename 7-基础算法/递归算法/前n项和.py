


class Solution:
    # 前n项和
    # 动态规划解
    def sum_of_first_n(self, n):
        # 边界条件：n=0时和为0，n=1时和为1
        if n == 0:
            return 0
        if n == 1:
            return 1
        
        # dp数组定义：dp[i] 表示 1到i+1 的和（因为数组索引从0开始）
        # 初始化dp数组，长度为n，初始值0
        dp = [0] * n
        dp[0] = 1  # 1的和为1
        
        # 状态转移方程：dp[i] = dp[i-1] + (i+1)
        # 解释：前i+1项和 = 前i项和 + 第i+1项的数值
        for i in range(1, n):
            dp[i] = dp[i-1] + (i + 1)
        
        # 返回前n项和（dp数组最后一个元素）
        return dp[-1]
    
    # 递归做法
    def sum_of_first_n(self, n):

        def dfs(n):

            if n == 0:
                return 0
            
            if n == 1:
                return 1

            return dfs(n - 1) + n
        
        return dfs(n)
        