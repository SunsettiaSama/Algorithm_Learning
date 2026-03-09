from typing import List

class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        # 1. 先整理“路和时间”成邻接表（娃漏了这步，会报错）
        adj = [[] for _ in range(n + 1)]  # 每家对应一个空列表，装邻居+时间
        for u, v, w in times:
            adj[u].append((v, w))  # 比如u=1, v=2, w=2 → 1号家的邻居是2号，要2分钟
        
        # 初始化到每家的时间（这部分娃是对的）
        # 该列表用以保存最速时间点，第i行记录的是从起点k出发，到i家的最速时间，是k到各个点的时间映射
        dist = [float('inf')] * (n + 1)
        dist[k] = 0  # 起点到自己时间为0
        visited = set()

        while len(visited) < n:
            current_node = -1
            # 2. 改：找最小距离（娃写成了max_distance和-inf，全反了）
            # 搜索到该点的最短路径，如果没去过，且耗时更短，那么就认为是最短路径：贪心算法
            min_distance = float("inf")  # 初始化成“无穷远”
            for i in range(1, n+1):
                # 改：找没去过、且时间更短的人家
                if i not in visited and dist[i] < min_distance:
                    min_distance = dist[i]
                    current_node = i
            
            if current_node == -1:
                break  # 如果为-1，意味着，不存在更短路径，且节点都访问完成，也就跳出

            visited.add(current_node)

            # 3. 改：用整理好的adj找邻居（娃用times[current_node]会错）
            for neighbor, weight in adj[current_node]:
                if neighbor not in visited:
                    # 算新时间：到当前家的时间 + 到邻居的时间
                    new_dist = dist[current_node] + weight
                    if new_dist < dist[neighbor]: # 去邻居家看一眼后发现，欸，比我直接到某某家更快，于是更新
                        dist[neighbor] = new_dist # neighbor是索引，new_dist为路径值，这里的更新是原本最短的时间，更新一遍新的值
                        # 注意，之前从未更新过dist的值，只有在这里更新，也就是临近时进行更新
        
        # 4. 娃漏了：计算并返回最终结果
        # 找全村收到消息的最长时间（从1号到n号家）
        # 取个max结束战斗
        max_time = max(dist[1:n+1])
        # 如果最长时间还是无穷远，说明有人没收到，返回-1；否则返回最长时间
        return max_time if max_time != float('inf') else -1
    

"""

V1

"""


class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        # 1. 正确构建邻接表：起点→[(邻居, 权重), ...]
        graph = {}
        for u, v, w in times:
            if u not in graph:
                graph[u] = []
            graph[u].append((v, w))  # 每个起点对应一个列表，存储所有邻居
        
        # 2. 初始化距离数组：节点编号1~n，所以列表长度n+1（索引0不用）
        min_distances = [float('inf')] * (n + 1)
        min_distances[k] = 0  # 起始节点k的距离为0
        visited = set()
        
        while len(visited) < n:
            # 找当前未访问的、距离最短的节点
            current_node = -1
            current_distance = float('inf')
            # 遍历1~n（节点编号从1开始）
            for node_id in range(1, n + 1):
                if min_distances[node_id] < current_distance and node_id not in visited:
                    current_node = node_id
                    current_distance = min_distances[node_id]
            
            # 无有效节点（存在不可达节点）
            if current_node == -1:
                break
            
            visited.add(current_node)
            
            # 遍历当前节点的所有邻居（处理key不存在的情况）
            for neighbor_node, neighbor_distance in graph.get(current_node, []):
                if neighbor_node in visited:
                    continue
                # 更新距离
                new_distance = current_distance + neighbor_distance
                if new_distance < min_distances[neighbor_node]:
                    min_distances[neighbor_node] = new_distance
        
        # 3. 处理边界条件：计算1~n的最大距离，若有inf（不可达）返回-1
        max_delay = max(min_distances[1:])  # 只看1~n的节点
        return max_delay if max_delay != float('inf') else -1
