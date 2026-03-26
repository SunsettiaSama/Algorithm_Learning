
"""
所以说树形结构dp和记忆化搜索这个路子完全一致
其实也就是计算dp[node]这个说法

"""

# Definition for a binary tree node.
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def __init__(self):
        self.ans = float('-inf')
        
    def dfs(self, node):
        if not node:
            return 0
        left_max = max(self.dfs(node.left), 0)     # 左子树提供的最大贡献值
        right_max = max(self.dfs(node.right), 0)   # 右子树提供的最大贡献值

        cur_max = left_max + right_max + node.val  # 包含当前节点和左右子树的最大路径和，从左走到右，是一条完整的路径
        self.ans = max(self.ans, cur_max)          # 更新所有路径中的最大路径和

        return max(left_max, right_max) + node.val # 返回包含当前节点的子树的最大贡献值

    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        self.dfs(root)
        return self.ans


"""
V0 学习版
"""

class Solution:
    def __init__(self):
        self.ans = float('-inf')
        
    def dfs(self, node):
        if not node:
            return 0
        left_value = max(self.dfs(node.left), 0) # 如果为负数，则抛弃
        right_value = max(self.dfs(node.right), 0)

        curr_value = left_value + right_value + node.val # 当前节点值别忘了

        self.ans = max(self.ans, curr_value) # 存答案的

        return max(left_value, right_value) + node.val # 路径当然只能选一个啦

    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        self.dfs(root)
        return self.ans

"""
V1 手搓

"""




class Solution:
    def __init__(self):
        self.ans = float('-inf')

    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        self.dfs(root)
        return self.ans
    
    # 某个节点的状态被定义为当前节点的贡献值（左中右）
    def dfs(self, node):
        if not node:
            return 0

        # 左侧贡献值
        ans_left = max(self.dfs(node.left), 0) # 允许两边都不选,非0的抛弃掉
        # 右侧贡献值
        ans_right = max(self.dfs(node.right), 0)

        curr_ans = ans_left + ans_right + node.val
        if curr_ans > self.ans:
            self.ans = curr_ans

        return max(ans_left, ans_right) + node.val
        

        

        



