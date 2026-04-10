class Solution:
    def __init__(self):
        self.memo = {}

    # 递归体O(nlogn)
    def myPowV0(self, x: float, n: int) -> float:
        # 递归终止条件
        if n == 1:
            return x
        
        # 递归体
        return x * self.myPow(x, n - 1)
    
    # 迭代体O(n)
    def myPowV1(self, x: float, n: int) -> float:
        # 处理两种特殊情况，即f(0)和f(1)
        if n == 0:
            return 1
        if n == 1:
            return x
        
        ai = x
        for i in range(1, abs(n)):
            ai *= x 
        
        return ai if n > 0 else  1 / ai
    
    # 分治算法O(logn)
    def myPowV2(self, x, n):
        
        # 递归体终止条件
        if n == 1:
            return x
        if n == -1:
            return 1 / x
        
        # 分解部分
        mid = int(n // 2)

        left = mid
        right = n - mid

        # 递归体 + 合并部分
        return self.myPowV2(x, left) * self.myPowV2(x, right)
    
    # 分治算法 + 记忆体 O(logn / 2)
    def myPowV2(self, x, n):
        # 记忆体
        if (x, n) in self.memo:
            return self.memo[(x, n)]

        # 递归体终止条件
        if n == 0:
            self.memo[(x, 0)] = 1
            return 1
        if n == 1:
            self.memo[(x, 1)] = x
            return x
        if n == -1:
            self.memo[(x, -1)] = 1 / x
            return 1 / x
        
        # 分解部分
        mid = int(n // 2)

        left = mid
        right = n - mid

        # 递归体 + 合并部分
        # 记忆体维护
        result = self.myPowV2(x, left) * self.myPowV2(x, right)
        self.memo[(x, n)] = result
        return result
    

        
    
    # 分析：
    # 第n项为x ** n
    # 但假设我们没有 ** 符号
    # 那就有 f(x, n) = x * f(x, n - 1)        -> 递归多项式
    # 终止条件为 n = 1 时，x = n               -> 递归终止条件
    # 可以进行分解与合并
    # 比如说以2为基底进行合并与分解。

if __name__ == "__main__":
    s = Solution()
    print(s.myPow(2, -2))