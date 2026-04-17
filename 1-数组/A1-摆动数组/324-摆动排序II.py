


from typing import List

class Solution:
    def wiggleSort(self, nums: List[int]) -> None:
        # 【错误1】函数定义返回None，这里写 return nums 完全违反题意！
        # 【关键】LC324要求**原地修改数组**，不能返回任何值
        if self.is_short_nums(nums):
            return nums
        
        # 【错误2】split_array内部排序了，但分割的mid计算错误（下方标注）
        left_arr, right_arr = self.split_array(nums)

        # 【错误3】调用了合并函数，但没有把结果赋值给原数组nums
        # 原地修改必须做 nums[:] = 合并结果，否则原数组无变化
        # 【错误4】再次return 结果，违反函数返回None的要求
        return self.merge_array(left_arr, right_arr)


    def is_short_nums(self, nums):
        # 【模块正确】边界判断无问题
        return len(nums) <= 1
    
    def split_array(self, nums):
        # 【模块正确】排序操作没问题
        sorted_nums = sorted(nums)
        # 【核心致命错误】LC324分割中点必须是 (len(nums)+1) // 2
        # 你用的 len//2 会导致奇数长度数组左半部分少1个元素，最终填充错位/越界
        mid = len(nums) // 2

        # 左右区间
        left_arr, right_arr = sorted_nums[: mid], sorted_nums[mid: ]

        # 【操作正确】逆序防止重复元素相邻，这个思路是对的
        return left_arr[::-1], right_arr[::-1]
    
    def merge_array(self, left_arr, right_arr):
        # 【合并模块全逻辑错误】这是最严重的问题，交替填充逻辑完全错误
        ans_arr = []
        ptr = 0

        epoch = max(len(left_arr), len(right_arr))
        # 【错误5】遍历范围错误，不应该只遍历left_arr长度
        for i in range(len(left_arr)):
            ans_arr.append(left_arr[ptr])

            # 【错误6】ptr初始是0，第一次循环就判断==epoch，永远不会触发
            if ptr == epoch:
                break
            # 【错误7】索引越界风险：ptr+1后直接取right_arr[ptr]，超出right_arr长度直接报错
            ptr += 1
            ans_arr.append(right_arr[ptr])

        # 【错误8】无法处理左右数组长度不一致的情况（奇数长度必出现）
        # 【错误9】没有按照 偶数位放左、奇数位放右 的规则填充

        return ans_arr



"""
V0 修复版
错的很多，需要思考一下
"""

from typing import List

class Solution:
    def wiggleSort(self, nums: List[int]) -> None:
        # 【错误1】函数定义返回None，这里写 return nums 完全违反题意！
        # 【关键】LC324要求**原地修改数组**，不能返回任何值
        if self.is_short_nums(nums):
            return
        
        sorted_arr = self.sorted(nums)
        # 【错误2】split_array内部排序了，但分割的mid计算错误（下方标注）
        left_arr, right_arr = self.split_array(nums)

        # 【错误3】调用了合并函数，但没有把结果赋值给原数组nums
        # 原地修改必须做 nums[:] = 合并结果，否则原数组无变化
        # 【错误4】再次return 结果，违反函数返回None的要求
        return self.merge_array(left_arr, right_arr)

    def sorted(self, nums):
        return sorted(nums)

    def is_short_nums(self, nums):
        # 【模块正确】边界判断无问题
        return len(nums) <= 1
    
    def split_array(self, sorted_nums):
        # 【模块正确】排序操作没问题
        # 【核心致命错误】LC324分割中点必须是 (len(nums)+1) // 2
        # 你用的 len//2 会导致奇数长度数组左半部分少1个元素，最终填充错位/越界
        mid = (len(sorted_nums) + 1) // 2

        # 左右区间
        left_arr, right_arr = sorted_nums[: mid], sorted_nums[mid: ]

        # 【操作正确】逆序防止重复元素相邻，这个思路是对的
        return left_arr[::-1], right_arr[::-1]
    
    def merge_array(self, left_arr, right_arr):
        # 【合并模块全逻辑错误】这是最严重的问题，交替填充逻辑完全错误
        ans_arr = []
        ptr = 0

        epoch = max(len(left_arr), len(right_arr))
        # 【错误5】遍历范围错误，不应该只遍历left_arr长度
        for i in range(len(left_arr)):
            ans_arr.append(left_arr[ptr])

            # 【错误6】ptr初始是0，第一次循环就判断==epoch，永远不会触发
            if ptr == epoch:
                break
            # 【错误7】索引越界风险：ptr+1后直接取right_arr[ptr]，超出right_arr长度直接报错
            ptr += 1
            ans_arr.append(right_arr[ptr])

        # 【错误8】无法处理左右数组长度不一致的情况（奇数长度必出现）
        # 【错误9】没有按照 偶数位放左、奇数位放右 的规则填充

        return ans_arr


"""
V0 修复版

"""

from typing import List
class Solution:
    def wiggleSort(self, nums: List[int]) -> None:

        if self.is_short_array(nums):
            return 
        
        sorted_nums = sorted(nums)
        left, right = self.split_array(sorted_nums)
        self.merge_wiggle(nums, left, right)
        
    def is_short_array(self, nums):
        return len(nums) <= 1
    
    def split_array(self, nums):

        mid = (len(nums) + 1) // 2 # 左半数组多一个,可以去填谷底,谷底一定是偶数下标,这注定了
        # 逆序
        left = nums[:mid]
        right = nums[mid:]

        return left[::-1], right[::-1]
    
    def merge_wiggle(self, nums, left, right):
        
        n = len(nums)
        for i in range(n):
            if i % 2 == 0:  # 偶数，放波谷
                nums[i] = left[i // 2]
            else:
                nums[i] = right[i // 2]

    