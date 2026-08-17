

from typing import List




class Solution:
    def findPeakGrid(self, mat: List[List[int]]) -> List[int]:


        m = len(mat)
        n = len(mat[0])

        for i in range(m):

            left = 0
            right = n - 1

            while left < right: # 存在一个逻辑问题，先对列进行二分再对行二分，存在明显问题，因为题目没有保证列只有一个山脉，所以找到的峰值是局部最小值
                mid = (left + right) // 2

                if mat[i][mid] < mat[i][mid + 1]:
                    left = mid + 1
                else:
                    right = mid

            # 此时，left是该位置最高的点
            up_ok = (i == 0) or (mat[i - 1][left] < mat[i][left])
            down_ok = (i == (m - 1)) or (mat[i][left] > mat[i + 1][left]) # 问题一,没有检查,依赖ai检查
            if  up_ok and down_ok:  
                break

        return (i, left)
# 事实上，可以直接用numpy找全域最大值



# ==========================================