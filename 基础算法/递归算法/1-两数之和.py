from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # 定义递归辅助函数：参数为当前起始索引
        def find_pair(start_idx):
            # 终止条件1：起始索引到数组倒数第二个元素（后面无元素可匹配）
            if start_idx >= len(nums) - 1:
                return []  # 题目保证有解，实际不会走到这
            
            # 固定当前起始索引的数，计算需要的补数
            current_num = nums[start_idx]
            complement = target - current_num
            
            # 遍历start_idx之后的元素，找补数（避免重复检查）
            for j in range(start_idx + 1, len(nums)):
                if nums[j] == complement:
                    return [start_idx, j]
            
            # 若当前start_idx的数找不到补数，递归处理下一个索引
            return find_pair(start_idx + 1)
        
        # 从索引0开始递归
        return find_pair(0)


class Solution:
    def twoSum(self, nums, target):

        def find_pairs(nums, idx, target):

            if idx > len(nums) - 2:
                return []

            counter = target - nums[idx]
            for index_j in range(idx + 1, len(nums)):
                if nums[index_j] == counter:
                   return [idx, index_j]

            return find_pairs(nums, idx + 1, target)
        
        return find_pairs(nums, 0, target)
    











# 测试用例
if __name__ == "__main__":
    s = Solution()
    print(s.twoSum([2,7,11,15], 9))  # 输出 [0,1]
    print(s.twoSum([3,2,4], 6))       # 输出 [1,2]
    print(s.twoSum([3,3], 6))         # 输出 [0,1]