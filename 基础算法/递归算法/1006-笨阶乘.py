


class Solution:
    def clumsy(self, n: int, start_n: int = None) -> int:

        # ERROR：递归终止条件错误，clumsy(1)=1、clumsy(0)无意义，但n=2/3/4时终止逻辑也不适用
        # 比如n=1应返回1，n=2应返回2×1=2，而不是统一返回1
        if n == 0 or n == 1:
            return 1
        
        # ERROR：start_n每次递归都被重置为当前n，导致无法判断当前处于“乘/除/加/减”哪个循环步骤
        # 比如初始n=4，start_n=4；递归到n=3时，start_n又被设为3，完全破坏循环逻辑
        start_n = n

        # ERROR：核心逻辑错误——用start_n%n判断运算类型完全不合理
        # start_n=n时，start_n%n=0永远成立，只会走第一个分支（乘法），无法实现“×÷+-”循环
        if start_n % n == 0:
            return n * self.clumsy(n - 1)
        elif start_n % n == 1:
            return n // self.clumsy(n - 1)
        elif start_n % n == 2:
            return n + self.clumsy(n - 1)
        elif start_n % n == 3:
            return n - self.clumsy(n - 1)


