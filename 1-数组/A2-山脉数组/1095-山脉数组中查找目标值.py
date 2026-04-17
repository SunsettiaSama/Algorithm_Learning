# """
# This is MountainArray's API interface.
# You should not implement it, or speculate about its implementation
# """
class MountainArray:
   def get(self, index: int) -> int:
       pass 
   def length(self) -> int:
        pass

class Solution:
    def findInMountainArray(self, target: int, mountain_arr: 'MountainArray') -> int:
        """主函数：统筹流程，返回target最小索引，无则返回-1"""
        n = mountain_arr.length()
        # 步骤1：找到山脉峰顶（唯一核心）
        peak_idx = self.find_peak(mountain_arr, n)
        
        # 步骤2：先查【左递增区间】（要求最小索引，优先查左边）
        left_res = self.binary_search_ascend(mountain_arr, target, 0, peak_idx)
        if left_res != -1:
            return left_res
        
        # 步骤3：左区间没找到，查【右递减区间】
        right_res = self.binary_search_descend(mountain_arr, target, peak_idx, n - 1)
        return right_res

    def find_peak(self, mountain_arr: 'MountainArray', length: int) -> int:
        """工具函数1：纯二分查找山脉峰顶索引（单一职责：只找峰顶）"""
        left, right = 0, length - 1
        while left < right:
            # 防溢出的标准mid计算
            mid = left + (right - left) // 2
            # 核心逻辑：比右侧小 → 峰顶在右侧
            if mountain_arr.get(mid) < mountain_arr.get(mid + 1):
                left = mid + 1
            else:
                right = mid
        return left

    def binary_search_ascend(self, mountain_arr: 'MountainArray', target: int, left: int, right: int) -> int:
        """工具函数2：递增区间二分查找（单一职责：只查递增段）"""
        while left <= right:
            mid = left + (right - left) // 2
            val = mountain_arr.get(mid)
            if val == target:
                return mid
            elif val < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1

    def binary_search_descend(self, mountain_arr: 'MountainArray', target: int, left: int, right: int) -> int:
        """工具函数3：递减区间二分查找（单一职责：只查递减段）"""
        while left <= right:
            mid = left + (right - left) // 2
            val = mountain_arr.get(mid)
            if val == target:
                return mid
            elif val < target:
                # 递减数组：值偏小 → 往左找
                right = mid - 1
            else:
                # 值偏大 → 往右找
                left = mid + 1
        return -1