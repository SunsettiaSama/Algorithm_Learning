from typing import TYPE_CHECKING
from typing import List








class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:

        n = len(nums)
        for index1 in range(n):
            for index2 in range(n):
                if index1 == index2: 
                    continue

                res = nums[index1] + nums[index2]
                if res == target:
                    return index1, index2





"""
V0

"""

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:

        n = len(nums)

        for index1 in range(n):
            for index2 in range(n):

                if index1 == index2:
                    continue
                
                if nums[index1] + nums[index2] == target:
                    return index1, index2



