
"""
===================
V0
===================
"""

class Solution:
    def countPrimes(self, n: int) -> int:
        # 先处理边界情况
        if n < 2:
            return True  # ERROR: 1.返回值错误（n<2无质数应返回0）；2.类型错误（题目要求int，此处返回bool）
        
        isPrime = [1] * n

        # 0，1是质数  # ERROR: 注释逻辑错误，0和1不是质数
        isPrime[0] = isPrime[1] = 0

        max_index = n ** 0.5 + 1  # ERROR: 1.未转整数（range不支持浮点数）；2.变量命名语义错误（应为筛选上限而非索引）
        for index in range(2, max_index):  # ERROR: range结束值为浮点数，运行会报TypeError
            
            start_pos = index ** 2
            end_pos = max_index  # ERROR: 标记结束位置错误，应到n而非max_index，漏标大量合数
            step = index

            mark_count = (end_pos - start_pos) // step  # ERROR: 1.数量计算少+1（导致数组长度不匹配）；2.依赖错误的end_pos
            isPrime[start_pos: end_pos: step] = [0] * mark_count  # ERROR: 核心逻辑缺失（未判断当前数是否为质数就标记）

        return sum(isPrime)
    

"""
===================
V1
===================
"""
class Solution:
    def countPrimes(self, n: int) -> int:
        # 边界条件
        if n < 2:
            return 0
        
        isPrime = [1] * n

        isPrime[0] = isPrime[1] = 0

        max_index = int(n ** 0.5) + 1
        for index in range(2, max_index):

            start_pos = index ** 2
            end_pos = n
            step = index

            mark_count = (end_pos - start_pos - 1) // step + 1
            isPrime[start_pos: end_pos: step] = [0] * mark_count

        return sum(isPrime)
    