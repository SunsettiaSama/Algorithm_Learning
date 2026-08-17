


from typing import List

class Solution:
    def findMaxForm(self, strs: List[str], m: int, n: int) -> int:
        
        # 这里的n是第一维,m是第二维
        dp = [[0 for i in range(m + 1)] for j in range(n + 1)]

        items = self.init_item(strs)
        # 外层循环，遍历
        for zero_k, one_k in items:
            for i in range(m, zero_k - 1, -1):
                for j in range(n, one_k - 1, -1):
                    dp[i][j] = max(dp[i][j], dp[i - zero_k][j - one_k] + 1)

        return dp[m][n]

    
    def init_item(self, strs):

        items = []
        for item in strs:
            zero = 0
            one = 0
            for s in item:
                if s == "0":
                    zero += 1
                elif s == "1":
                    one += 1
            
            items.append((zero, one))

        return items