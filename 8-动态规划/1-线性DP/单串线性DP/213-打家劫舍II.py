from typing import List

"""
V0 思路复现
"""
class Solution:
    def rob(self, nums: List[int]) -> int:
        
        n = len(nums)

        if n == 0:
            return 0
        elif n == 1:
            return nums[1]  # ERROR 1：索引越界！只有1个元素时索引是0，应该return nums[0]
        elif n == 2:
            return max(*nums)

        # 首尾截断，逻辑复用
        def helper(arr):
            length = len(nums)  # ERROR 2：完全错了！helper处理的是传入的arr，不是原nums，应该len(arr)
            if length == 2:
                return max(*arr)
            
            dp = [0 for i in range(length)]
            dp[0] = nums[0]  # ERROR 3：用了原数组nums！应该用传入的arr[0]
            dp[1] = max(*nums[: 2])  # ERROR 4：用了原数组前两位！应该用arr[0]和arr[1]
            for i in range(2, length):
                dp[i] = max(dp[i - 1], dp[i - 2] + arr[i])

            return dp[length - 1]
        
        return max(helper(nums[1: ]), helper(nums[: -1]))
    


from typing import List

"""
V0 修改
"""
class Solution:
    def rob(self, nums: List[int]) -> int:
        
        n = len(nums)

        if n == 0:
            return 0
        elif n == 1:
            return nums[0]  # ERROR 1：索引越界！只有1个元素时索引是0，应该return nums[0]
        elif n == 2:
            return max(*nums)

        # 首尾截断，逻辑复用
        def helper(arr):
            length = len(arr)  # ERROR 2：完全错了！helper处理的是传入的arr，不是原nums，应该len(arr)
            if length == 2:
                return max(*arr)
            
            dp = [0 for i in range(length)]
            dp[0] = arr[0]  # ERROR 3：用了原数组nums！应该用传入的arr[0]
            dp[1] = max(*arr[: 2])  # ERROR 4：用了原数组前两位！应该用arr[0]和arr[1]
            for i in range(2, length):
                dp[i] = max(dp[i - 1], dp[i - 2] + arr[i])

            return dp[length - 1]
        
        return max(helper(nums[1: ]), helper(nums[: -1]))