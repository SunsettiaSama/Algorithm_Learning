
from typing import List


class Solution:
    def findLength(self, nums1: List[int], nums2: List[int]) -> int:
        m, n = len(nums1), len(nums2)
        # 初始化DP表，维度为 (m+1) x (n+1)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        ans = 0

        # 从1开始遍历，这样 i-1 和 j-1 就不会越界
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                # 状态转移
                if nums1[i - 1] == nums2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                    # 更新全局最大值
                    ans = max(ans, dp[i][j])
                # 如果元素不相等，dp[i][j] 默认就是0

        return ans
    

from typing import List

class Solution:
    def findLength(self, A: List[int], B: List[int]) -> int:
        m, n = len(A), len(B)
        # 让 B 作为较短的数组，减少空间开销
        if m < n:
            A, B = B, A
            m, n = n, m
        dp = [0] * (n + 1)
        max_len = 0
        for i in range(1, m + 1):
            # 从后向前更新，避免覆盖本轮需要的上一行值
            for j in range(n, 0, -1):
                if A[i-1] == B[j-1]:
                    dp[j] = dp[j-1] + 1
                    max_len = max(max_len, dp[j])
                else:
                    dp[j] = 0
        return max_len