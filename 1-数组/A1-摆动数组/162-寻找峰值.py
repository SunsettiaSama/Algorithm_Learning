

from typing import List

class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        
        return self.binarySearch_peak(nums)
    
    def binarySearch_peak(self, nums):

        left = 0
        # =============问题===========
        # 开区间，不能直接使用 right = len(nums)
        right = len(nums) - 1 

        while left < right:
            mid = (left + right) // 2

            if nums[mid] < nums[mid + 1]:
                # 右侧存在峰值
                left = mid + 1
            else:
                right = mid

        return left



