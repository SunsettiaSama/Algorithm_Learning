import collections




class Solution:
    # 拓扑排序，graph 中包含所有顶点的有向边关系（包括无边顶点）
    def topologicalSortingKahn(self, graph: dict):
        # 初始化所有顶点的入度为 0
        indegrees = {u: 0 for u in graph}
        # 统计每个顶点的入度
        for u in graph:
            for v in graph[u]:
                indegrees[v] += 1

        # 将所有入度为 0 的顶点加入队列 S
        S = collections.deque([u for u in indegrees if indegrees[u] == 0])
        order = []  # 用于存储拓扑序列

        while S:
            u = S.pop()  # 取出一个入度为 0 的顶点
            order.append(u)  # 加入拓扑序列
            for v in graph[u]:  # 遍历 u 的所有邻接点
                indegrees[v] -= 1  # 删除 u 指向 v 的边，v 入度减 1
                if indegrees[v] == 0:
                    S.append(v)  # 如果 v 入度为 0，加入队列

        # 如果 order 长度小于顶点数，说明有环，无法拓扑排序
        if len(order) != len(indegrees):
            return []
        return order  # 返回拓扑序列

    def findOrder(self, n: int, edges):
        """
        n: 顶点个数，编号为 0 ~ n - 1
        edges: 边列表，每条边为 (u, v)，表示 u 指向 v
        返回一个拓扑序列（如果有环则返回空列表）
        """
        # 构建邻接表
        graph = {i: [] for i in range(n)}
        for u, v in edges:
            graph[u].append(v)
        # 调用 Kahn 算法进行拓扑排序
        return self.topologicalSortingKahn(graph)
    

class Solution:
    # 拓扑排序，graph 中包含所有顶点的有向边关系（包括无边顶点）
    def topologicalSortingKahn(self, graph: dict):

        indegrees = {u: 0 for u in graph}

        for u in graph:
            for v in graph[u]:
                indegrees[v] += 1

        S = collections.deque([u for u in indegrees if indegrees[u] == 0])
        order = []

        # BFS，一定保证入度为0
        while S:
            u = S.pop()
            order.append(u)
            for v in graph[u]:
                indegrees[v] -= 1
                if indegrees[v] == 0:
                    S.append(v)
            
        if len(order) != len(indegrees):
            return []
            
        return order
    
    def findOrder(self, n, edges):

        graph = {i: [] for i in range(n)}
        for u, v in edges:
            graph[u].append(v)

        return self.topologicalSortingKahn(graph)
            
