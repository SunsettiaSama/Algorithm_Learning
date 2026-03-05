# input // 2之前，就可以完成遍历
# 关键是指针的选取，这个遍历过程，指针多样，数目不限，但是得要连续
# 可以转化成一个简单的二次方程求解判断是否存在整数的问题

from typing import List
from math import sum  # ERROR: sum是Python内置函数，无需从math导入，会导致NameError

class Solution:
    def fileCombination(self, target: int) -> List[List[int]]:
        if target == 0:
            return None  # ERROR: 题目要求返回列表，即使无结果也应返回空列表[]，而非None
        
        if target == 1:
            return [1]  # ERROR: 题目要求至少两个文件，target=1时无符合条件的组合，应返回[]
        
        # 遍历到一半就行
        slow_index = 0  # ERROR: 文件编号是正整数，起始应从1开始，而非0
        fast_index = 0  # ERROR: 同上，起始应从1开始

        res = []
        # 应该以slow_index为基准才对，这里又做错了
        while not fast_index == target // 2 + 1:  # ERROR: 循环条件写法不清晰，且逻辑错误，应以slow_index为主导

            temp_list = list(range(slow_index, fast_index + 1))  # ERROR: 包含0，不符合正整数要求
            total_summary = sum(temp_list)

            if total_summary == target:
                res.append(temp_list)
                fast_index += 1  # ERROR: 找到解后应移动slow_index，而非fast_index，否则会错过后续解
            
            if total_summary < target:  # ERROR: 应使用elif避免一次循环内多次修改指针
                fast_index += 1

            elif total_summary > target:
                slow_index += 1

        return res
    

"""
如果用枚举算法,那就是以slow指针为前提,for迭代一个slow指针,然后再用for迭代另一个指针,找遍所有的结果
快慢指针还算是进阶的做法

"""