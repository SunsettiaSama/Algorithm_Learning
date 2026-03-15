
from typing import List


class Solution:
    def findLength(self, nums1: List[int], nums2: List[int]) -> int:
        
        size1 = len(nums1)
        size2 = len(nums2)
        dp = [[0 for _ in range(size2 + 1)] for _ in range(size1 + 1)]
        res = 0

        for i in range(1, size1 + 1):
            for j in range(1, size2 + 1):
                if nums1[i - 1] == nums2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1

                # 这里同max等效
                if dp[i][j] > res:
                    res = dp[i][j]

        return res