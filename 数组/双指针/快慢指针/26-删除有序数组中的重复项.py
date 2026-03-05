

"""
=================
V0
=================
"""

from typing import List

class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        
        # ERROR：边界条件错误，len(nums) == 1时应返回1（长度），而非数组；且未处理空数组
        if len(nums) == 1:
            return nums
        
        # 首先遍历该数组

        slow = 0
        fast = 0

        slow_string = nums[0]  # ERROR：变量命名误导（数组元素是int，非string），且用值而非索引记录位置
        # slow用来标记不重复的数
        # fast用来标记重复数

        # ERROR：遍历方式错误，enumerate(nums[1:])返回的是切片后的索引，不是原数组索引，删除后会导致索引错位
        for fast, num in enumerate(nums[1: ]):
            curr_string = num
            # 表明有重复，删除该位置
            if curr_string == slow_string:
                del nums[fast]  # ERROR：遍历中删除元素会改变数组长度，导致后续索引错乱，且效率低（O(n²)）
        
        # ERROR：未返回最终长度，不符合题目要求



"""
=================
V0 修复版本，需要学习
=================
"""

class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        
        if not nums:
            return 0
        
        slow = 0

        for fast in range(1, len(nums)):

            if nums[fast] != nums[slow]:

                slow += 1
                nums[slow] = nums[fast]

        return slow + 1



"""
==================
V1
==================
"""
class Solution:
    def removeDuplicates(self, nums: list[int]) -> int:
        if not nums:
            return 0
        
        slow = 0 
        fast = 0

        while fast < len(nums):
            slow += 1  # ERROR: 初始slow=0（指向第一个有效元素），未判断就直接+1，跳过第一个元素，逻辑顺序完全错误
            fast += 2  # ERROR: fast步长设为2，无法逐个遍历数组检查重复项，且极易导致后续nums[fast]索引越界
            # 指针覆盖
            if nums[slow] != nums[fast]:  # ERROR: 1.fast可能已越界（如数组长度<2时）；2.逻辑颠倒，应先判断fast与slow指向元素是否不同，再移动slow
                nums[slow] = nums[fast]  # ERROR: 覆盖时机错误，且未处理fast越界的情况，会触发IndexError
        
        return slow + 1  # ERROR: 返回值计算错误，因slow移动逻辑错误，最终返回值远大于实际去重后的数组长度


class Solution:
    def removeDuplicates(self, nums: list[int]) -> int:
        if not nums:
            return 0
        
        slow = 0 
        fast = 1

        while fast < len(nums):

            if nums[fast] != nums[slow]:
                slow += 1
                nums[slow] = nums[fast]

            fast += 1
        
        return slow + 1


if __name__ == "__main__":


    solu = Solution()
    solu.removeDuplicates([0,0,1,1,1,2,2,3,3,4])


