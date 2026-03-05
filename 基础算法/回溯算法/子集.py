class Solution:
    def subsets(self, nums):

        res = []
        path = []

        def backtracking(index):
            # 递归终止条件

            res.append(path[:])
            if len(path) == len(nums):
                return 
                        
            for i in range(index, len(nums)):
                # 第i层的第j个决策下，过滤path已存在的值
                path.append(nums[i])
                # 递归
                backtracking(i + 1) 
                # 回溯
                path.pop()

        backtracking(0)
        return res

        
if __name__ == "__main__":
    s = Solution()
    print(s.subsets([0, 1, 2]))
    

