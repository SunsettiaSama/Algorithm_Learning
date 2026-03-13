from typing import List


class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:

        
        res = []
        path = []

        def dfs():
            if len(path) == len(nums):
                res.append(path[:])
                return 
            
            for i in range(len(nums)):
                if nums[i] in path:
                    continue

                path.append(nums[i])
                dfs()
                path.pop()
        
        dfs()
        return res
    

"""
也就是说，递归的终止条件是肯定固定的
但是递归的位置可以发生改变，如果放在return，那就是线性调用
如果放到循环中，结合pop和return，就可以进一步实现回溯

"""
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        """
        回溯法求解全排列问题
        :param nums: 输入的数字列表
        :return: 所有可能的全排列
        """
        res = []    # 用于存放所有符合条件的排列结果
        path = []   # 用于存放当前递归路径下的排列

        def backtracking():
            
            # 终止条件，长度相等
            if len(path) == len(nums):
                res.append(path[:])
                return 
            
            for i in range(len(nums)):
                if nums[i] in path:
                    continue

                path.append(nums[i])
                backtracking()
                path.pop()
        
        # 最后忘记调用了
        backtracking()
        return res

            

            