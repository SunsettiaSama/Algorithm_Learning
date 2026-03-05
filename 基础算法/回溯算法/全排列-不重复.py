class Solution:

    def permute(self, nums):
        """
        回溯法求解全排列问题
        :param nums: 输入的数字列表
        :return: 所有可能的全排列
        """
        # 排序是后续判断成立的前提
        nums = sorted(nums)
        # 全局变量
        res = []
        path = []
        visited = [False for i in range(len(nums))]
        
        # 回溯体
        def backtracks():
            # 递归终止条件
            if len(path) == len(nums):
                res.append(path[:])
                return 
            
            # 选择 + 递归 + 回溯
            # 全排列2的特殊选择：永远只选择【第一个】【不重复的】元素作为【path开头的第一个元素】
            for index, item in enumerate(nums):
                if index > 0 and nums[index - 1] == nums[index] and not visited[index - 1]: 
                    continue
                
                if not visited[index]:
                    # 选择
                    visited[index] = True
                    path.append(item)
                    # 回溯
                    backtracks()
                    path.pop()
                    visited[index] = False
        backtracks()
        return res

if __name__ == "__main__":
    s = Solution()
    print(s.permute([1, 1, 2]))
