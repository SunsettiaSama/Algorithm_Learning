
class Solution:
    # 解法一、图（二叉树）的深度优先遍历
    def findTargetSumWays(self, nums, target):
        if len(nums) == 0:
            return 0
        
        size = len(nums)

        def dfs(index, curr_sum):
            if index == size:
                if curr_sum == target:
                    return 1
                else:
                    return 0
            ans = dfs(index + 1, curr_sum - nums[index]) + dfs(index + 1, curr_sum + nums[index]) 
            return ans

        return dfs(0, 0)
    
    # 解法一拓展：记忆单元
    def findTargetSumWays(self, nums, target):
        
        # 如何定义记忆？
        # 记忆应当是第i个元素的ans解才对
        cache = dict()

        # 先搜索到一条路径顶端
        def dfs(index, curr_target):
            # 递归终止条件：深度达到底端，此时返回答案
            if index == len(nums):
                if curr_target == target:
                    return 1
                else:
                    return 0
            
            # 递归终止记忆条件：当前的递归轮数有解
            if (index, curr_target) in cache:
                return cache[(index, curr_target)]
            
            # 处理当前情况，当指针落到第i个元素时
            # 还是做出选择，选择加还是减，从0开始的加减
            ans = dfs(index + 1, curr_target + nums[index]) + dfs(index + 1, curr_target - nums[index])
            # 记忆单元维护当前情况
            cache[(index, curr_target)] = ans

            return ans

        return dfs(index = 0, curr_target = 0)



    

    # 解法二、回溯算法
    def findTargetSumWays(self, nums, target):

        result = [0]

        def dfs(index, curr_sum):
            
            # 递归终止条件：所有数都已被选择过
            if index == len(nums):
                if curr_sum == target:
                    result[0] += 1
                return 
            
            # 递归体
            # 选择，选择加号
            curr_sum += nums[index]
            # 递归
            dfs(index + 1, curr_sum)
            # 回溯
            curr_sum -= nums[index]

            # 选择，选择加号
            curr_sum -= nums[index]
            # 递归
            dfs(index + 1, curr_sum)
            # 回溯
            curr_sum += nums[index]
        
        dfs(index = 0, curr_sum = 0)
        return result



    