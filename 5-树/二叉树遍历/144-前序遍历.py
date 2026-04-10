

from typing import List

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# 二叉树的前序遍历
# 规则：访问根节点，遍历左子树，遍历右子树

class Solution:
    def preorderTraversal(self, root: TreeNode) -> List[int]:
        """
        二叉树的前序遍历（递归实现）
        参数:
            root: TreeNode，二叉树的根节点
        返回:
            List[int]，前序遍历的节点值列表
        """
        res = []  # 用于存储遍历结果

        def preorder(node):
            if not node:
                return  # 递归终止条件：节点为空
            res.append(node.val)      # 1. 访问根节点
            preorder(node.left)       # 2. 递归遍历左子树
            preorder(node.right)      # 3. 递归遍历右子树

        preorder(root)  # 从根节点开始递归
        return res

"""
手搓V0

"""
class Solution:
    def preorderTraversal(self, root: TreeNode) -> List[int]:

        res = []

        def dfs(node):
            if not node:
                return 
            
            res.append(node.val)

            dfs(node.left)
            dfs(node.right)
        
        dfs(root)

        return res
    

"""
手搓V1

"""
class Solution:
    def preorderTraversal(self, root: TreeNode) -> List[int]:

        res = []

        def dfs(node):
            if not node:
                return
        
            res.append(node)
            dfs(node.left)
            dfs(node.right)
        
        dfs(root)


"""
0410扫了一眼
"""