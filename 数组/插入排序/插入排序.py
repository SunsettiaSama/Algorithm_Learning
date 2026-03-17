

# 插入排序等于 打扑克牌前整理牌面

class Solution:
    def sortArray(self, nums):

        n = len(nums)

        for i in range(1, n):

            current = nums[i]

            j = i - 1


            while j >= 0 and nums[j] > current:
                nums[j + 1] = nums[j]
                j -= 1

            nums[j + 1] = current

        return nums
    