
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []



"""
V0：这道题没学明白，先学例题

"""
from typing import Optional
class Solution:
    def cloneGraph(self, node):
        # 记录哪些访问过哪些没有
        visited = {}

        def build(original_node):

            # 边界条件：不存在节点与已经访问过的节点
            if not original_node: 
                return None
            
            if original_node in visited:
                return visited[original_node]
            
            clone_node = Node(original_node.val)

            visited[original_node] = clone_node

            for neighbor in original_node.neighbors:
                clone_node.neighbors.append(build(neighbor))


            return clone_node

        return build(node)