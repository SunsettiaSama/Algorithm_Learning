
from typing import List

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def levelOrder(self, root: TreeNode) -> List[List[int]]:
        """
        二叉树层序遍历（广度优先搜索，BFS）
        返回每一层的节点值组成的二维列表
        """
        if not root:
            return []  # 空树直接返回空列表

        from collections import deque  # 推荐使用 deque 提高队列效率
        queue = deque([root])  # 初始化队列，根节点入队
        order = []             # 用于存储最终结果

        while queue:
            level = []                 # 存储当前层的节点值
            for _ in range(len(queue)):
                curr = queue.popleft() # 弹出队首节点
                level.append(curr.val) # 访问当前节点
                if curr.left:
                    queue.append(curr.left)   # 左子节点入队
                if curr.right:
                    queue.append(curr.right)  # 右子节点入队
            if level:
                order.append(level)     # 当前层结果加入总结果

        return order