# 输入：adjList = [[2,4],[1,3],[2,4],[1,3]]
# 输出：[[2,4],[1,3],[2,4],[1,3]]
# 解释：
# 图中有 4 个节点。
# 节点 1 的值是 1，它有两个邻居：节点 2 和 4 。
# 节点 2 的值是 2，它有两个邻居：节点 1 和 3 。
# 节点 3 的值是 3，它有两个邻居：节点 2 和 4 。
# 节点 4 的值是 4，它有两个邻居：节点 1 和 3 。

class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
        
import collections

class solu:
    

    def cloneGraph(self, node):
        if not node:
            return node
        
        global visited
        visited = dict()

        return self.dfs(node)
    
    
    def dfs(self, node):

        # 递归终止条件：该节点被访问过，那么返回已经访问过的节点
        if node in visited:
            return visited[node]
        
        # 节点处理
        clone_node = Node(node.val, [])
        visited[node] = clone_node # 这个映射是一一对应的映射，不存在子节点和父节点的关系

        for neighbor in node.neighbors:
            clone_node.neighbors.append(self.dfs(neighbor))
        
        return clone_node



"""
V0
其实这个地方最复杂的点在于原本的数据结构，复现该数据结构的前提是，你必须知道该数据结构输入是什么样的
本质上是Node Definetion，给你一个头节点，然后按照顺序建立一套一模一样的图
"""
class Solution:
    def cloneGraph(self, node: 'Node') -> 'Node':
        if not node:
            return node
        
        visited = dict()
        queue = collections.deque()

        visited[node] = Node(node.val, [])

        queue.append(node)

        while queue:
            node_u = queue.popleft()
            for node_v in node_u.neighbors:
                if node_v not in visited:
                    visited[node_v] = Node(node_v.val, [])
                    queue.append(node_v)
                
                # 这里的列表当中会直接指向Node本身，而不是索引或者什么别的东西
                visited[node_u].neighbors.append(visited[node_v])

        return visited[node]


