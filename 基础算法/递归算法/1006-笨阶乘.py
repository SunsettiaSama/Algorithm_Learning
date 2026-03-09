


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

"""
V0，数学解版本，最终的解是可以用归纳法推导出一个等式的
"""


class Solution:
    def clumsy(self, n: int) -> int:
        # 处理n≤4的特殊情况
        if n == 1:
            return 1
        elif n == 2:
            return 2
        elif n == 3:
            return 6
        elif n == 4:
            return 7
        
        # 处理n>4的情况
        mod = n % 4
        if mod == 0:
            return n + 1
        elif mod == 1 or mod == 2:
            return n + 2
        else:  # mod ==3
            return n - 1

"""
V0版本：栈解法版本
"""

class Solution:
    def clumsy(self, n: int) -> int:
        if n == 0:
            return 0
        # 初始化栈，先放入第一个数n
        stack = [n]
        # 操作符循环：* / + - 对应索引0,1,2,3
        op_idx = 0
        
        # 从n-1遍历到1
        for num in range(n-1, 0, -1):
            if op_idx == 0:  # 乘法
                stack.append(stack.pop() * num)
            elif op_idx == 1:  # 除法（向零取整，用int(a/b)而非//）
                # 注意：Python的//是向下取整，int(a/b)是向零取整，符合题目要求
                stack.append(int(stack.pop() / num))
            elif op_idx == 2:  # 加法
                stack.append(num)
            elif op_idx == 3:  # 减法（入栈负数）
                stack.append(-num)
            # 切换下一个操作符（循环）
            op_idx = (op_idx + 1) % 4
        
        # 栈中所有元素求和即为结果
        return sum(stack)



"""
V0
递归解法版本

"""

class Solution:
    def clumsy(self, n: int) -> int:
        # 操作符循环：* / + -，用索引控制（可选，更通用）
        def dfs(num):
            if num == 0:
                return 0
            if num == 1:
                return 1
            if num == 2:
                return 2  # 2*1，无后续运算，直接返回
            if num == 3:
                return 6  # 3*2/1=6，触发终止，不进入递归公式
            
            # 遍历当前num的后续数字，按操作符循环计算
            # ===========================
            # 这里注意，一定要按照四个符号为循环来写，不循环的话，会变成括号后再乘除，然后就炸了
            # ===========================
            # 所以递归问题的正确等式应该是f(n) = n * (n-1) / (n-2) + (n-3) - f(n - 4)
            # 不过这么做还有地板除法的问题，也需要考虑清楚这个问题
            # ===========================
            return num * (num - 1) // (num - 2) + (num - 3) - dfs(num - 4)
    
        return dfs(n)
