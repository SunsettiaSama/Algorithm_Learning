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
    

"""
V0 Dijkstra算法

"""
class Solution:
    def dijkstra(self, graph, node_nums, start_node):
        # 注意这个输入，这个输入完全不依赖于Node那个类，记得吧

        # 边界条件：想不明白

        min_distances = [float('inf') for i in range(node_nums)]
        # 到其自身的距离为0
        min_distances[start_node] = 0


        visited = set()

        while len(visited) < node_nums: 

            # 使用dijkstra，确定起点出发的源头
            # 比如第一个最近的点,取出来,那么它和source源头是连通的
            # 那么就去找,找到距离最近的点,初始化为无穷大,检索出当前的最近的点,
            min_dis = float('inf')
            current_node = -1
            for i in range(1, node_nums):
                if i not in visited and min_distances[i] < min_dis:
                    min_dis = min_distances[i]
                    current_node = i
            
            # 无可用的节点
            if current_node == -1:
                break

            visited.add(current_node)

            for neighbor, weight in graph.get(current_node, {}).items():
                if neighbor not in visited:
                    if min_distances[current_node] + weight < min_distances[neighbor]:
                        min_distances[neighbor] = min_distances[neighbor] + weight
            
        return min_distances


"""
V0 Dijkstra算法

"""
class Solution:
    def dijkstra(self, graph, node_nums, start_node):
        # 初始化：起点到各节点的最短距离，初始为无穷大
        min_distances = [float('inf') for i in range(node_nums)]
        min_distances[start_node] = 0  # 起点到自身距离为0

        visited = set()  # 已确定最短路径的节点集合

        # 错误1修正：判断已访问节点数 < 总节点数
        while len(visited) < node_nums:
            # 初始化：本轮要找的最小距离和对应节点
            current_min_distance = float('inf')
            current_min_dist_node = -1

            # 错误2修正：遍历所有节点（从0开始）
            for i in range(1, node_nums + 1):
                # 错误3修正：判断i未访问，且i的距离 < 当前记录的最小值
                if i not in visited and min_distances[i] < current_min_distance:
                    current_min_dist_node = i  # 更新距离最小的节点
                    current_min_distance = min_distances[i]  # 更新最小距离值
            
            # 无可用节点（剩下的都无法到达），提前退出
            if current_min_dist_node == -1:
                break
            
            # 新增：标记当前节点为已访问（核心步骤，原代码遗漏）
            visited.add(current_min_dist_node)

            # 处理当前节点的所有邻居
            for neighbor_node, weight in graph.get(current_min_dist_node, {}).items():
                if neighbor_node not in visited:
                    # 计算经当前节点到邻居的新距离
                    new_distance = current_min_distance + weight
                    if new_distance < min_distances[neighbor_node]:
                        # 错误4修正：用节点索引取距离，而非距离值
                        min_distances[neighbor_node] = min_distances[current_min_dist_node] + weight
        
        # 错误5修正：return缩进到循环外
        return min_distances

"""
V1 Dijkstra算法

"""
class Solution:
    def dijkstra(self, graph: dict, node_nums, start_node):
        """
        graph 为邻接表
        """

        min_distances = [float('inf') for i in range(node_nums)]
        min_distances[start_node] = 0
        # 这里有个什么东西来着

        visited = set()
        while len(visited) < node_nums:

            # 先使用贪婪，检索到目前路径最短的点
            current_distance = float('inf')
            current_node = -1
            for nodei in range(node_nums):
                noted_distance = min_distances[nodei]
                # 没有访问过，并且记录的距离是最短的
                # 注意,这里的i其实就是node本身
                if noted_distance < current_distance and not nodei in visited:
                    current_distance = noted_distance
                    current_node = nodei
            
            if current_node == -1:
                break
            
            visited.add(current_node)

            # 然后检查它的邻居
            for neighbor, neighbor_distance in graph:
                # 如果邻居访问过，则不管
                if neighbor in visited:
                    continue

                # 如果没访问过，此时考虑距离，如果距离更小，则更新，否则不更新
                if current_distance + neighbor_distance < min_distances[neighbor]:
                    min_distances[neighbor] = current_distance + neighbor_distance
            
        return min_distances



"""
V1修复版
"""

class Solution:
    def dijkstra(self, graph: dict, node_nums, start_node):
        
        min_distances = [float('inf') for i in range(node_nums)]
        min_distances[start_node] = 0

        visited = set()

        while len(visited) < node_nums:

            # 遍历每一个节点，取出最近的节点
            current_node = -1
            current_distance = float('inf')
            for node_id in range(node_nums):
                if min_distances[node_id] < current_distance and not node_id in visited:
                    current_node = node_id
                    current_distance = min_distances[node_id]
            
            # 无有效节点
            if current_node == -1:
                break

            # 标记为已经访问过
            visited.add(current_node)
                
            for neighbor_node, neighbor_distance in graph.get(current_node, []):
                # 邻居如果在内部，那就不管了
                if neighbor_node in visited:
                    continue

                # 此时来更新邻居的距离
                if neighbor_distance + current_distance < min_distances[neighbor_node]:
                    min_distances[neighbor_node] = neighbor_distance + current_distance 

        return min_distances








