


"""
===================
V0
===================
"""


class Solution:
    def countTriples(self, n: int) -> int:
        
        counts = 0
        
        for a in range(n):  # ERROR: 1.范围错误（range(n)是0~n-1，三元数a应为正整数，需从1开始到n；2.漏了n本身，应是range(1, n+1)）
            for b in range(a, n):  # ERROR: 1.范围错误（同a，应是1~n；2.限制b≥a会导致后续乘2的补偿逻辑不严谨，且漏标n）
                for c in range(b, n):  # ERROR: 1.范围错误（同a，应是1~n；2.限制c≥b会导致漏查c<a或c<b的情况，而c作为斜边必然最大，此点逻辑对但范围错）
                    if a ** 2 + b ** 2 == c ** 2:
                        counts += 1

        return counts * 2  # ERROR: 补偿逻辑错误（因a/b范围错误+起始为0，乘2无法修正统计偏差，且若存在a=b的情况（实际正整数中无）会重复统计）




"""
===================
V1
===================
"""


class Solution:
    def countTriples(self, n: int) -> int:
        
        counts = 0

        for a in range(n+1):
            for b in range(a + 1, n + 1):
                for c in range(b + 1, n + 1):
                    if a **2 + b **2 == c ** 2:
                        counts += 1
        
        return counts # ERROR: 补偿逻辑错误，忘记乘以2




"""
===================
V2
===================
"""


class Solution:
    def countTriples(self, n: int) -> int:
        
        counts = 0

        for a in range(n+1):
            for b in range(a + 1, n + 1):
                for c in range(b + 1, n + 1):
                    if a **2 + b **2 == c ** 2:
                        counts += 1
        
        return counts * 2


"""
===================
V3
===================
"""
class Solution:
    def countTriples(self, n: int) -> int:
        
        counts = 0

        for a in range(1, n+1):
            for b in range(1, n+1):
                squre = a ** 2 + b ** 2  # ERROR: 变量名拼写错误（squre → square），虽不影响运行，但违反语法规范，降低可读性
                if squre > n ** 2:
                    break  # 注：此break逻辑本身无错（b递增，sum递增，超过n²后无需继续）

                # ERROR: 浮点数精度问题——用**0.5计算平方根会有精度误差，导致部分完全平方数漏判（如大数值的完全平方数）
                if (squre ** 0.5) ** 2 == squre:
                    counts += 1
        
        return counts



"""
===================
V4
===================
"""

from math import isqrt

class Solution:
    def countTriples(self, n: int) -> int:
        
        counts = 0

        for a in range(1, n+1):
            for b in range(a, n+1):
                squre = a ** 2 + b ** 2 
                if squre > n ** 2:
                    break  
                if isqrt(squre)** 2 == squre:
                    counts += 1
        
        return counts * 2
