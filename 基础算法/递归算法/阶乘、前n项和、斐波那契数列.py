
class Solution1:
    def __init__(self, *args, **kwargs, ):
        super().__init__(*args, **kwargs, )
        self.cache = {}
        return 
    
    def fact(self, n):

        # 终止条件:
        if n == 1 or n == 0:
            return 1
        
        # 递归体实现
        return n * self.fact(n-1)
    
    # 前n项和
    def former_n(self, n):
        # 终止条件
        if n == 1:
            return 1
        # 子问题
        return n + self.former_n(n - 1)

    # 斐波那契数列
    def fib(self, n):
        # 终止条件
        # 斐波那契数列有两个终止条件
        if n == 1:
            return 1
        if n == 2:
            return 2
        
        return self.fib(n - 1) + self.fib(n - 2)

    def fib_with_memo(self, n):
        """
        计算斐波那契数列的第n项（记忆化递归实现）
        使用缓存避免重复计算
        """
        # 检查缓存中是否已有结果
        if n in self.cache:
            return self.cache[n]
        
        # 终止条件
        if n == 1:
            result = 1
        elif n == 2:
            result = 2
        else:
            # 递归计算并缓存结果
            result = self.fib(n - 1) + self.fib(n - 2)
        
        # 将结果存入缓存
        self.cache[n] = result
        return result
    
    def fib_with_iter(self, n):
        if n == 1:
            return 1
        if n == 2:
            return 2
        
        ai = 1
        aj = 2
        for i in range(3, n):
            ai, aj = aj, ai + aj # 最后一步的输出为fn-2 fn-1，因此需要额外的处理
        
        return ai + aj
    
    # 其实n项式都可以用这种方法解决
    # 其和无穷级数之间还是有些不一样
    # n项有限毕竟

if __name__ == "__main__":
    s = Solution1()
    print(s.fib_with_iter(100))
        