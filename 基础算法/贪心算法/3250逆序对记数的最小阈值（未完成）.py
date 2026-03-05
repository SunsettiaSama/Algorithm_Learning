class Solution:
    def minThreshold(self, nums: List[int], k: int) -> int:
        
        # 贪心算法
        sorted_nums = sorted(nums, reverse = True)

