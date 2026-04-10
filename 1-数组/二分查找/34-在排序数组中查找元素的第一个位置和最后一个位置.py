

from typing import List


class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        
        if not nums:
            return (-1, -1)
        # 二分查找加上搜索
        # 或者二分查找加上区间扩张
        left = 0
        right = len(nums) - 1

        while left <= right:

            mid = (left + right) // 2

            if nums[mid] == target:
                # 则开始进行区间扩张
                left = mid  # 问题1：覆盖了二分查找的left变量，命名冲突易混淆
                right = mid # 问题1：同理，覆盖了二分查找的right变量

                # 向两边扩张
                # 问题2：越界风险！left-1可能<0（比如mid=0时），访问nums[-1]直接报错
                # 问题3：循环条件逻辑错误！应该先判断left-1有效，再比较值；且条件写反（会漏边界）
                while nums[left] == nums[left - 1]:
                    left -= 1
                # 问题2：同理，right+1可能>=len(nums)（比如mid是最后一个元素），访问nums[len(nums)]报错
                # 问题3：循环条件逻辑错误！
                while nums[right] == nums[right + 1]:
                    right += 1
                
                return (left, right)
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return (-1, -1)

"""
V0修复版
思路不是不行，思路挺好的，但是扩张的逻辑条件错误
但事实上，这个思路直观，但不够有效，这方面，应该要考虑左右边界问题，单独查找
"""

class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        if not nums:
            return (-1, -1)
        
        # 二分查找的指针（避免和扩张边界重名）
        binary_left = 0
        binary_right = len(nums) - 1

        while binary_left <= binary_right:
            mid = (binary_left + binary_right) // 2

            if nums[mid] == target:
                # 扩张的边界（单独命名，避免覆盖）
                left_bound = mid
                right_bound = mid

                # 左扩张：先判断下标有效，再判断值等于target
                while left_bound - 1 >= 0 and nums[left_bound - 1] == target:
                    left_bound -= 1
                # 右扩张：先判断下标有效，再判断值等于target
                while right_bound + 1 < len(nums) and nums[right_bound + 1] == target:
                    right_bound += 1
                
                return (left_bound, right_bound)
            elif nums[mid] < target:
                binary_left = mid + 1
            else:
                binary_right = mid - 1
        
        return (-1, -1)

"""
标准解法：分别查找左右边界

"""
class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        # 辅助函数：找左边界（第一个等于target的下标）
        def find_left():
            left = 0
            right = len(nums) - 1
            while left <= right:
                mid = (left + right) // 2
                if nums[mid] >= target:
                    # 找左边界：遇到>=target就收缩右边界，锁定更靠左的位置
                    right = mid - 1
                else:
                    # nums[mid] < target，目标在右侧
                    left = mid + 1
            # 循环结束后left是第一个>=target的位置，需验证是否有效
            if left < len(nums) and nums[left] == target:
                return left
            return -1
        
        # 辅助函数：找右边界（最后一个等于target的下标）
        def find_right():
            left = 0
            right = len(nums) - 1
            while left <= right:
                mid = (left + right) // 2
                if nums[mid] <= target:
                    # 找右边界：遇到<=target就收缩左边界，锁定更靠右的位置
                    left = mid + 1
                else:
                    # nums[mid] > target，目标在左侧
                    right = mid - 1
            # 循环结束后right是最后一个<=target的位置，需验证是否有效
            if right >= 0 and nums[right] == target:
                return right
            return -1
        
        left_idx = find_left()
        right_idx = find_right()
        return [left_idx, right_idx]
