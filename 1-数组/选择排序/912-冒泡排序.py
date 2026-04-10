


from typing import List

class Solution:
    # 最终调用接口
    def sortArray(self, nums: List[int]) -> List[int]:


        n = len(nums)

        for i in range(n - 1):
            
            # 找接下来所有解中的最小值，然后更换位置
            curr_min_index = i
            for j in range(i + 1, n):

                if nums[j] < nums[curr_min_index]:
                    curr_min_index = j

            nums[i], nums[curr_min_index] = nums[curr_min_index], nums[i]

        return nums
    