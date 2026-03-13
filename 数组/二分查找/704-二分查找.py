


from typing import List


"""

V0版本尝试

"""
class Solution:
    def search(self, nums: List[int], target: int) -> int:

        # 二分查找的思路和双指针的对撞指针思路是不同的，请注意
        # 这里是要查找target是否存在于有序数组

        # 错误1：初始边界判断有漏洞（nums为空时nums[-1]/nums[0]会报错；未处理nums长度为1的场景）
        if target > nums[-1] or target < nums[0]:
            return -1

        left = 0
        right = len(nums) - 1

        while left < right:
            # 看看中间值是大是小

            # 错误2：mid计算公式完全错误（核心！）
            # 正确公式：mid = (left + right) // 2 或 (right - left) // 2 + left
            # 你写的+1会导致mid偏移，比如left=0、right=2时，正确mid=1，你的mid=2
            mid = (right - left) // 2 + 1

            if target > nums[mid]: 
                # 错误3：左边界更新不严谨（应left=mid+1，否则可能死循环）
                left = mid
            elif target < nums[mid]:
                # 错误4：右边界更新错误（应right=mid-1，否则会遗漏/死循环）
                right = mid
            else:
                return mid
            
            # 错误5：多余且错误的手动break（二分循环应靠left/right关系自然终止，手动break会漏掉目标）
            if left in (right, right + 1):
                break
            
        # 错误6：循环结束后未检查最后一个节点（left==right时，可能刚好是target）
        return -1


"""

V1版本尝试

"""
class Solution:
    def search(self, nums: List[int], target: int) -> int:

        if len(nums) == 0:
            return -1
        
        left_index = 0
        right_index = len(nums) - 1

        while left_index <= right_index: # 易错：等于
            
            mid_index = (right_index + left_index) // 2 # 易错，对折区间的公式是加号

            if target == nums[mid_index]:
                return mid_index
            elif target > nums[mid_index]:
                left_index = mid_index + 1
            elif target < nums[mid_index]:
                right_index = mid_index - 1
        
        return -1





