
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

"""
V0 手搓

"""

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:


        left_index = 0
        right_index = len(nums) - 1

        # 创建哈希映射，以保证索引的正确
        # 字典映射不太好完成，因为键不唯一，只有idx是唯一的，也就是需要用num反向查找idx
        # 对撞指针仅能针对有序数组
        nums_hash = [(nums[idx], idx) for idx in range(len(nums))]
        nums_hash = sorted(nums_hash, key = lambda x: x[0])

        while left_index < right_index:
            
            curr_sum = nums_hash[left_index][0] + nums_hash[right_index][0]

            if curr_sum == target: # 我说怎么无限循环了。注意，找到了结果解，一定要进一步地挪动指针，千万别忘了这个小细节。
                left_index += 1
                right_index -= 1
                return (nums_hash[left_index][1], nums_hash[right_index][1])
            

            elif curr_sum < target:
                left_index += 1 # 有序，左加右减

            elif curr_sum > target:
                right_index -= 1
            
            if left_index >= right_index:
                break





        



