from typing import List

class Solution:
    def shellSort(self, nums: List[int]) -> List[int]:
        size = len(nums)
        gap = size // 2  # 初始间隔设为数组长度的一半

        # 不断缩小gap，直到gap为0
        while gap > 0:
            # 从gap位置开始，对每个元素进行组内插入排序
            for i in range(gap, size):
                temp = nums[i]  # 记录当前待插入的元素
                j = i
                # 在组内进行插入排序，将比 temp 大的元素向后移动
                while j >= gap and nums[j - gap] > temp:
                    nums[j] = nums[j - gap]  # 元素后移
                    j -= gap    # 向前跳 gap 步
                nums[j] = temp  # 插入到正确位置
            # 缩小 gap，通常取 gap 的一半
            gap //= 2

        return nums  # 返回排序后的数组

    def sortArray(self, nums: List[int]) -> List[int]:
        """排序接口，调用shellSort方法"""
        return self.shellSort(nums)


"""
V1 手搓

"""
from typing import List

class Solution:
    def shellSort(self, nums: List[int]) -> List[int]:
        size = len(nums)
        gap = size // 2  # 初始间隔设为数组长度的一半

        while gap > 0:
            for i in range(gap, size):
                temp = nums[i]

                j = i
                


    