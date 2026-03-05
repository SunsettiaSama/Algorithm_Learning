
from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:

        left_index = 0
        right_index = len(nums) - 1

        data_dict = sorted([(nums[i], i) for i in range(len(nums))], key = lambda x: x[0])

        while left_index < right_index:
            
            left_num = data_dict[left_index][0]
            right_num = data_dict[right_index][0]
            
            if left_num + right_num == target:
                return data_dict[left_index][1], data_dict[right_index][1]
            elif left_num + right_num < target:
                left_index += 1
            elif left_num + right_num > target:
                right_index -= 1
        
        return -1


