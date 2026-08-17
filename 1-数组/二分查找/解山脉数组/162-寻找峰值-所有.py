from typing import List

class Solution:
    def findAllPeaks(self, nums: List[int]) -> List[int]:
        n = len(nums)
        if n == 0:
            return []
        
        res = []
        
        for i in range(n):
            # 检查左边：如果是第一个元素，或者大于左边
            left_ok = (i == 0) or (nums[i] > nums[i - 1])
            # 检查右边：如果是最后一个元素，或者大于右边
            right_ok = (i == n - 1) or (nums[i] > nums[i + 1])
            
            if left_ok and right_ok:
                res.append(i)  # 或者 append(nums[i])，看你想要索引还是值
        
        return res



# ================================================
class Solution:
    def findAllPeaks(self, nums: List[int]) -> List[int]:
        n = len(nums)
        if n == 0:
            return []

        res = []

        for i in range(n):
            # 如果下一个元素比当前元素小 则认为是峰值
            left_ok = (i == 0) or (nums[i] > nums[i - 1])
            right_ok = (i == 0) or (nums[i] < nums[i + 1])

            if left_ok and right_ok:
                res.append(nums[i])


        return nums



# 测试用例
sol = Solution()
print(sol.findAllPeaks([1, 3, 2, 4, 1, 5, 1]))  # 输出: [1, 3, 5]
print(sol.findAllPeaks([1, 2, 3, 4, 5]))        # 输出: [4] (最后一个元素是峰值)
print(sol.findAllPeaks([5, 4, 3, 2, 1]))        # 输出: [0] (第一个元素是峰值)


