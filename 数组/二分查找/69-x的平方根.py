
"""

V0版本，当时我们做过的手撕之一
"""


class Solution:
    def mySqrt(self, x: int) -> int:
        if x == 0:
            return 0
        if x == 1:
            return 1
        
        left = 0
        right = x // 2 + 1

        while left <= right:

            mid = (left + right) // 2
            # 这里中间有一个距离该如何处理，思考一下，比如2x2 = 4, 3x3 = 9, 那么5~8返回的结果都应该是2
            # 错误1：边界更新完全反了（核心逻辑错误）
            # mid² > x 说明mid太大，应缩小右边界（right=mid-1），而非扩大左边界
            if mid * mid > x:
                left = mid + 1
            # 错误2：mid² < x 说明mid偏小，应扩大左边界（left=mid+1），而非缩小右边界
            elif mid * mid < x:
                right = mid - 1
            elif mid * mid == x:
                return mid

        # 错误3：循环结束后返回值错误
        # 循环终止时left > right，right是最后一个满足mid² ≤x的合法值，返回left会得到错误结果
        return left

