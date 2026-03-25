
from typing import List


class Solution:
    def predictTheWinner(self, nums: List[int]) -> bool:
        


        # dp应该定义为还剩slow、fast区间时，玩家一能成为赢家的可能性 ERROR：出发点就错了
        """
        现在轮到你拿牌了，在剩下 slow ~ fast 这堆数字里，
        你最后能比对手【多赢几分】
        """
        # dp[slow][fast] = 在数组第i个区间到第j个区间内，当前玩家能比对手多拿多少分
        size = len(nums)
        dp = [[0 for i in range(size)] for j in range(size)]

        for length in range(1, size + 1):
            for slow in range(size):
                fast = length + slow - 1

                if fast >= size:
                    break

                # 区间有了，那么状态转移方程呢
                if slow == fast:
                    dp[slow][fast] = nums[slow]
                
                else:
                    dp[slow][fast] = max(
                        nums[slow] - dp[slow + 1][fast], 
                        nums[fast] - dp[slow][fast - 1]
                    )
        
        return dp[0][size - 1] >= 0