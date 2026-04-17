

from typing import List

class Solution:
    def peakIndexInMountainArray(self, arr: List[int]) -> int:
        

        # 也就是找到数组里面的最大值
        # 这个山脉数组必定合法

        left_index = 0
        right_index = len(arr) - 1

        while left_index <= right_index:

            mid = (left_index + right_index) // 2

            if arr[mid] > arr[mid - 1]:
                left_index = mid + 1
            elif arr[mid] < arr[mid - 1]:
                right_index = mid - 1
            
            
            if left_index == right_index:
                return right_index
            

"""
豆包修复版

"""
def peakIndexInMountainArray(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        mid = (left + right) // 2
        if arr[mid] < arr[mid + 1]:
            left = mid + 1  # 峰顶在右侧
        else:
            right = mid     # 峰顶在左侧（含mid）
    return left  # left和right最终重合，就是峰顶




from typing import List

class Solution:
    def peakIndexInMountainArray(self, arr: List[int]) -> int:
        
        return self.binarySearch(arr)


    
    def binarySearch(self, arr):
        """
        该函数用以返回峰顶索引
        """
        left, right = 0, len(arr) - 1

        while left < right:
            mid = (left + right) // 2

            if arr[mid] < arr[mid + 1]:
                # 说明在上坡，在区间右侧
                left = mid + 1
            elif arr[mid] > arr[mid + 1]:
                right = mid - 1 # ERROR：如果这里使用的是-1，就像原本的去重方法那样，那么我们就会错过山峰
                # 在中间那个点，那个小区间内，有一个位置其实是山峰，如果正常搜索的话，我们不能确定哪个是山峰（左或者右，因为此时山峰已经被排除了）

        return left


"""
修复

"""

from typing import List

class Solution:
    def peakIndexInMountainArray(self, arr: List[int]) -> int:
        
        return self.binarySearch(arr)


    
    def binarySearch(self, arr):
        """
        该函数用以返回峰顶索引
        """
        left, right = 0, len(arr) - 1

        while left < right:
            mid = (left + right) // 2

            if arr[mid] < arr[mid + 1]:
                # 说明在上坡，在区间右侧
                left = mid + 1
            elif arr[mid] > arr[mid + 1]:
                right = mid

        return left