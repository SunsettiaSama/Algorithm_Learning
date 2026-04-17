
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

"""
V1
"""

class Solution:
    def mySqrt(self, x: int) -> int:

        if x == 0:
            return 0
        if x == 1:
            return 1
        

        # 使用二分查找
        left_index = 0
        right_index = x // 2

        while left_index < right_index: # 这里有个问题，需要小于等于，而不是小于，小于的话边界条件错误
            # 即如果是小于，则最后一个数字，left == right时，最后一个数没有得到正确的检查

            mid_index = (left_index + right_index) // 2
            mid_square = mid_index * mid_index

            # 更新两指针
            if mid_square < x:
                left_index = mid_index + 1
            elif mid_square > x:
                right_index = mid_index - 1
            else:
                return mid_index
            
        return right_index



"""
V2

"""
# 平方根，二分查找的典型题目


class Solution:
    def mySqrt(self, x: int) -> int:

        if x == 0:
            return 0
        elif x == 1:
            return 1
        
        left_index = 0
        right_index = x

        while left_index < right_index:

            mid = (left_index + right_index) // 2
            square = mid * mid 
            if square == x:
                return mid
            elif square < x:
                left_index = mid # ERROR：边界条件错误，忘记加一
            else:
                right_index = mid # ERROR：边界条件错误，忘记加一
    
        return right_index


"""
V2

"""
# 平方根，二分查找的典型题目


class Solution:
    def mySqrt(self, x: int) -> int:

        if x == 0:
            return 0
        elif x == 1:
            return 1
        
        left_index = 0
        right_index = x

        while left_index < right_index:

            mid = (left_index + right_index) // 2
            square = mid * mid 
            if square == x:
                return mid
            elif square < x:
                left_index = mid + 1# ERROR：边界条件错误，忘记加一
            else:
                right_index = mid + 1# ERROR：边界条件错误，忘记加一
    
        return right_index


