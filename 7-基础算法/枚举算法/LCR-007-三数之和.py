
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
    

'''
V1：V1版本表示不会这东西，需要学习一下
需要对撞指针，而且是嵌套在for循环里面的对撞
'''

class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        # 错误1：长度判断逻辑错误
        # 三数之和需要至少3个元素，应该是 len(nums) < 3，而非 < 2
        if len(nums) < 2:
            return []

        nums = sorted(nums)
        results = []

        for slow_index, slow_num in enumerate(nums):
            # 错误2：外层基准数去重逻辑被注释，且原注释的去重写法也不优雅（not slow_index == 0 等价于 slow_index != 0）
            # 即使不注释，该版本也没有内层双指针的去重，会产生重复三元组
            # if not slow_index == 0 and slow_num == nums[slow_index - 1]:
            #     continue

            left_index = slow_index + 1
            right_index = len(nums) - 1

            while left_index < right_index:
                left_num = nums[left_index]
                right_num = nums[right_index]
                if slow_num + left_num + right_num == 0:
                    results.append([slow_num, left_num, right_num])
                    # 错误3：找到一个解后直接break，终止双指针循环
                    # 导致当前基准数下的其他可能解（比如多个和为0的组合）无法被找到
                    break
                elif slow_num + left_num + right_num < 0:
                    left_index += 1
                elif slow_num + left_num + right_num > 0:
                    right_index -= 1
            
        return results
        
        

'''
V1修复版：去重逻辑

'''

class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        # 错误1：长度判断仍未修复，还是 len(nums) < 2
        if len(nums) < 2:
            return []

        nums = sorted(nums)
        results = []

        for slow_index, slow_num in enumerate(nums):
            # 错误2：外层基准数的去重仍被注释，未处理重复的基准数
            # if not slow_index == 0 and slow_num == nums[slow_index - 1]:
            #     continue

            left_index = slow_index + 1
            right_index = len(nums) - 1

            while left_index < right_index:
                left_num = nums[left_index]
                right_num = nums[right_index]
                if slow_num + left_num + right_num == 0:
                    results.append([slow_num, left_num, right_num])

                    # 问题1：去重逻辑后未移动左右指针，导致死循环
                    # 比如输入[-1,0,1,2,-1,-4]，找到[-1,0,1]后，left和right指针不移动，while循环会无限执行
                    # 问题2：右指针去重条件错误
                    # 排序后数组是升序，右指针要跳过重复值，应判断 nums[right_index] == nums[right_index - 1] 吗？
                    # 实际应为：先移动指针，再去重；且当前写法会跳过未处理的重复值
                    # 去重：跳过left指针的重复值
                    while left_index < right_index and nums[left_index] == nums[left_index + 1]:
                        left_index += 1
                    # 去重：跳过right指针的重复值（条件逻辑有问题）
                    while left_index < right_index and nums[right_index] == nums[right_index-1]:
                        right_index -= 1
                    
                    left_index += 1
                    right_index -= 1

                elif slow_num + left_num + right_num < 0:
                    left_index += 1
                elif slow_num + left_num + right_num > 0:
                    right_index -= 1
            
        return results









