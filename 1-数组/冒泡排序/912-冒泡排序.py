


from typing import List

class Solution:
    # 最终调用接口
    def sortArray(self, nums: List[int]) -> List[int]:


        n = len(nums)

        for i in range(n - 1):

            for j in range(n - 1 - i):
                if nums[j] > nums[j + 1]:
                    nums[j], nums[j + 1] = nums[j + 1], nums[j]

        
        return nums