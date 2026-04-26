
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right



class Solution:
    def rangeSumBST(self, root: TreeNode, low: int, high: int) -> int:
        # 取出所有的值再求和么
        self.dfs_order = []          # ❶ 存储中序遍历结果的列表
        
        self.inorder(root)           # ❷ 执行中序遍历，填充 dfs_order
        
        total = 0
        for val in self.dfs_order:   # ❸ 遍历有序数组，累加区间内的值
            if low <= val <= high:
                total += val
        return total
    
    def inorder(self, node: TreeNode):
        if not node:                 # ❹ 递归终止条件：空节点返回
            return
        self.inorder(node.left)      # ❺ 遍历左子树
        self.dfs_order.append(node.val)  # ❻ 访问当前节点，将其值加入序列
        self.inorder(node.right)     # ❼ 遍历右子树