"""
dijkstra算法要求：
非负性，路径边权重一定得非负


"""
class Solution:
    def dijkstra(self, graph, n, source):

        dist = [float('inf')] * (n + 1)
        dist[source] = 0

        visited = set()

        while len(visited) < n:

            current_node = -1

            # 选择距离源点最近的节点
            min_distance = float('inf')
            for i in range(1, n + 1):
                if i not in visited and dist[i] < min_distance: # 未访问的最小距离
                    min_distance = dist[i]
                    current_node = i
                
            
            if current_node == -1: # 若无可处理节点，剩下节点不可达，直接跳出
                break 
            
            # 标记当前节点为已访问
            visited.add(current_node)

            # 遍历当前节点的所有邻居，尝试更新最短距离
            for neighbor, weight in graph.get(current_node, {}).items():
                if neighbor not in visited:
                    if dist[current_node] + weight < dist[neighbor]:
                        dist[neighbor] = dist[current_node] + weight
            

        return dist