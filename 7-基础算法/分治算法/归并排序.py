
from typing import List

class Solution:


    def merge(self, left_array, right_array):

        result_array = []
        # 对当前分解的两个结果进行排序
        # 合并
        while left_array and right_array:
            if left_array[0] <= right_array[0]:
                result_array.append(left_array.pop(0))
            else:
                result_array.append(right_array.pop(0))
        
        while left_array:
            result_array.append(left_array.pop(0))

        while right_array:
            result_array.append(right_array.pop(0))

        return result_array
    
    def mergeSort(self, nums):
        """该函数为递归主体，第i步中 -> 拆开 -> 排序 -> 合并 -> 返回"""
        # 递归

        # 递归终止条件当仅有一个元素时，视为有序
        if len(nums) == 1:
            return nums
        
        # 分解
        mid = len(nums) // 2
        left_array, right_array = nums[:mid], nums[mid: ]

        # 排序并且合并
        left_array = self.mergeSort(left_array)
        right_array = self.mergeSort(right_array)

        return self.merge(left_array, right_array)

    # 最终调用接口
    def sortArray(self, nums: List[int]) -> List[int]:
        return self.mergeSort(nums)

if __name__ == "__main__":
    s = Solution()
    print(s.sortArray([12, 2, 5, 7]))