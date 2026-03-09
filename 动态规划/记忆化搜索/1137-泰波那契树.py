

class Solution:
    def tribonacci(self, n: int) -> int:

        memory = dict()

        def dfs(n):
            if n == 0: 
                return 0
            
            if n == 1:
                return 1
            
            if n == 2:
                return 1
            
            if n in memory:
                return memory[n]
            
            ans = dfs(n - 1) + dfs(n - 2) + dfs(n - 3)
            memory[n] = ans

            return ans
    
        return dfs(n)