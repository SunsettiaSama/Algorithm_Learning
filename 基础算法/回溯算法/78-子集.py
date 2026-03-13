

"""
V0 错误百出的子集解
"""
class Solution:
    def subsets(self, nums):

        res = []
        path = []

        def backtracking():
            # 错误1：低效且无效的去重判断（本质是生成重复子集，而非去重能解决）
            # 问题：path in res 是O(n)操作，且因引用问题+重复生成，根本无法正确去重
            if not path in res:
                # 错误2：添加path的引用而非副本
                # 问题：后续path.pop()会同步修改res中已添加的path内容，最终res全是错误值
                res.append(path)
            
            # 错误3：终止条件错误
            # 问题：子集不需要等长度等于nums才停止，此条件会导致递归提前终止，漏生成短子集
            if len(path) == len(nums):
                return 
            
            # 错误4：无起始索引控制，for循环从0开始遍历
            # 问题：会重复选择元素（如[1,2]和[2,1]都生成，且会选到重复元素如[1,1]），子集要求不重复选、无顺序
            for i in range(len(nums)):

                path.append(nums[i])
                backtracking()
                path.pop()

        backtracking()
        return res


"""
V0 豆包修复版
"""

class Solution:
    def subsets(self, nums):
        res = []  # 存储所有子集
        path = []  # 存储当前路径（单个子集）

        def backtracking(start):
            # 关键：每次进入递归先把当前路径的副本加入结果（所有路径都是有效子集）
            res.append(path.copy())  # 用copy()/path[:]创建副本，避免引用问题
            
            # 终止条件：start超过nums长度时，for循环不执行，自然终止（可省略显式return）
            if start >= len(nums):
                return
            
            # 从start开始遍历，避免重复选择元素
            for i in range(start, len(nums)):
                path.append(nums[i])  # 选择当前元素
                backtracking(i + 1)   # 递归：下一轮从i+1开始，避免重复选当前及之前元素
                path.pop()            # 回溯：撤销选择
        
        backtracking(0)  # 初始从索引0开始
        return res





