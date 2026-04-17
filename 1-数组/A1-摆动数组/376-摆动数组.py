




from typing import List

class Solution:
    def wiggleMaxLength(self, nums: List[int]) -> int:
        # 主函数：流程调度
        if self._is_short_array(nums):
            return len(nums)
        
        return self._count_wiggle(nums)

    def _is_short_array(self, nums):
        return len(nums) <= 1
    
    def _get_trend(self, a: int, b: int) -> int:

        diff = b - a
        if diff > 0:
            return 1
        elif diff < 0:
            return -1
        else:
            return 0
    

    def _count_wiggle(self, nums):
        max_len = 1
        prev_trend = 0

        for i in range(1, len(nums)):
            curr_trend = self._get_trend(nums[i - 1], nums[i])

            if curr_trend != 0 and curr_trend != prev_trend:
                max_len += 1
                prev_trend = curr_trend
        
        return max_len

"""
V0 手搓

"""

from typing import List

class Solution:
    def wiggleMaxLength(self, nums: List[int]):
        # 需要计算子序列的长度
        if self._is_short_array(nums):
            return len(nums)
        
        return self._count_wiggle(nums = nums)

    def _get_trend(self, a, b):
        # 【逻辑无错，但定义不直观】a是前一个数，b是后一个数
        # a-b>0 代表 前>后（下降），返回1；a-b<0代表前<后（上升），返回-1
        # 趋势符号不影响交替判断，这个函数本身没问题
        if a - b > 0:
            return 1
        elif a - b < 0:
            return -1
        else:
            return 0

    def _is_short_array(self, nums):
        # 【完全正确】边界判断模块
        return len(nums) <= 1
    
    def _count_wiggle(self, nums):
        max_len = 1
        prev_trend = 0

        for i in range(1, len(nums)):
            curr_trend = self._get_trend(nums[i - 1], nums[i])
            # ==================== 【核心致命BUG】 ====================
            # 错误原因：没有过滤 curr_trend == 0（两个数相等的情况）
            # 相等的元素没有摆动，**绝对不能计数**，但你的代码会把它当成有效转折！
            # 正确条件：必须同时满足 趋势≠0 且 趋势和上一次不同
            # ==========================================================
            if curr_trend != prev_trend:
                # 认为发生了有效转折
                max_len += 1
                prev_trend = curr_trend
        
        return max_len