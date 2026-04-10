
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

"""
V2
"""


class Solution:
    def countPrimes(self, n: int) -> int:
        # 最简单的办法就是嵌套，但是嵌套复杂度很高，最好使用筛来解决这个问题

        # 初始化
        if n < 2:
            return 0
        
        # 错误1：标记数组初始化完全搞反
        # 埃式筛应初始为 True（假设所有数是质数），再把 0、1 标为 False；V2 初始全 False，后续标记逻辑也反了
        isPrime = [False for i in range(n)]  
        
        # 错误2：循环范围和 index 含义错误
        # 1. 埃式筛只需遍历到 √n（无需遍历到 n），超过 √n 的数的倍数已被更小的数标记过
        # 2. index 应从 2 开始（0、1 不是质数），V2 从 0 开始遍历无意义
        for index in range(n):
            # 使用埃式筛

            # 错误3：start 计算错误（完全违背埃式筛逻辑）
            # 埃式筛中，质数 index 的倍数应从 index² 开始标记（避免重复）；V2 用 index+1 毫无道理
            start = index + 1
            
            # 错误4：end 计算致命错误（语法+逻辑）
            # 1. n 是整数，len(n) 会直接抛出 TypeError（整数无长度属性）
            # 2. 正确 end 应为 n（切片是左闭右开，标记到 n-1 即可）
            end = len(n) 
            
            # 错误5：step 计算错误（核心逻辑错误）
            # 埃式筛标记质数倍数的步长应为 index 本身（如 index=2，步长2，标记4、6、8...）；V2 用 end//index 步长完全混乱
            step = end // index

            # 错误6：赋值逻辑双重错误
            # 1. 切片赋值要求等长可迭代对象，直接赋值 True 会抛 TypeError（应赋值 [False]*长度）
            # 2. 埃式筛是把倍数标记为非质数（False），V2 标为 True，与初始化逻辑完全矛盾
            isPrime[start: end: step] = True
            

        return sum(isPrime)

"""
V2 修复版本
"""
import math 

class Solution:
    def countPrimes(self, n: int) -> int:
        # 最简单的办法就是嵌套，但是嵌套复杂度很高，最好使用筛来解决这个问题

        # 初始化
        if n < 2:
            return 0
        
        isPrime = [True for i in range(n)]
        isPrime[0] = False
        isPrime[1] = False

        for index in range(2, int(math.sqrt(n)) + 1):

            start = index ** 2
            end = n  
            step = index

            mark_count = (end - start - 1) // step + 1

            isPrime[start: end: step] = [False] * mark_count

        
        return sum(isPrime)

