
from typing import List

class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        
        res = []

        for index1 in range(len(nums)):
            for index2 in range(index1, len(nums)):
                for index3 in range(index2, len(nums)):

                    if any((index1 == index2, index2 == index3, index1 == index3)):
                        continue

                    if nums[index1] + nums[index2] + nums[index3] == 0:
                        result = sorted([nums[index1], nums[index2], nums[index3]])
                        if not result in res:
                            res.append(result)

        return res

"""
=================================
代码说明与优化必要性
这段代码采用纯枚举（暴力）的方式求解三数之和问题，通过三重嵌套循环遍历所有可能的三元组索引组合，再验证索引不重复、三数之和为 0，最后通过排序 + 查重得到结果。
该算法的时间复杂度为 O(n3)（n 为数组长度），其中三重循环是核心时间开销，此外每次找到候选结果后还需排序（O(log3) 可忽略）和检查结果是否已存在（O(k)，k 为结果集长度），进一步增加了时间消耗。
在实际应用中，当数组长度 n 稍大（如 n>200）时，这种纯枚举的方式会因超出在线判题系统的时间限制触发超时，无法通过测试用例，因此必须对枚举算法进行优化。
=================================

"""


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        res = []
        n = len(nums)
        # 1. 先排序，为双指针和去重做准备，排序时间 O(n log n)
        nums.sort()
        
        # 2. 固定第一个数，遍历范围 0 ~ n-3（后面留两个数给双指针）
        for i in range(n):
            # 去重：如果当前数和前一个数相同，跳过（避免重复三元组）
            if i > 0 and nums[i] == nums[i-1]:
                continue
            # 3. 双指针：left 从 i+1 开始，right 从末尾开始
            left = i + 1
            right = n - 1
            while left < right:
                total = nums[i] + nums[left] + nums[right]
                if total == 0:
                    # 找到符合条件的三元组，加入结果集
                    res.append([nums[i], nums[left], nums[right]])
                    # 去重：跳过left指针的重复值
                    while left < right and nums[left] == nums[left+1]:
                        left += 1
                    # 去重：跳过right指针的重复值
                    while left < right and nums[right] == nums[right-1]:
                        right -= 1
                    # 双指针同时移动，寻找下一个可能的组合
                    left += 1
                    right -= 1
                elif total < 0:
                    # 和太小，左指针右移（增大数值）
                    left += 1
                else:
                    # 和太大，右指针左移（减小数值）
                    right -= 1
        return res
    