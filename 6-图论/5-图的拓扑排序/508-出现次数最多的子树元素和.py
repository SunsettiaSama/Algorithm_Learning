

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def findFrequentTreeSum(self, root: TreeNode) -> List[int]:
        from collections import defaultdict
        
        self.count = defaultdict(int)   # 记录每个子树和出现的次数
        self.max_count = 0              # 最大出现次数
        
        # 后序遍历：先左右，再处理当前节点
        self.postOrder(root)
        
        # 收集所有出现次数等于最大次数的子树和
        res = []
        for s, c in self.count.items():
            if c == self.max_count:
                res.append(s)
        return res
        
    def postOrder(self, node: TreeNode) -> int:
        if not node:
            return 0
        
        # 后序遍历：左子树和 + 右子树和 + 当前节点值
        left_sum = self.postOrder(node.left)
        right_sum = self.postOrder(node.right)
        cur_sum = left_sum + right_sum + node.val
        
        # 更新计数
        self.count[cur_sum] += 1
        self.max_count = max(self.max_count, self.count[cur_sum])
        return cur_sum