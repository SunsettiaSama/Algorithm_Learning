from typing import List


class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:


        # 搜索插入的位置，要求logn复杂度
        # 那好说，二分查找，查找对象为可以插入的索引index

        left = 0
        right = len(nums) - 1

        if target < nums[0]:
            return 0
        if target > nums[-1]:
            return len(nums)

        while left <= right:

            mid = (left + right) // 2
            
            # 检查中间值大还是小

            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        # 注意，这里是左侧为插入点，因为一旦跳出循环，则有left > right
        # 那么，此时left和right仅相差1，且左侧为right，右侧为left，现在要返回右侧
        return left
    
        
