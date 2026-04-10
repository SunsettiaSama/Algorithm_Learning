class Solution:
    def mySqrt(self, x):


        # 分治算法
        # 求解平方根需要在左右区间进行查找

        if x == 0:
            return 0
        


        left = 1
        right = x

        while left <= right:
            mid = int((left - right) / 2)
            square = mid * mid

            if square == x:
                return mid
            elif square < x:
                left = mid + 1
            else:
                right = mid - 1