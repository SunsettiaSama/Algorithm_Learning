

class Solution:
    


    def fact(self, n):
        
        # 终止条件：
        if n == 1 or n == 0:
            return 1
        
        return n * self.fact(n-1)