class Solution:
    def majorityElement(self, nums):
        # 迭代算法，最蠢的一集
        memo = {}

        for item in nums:
            if item not in memo:
                memo[item] = 1
            else:
                memo[item] += 1
        
        for key, value in memo.items():
            if value > len(nums) / 2:
                return key
            
    def majorityElement(self, nums) -> int:
        return self._majority_element_rec(nums, 0, len(nums) - 1)
    
    def _majority_element_rec(self, nums, left: int, right: int) -> int:
        # 基本情况：当数组只有一个元素时，该元素就是多数元素
        if left == right:
            return nums[left]
        
        # 分解：将数组分为左右两半
        mid = (left + right) // 2
        
        # 解决：递归地在左右两半中寻找多数元素
        left_majority = self._majority_element_rec(nums, left, mid)
        right_majority = self._majority_element_rec(nums, mid + 1, right)
        
        # 合并：如果左右两半的多数元素相同，直接返回
        if left_majority == right_majority:
            return left_majority
        
        # 如果不同，统计这两个候选元素在整个数组中的出现次数
        left_count = self._count_in_range(nums, left_majority, left, right)
        right_count = self._count_in_range(nums, right_majority, left, right)
        
        # 返回出现次数更多的元素
        return left_majority if left_count > right_count else right_majority
    
    def _count_in_range(self, nums, num: int, left: int, right: int) -> int:
        """统计指定元素在数组指定范围内的出现次数"""
        count = 0
        for i in range(left, right + 1):
            if nums[i] == num:
                count += 1
        return count

        
        