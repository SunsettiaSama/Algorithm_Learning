class Solution:

    def permute(self, nums):
        """
        回溯法求解全排列问题
        :param nums: 输入的数字列表
        :return: 所有可能的全排列
        """
        # 全局变量
        path = []
        res = []

        # 回溯体
        def backtrack(): 
            # 终止条件：所有元素都已经得到了选择
            if len(path) == len(nums):
                res.append(path[:]) 
                return 
            
            
            # 选择 + 递归 + 回溯
            for num in nums:
                # 从左至右的选择
                if num in path:
                    continue
                path.append(num) # 选择
                backtrack()
                path.pop() # 回溯

        backtrack()
        return res


    


if __name__ == "__main__":
    s = Solution()
    print(s.permute([0, 1, 2]))
