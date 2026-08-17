


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



# ======================================================
class Solution:
    def bubbleSort(self, nums):

        n = len(nums)

        # 给内部进行排序
        for i in range(n - 1):
            swapped = False

            for j in range(n - 1 - i):
                if nums[j] > nums[j + 1]:
                    nums[j], nums[j + 1] = nums[j + 1], nums[j]
                    swapped = True


            if not swapped:
                break

        return nums

# =====================================


class Solution:
    def bubbleSort(self, nums):

        n = len(nums)

        for i in range(n - 1):

            swapped = False

            for j in range(n - i - 1):

                if nums[j] > nums[j + 1]:
                    nums[j], nums[j + 1] = nums[j + 1], nums[j]
                    swapped = True

            if swapped == False:
                break

        return nums

