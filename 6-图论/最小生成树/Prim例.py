

"""
例：Prim

"""

class Solution:
    # Prim 算法实现，graph 为邻接表（dict of dict），start 为起始顶点编号
    def prim_mst(self, adjacency_matrix: dict, start_vertex: int) -> int:
        """
        Prim算法核心实现：从指定起始顶点构建最小生成树，返回总权值
        
        参数说明：
        - adjacency_matrix: 邻接矩阵（dict of dict），格式为 {顶点u: {顶点v: 边权, ...}}
                            若顶点u和v无直接边，需保证 adjacency_matrix[u][v] = inf（无穷大）
        - start_vertex: 起始顶点编号（整数，需在0~顶点总数-1范围内）
        
        返回值：
        - total_mst_weight: 最小生成树的总权值；若图不连通，返回-1
        """
        # ========== 核心变量初始化 ==========
        # 1. 图的总顶点数（所有顶点编号为0 ~ vertex_count-1）
        vertex_count = len(adjacency_matrix)
        
        # 2. 已加入最小生成树（MST）的顶点集合（避免重复加入，保证无环）
        mst_vertices = set()
        
        # 3. 每个未加入MST的顶点，到「已选MST集合」的最小边权
        #    索引=顶点编号，值=该顶点到MST的最小边权，初始为无穷大（表示未连通）
        min_edge_weight_to_mst = [float('inf')] * vertex_count
        
        # 4. 最小生成树的总权值（最终返回结果）
        total_mst_weight = 0
        
        # ========== 起始顶点初始化 ==========
        # 起始顶点到自身的最小边权为0（自身已在MST集合中）
        min_edge_weight_to_mst[start_vertex] = 0
        
        # 初始化：更新起始顶点到所有其他顶点的直接边权（填充min_edge_weight_to_mst）
        for current_vertex in range(vertex_count):
            # 跳过起始顶点（自身边权已设为0）
            if current_vertex != start_vertex:
                # 取起始顶点到当前顶点的直接边权作为初始最小边权
                min_edge_weight_to_mst[current_vertex] = adjacency_matrix[start_vertex][current_vertex]
        
        # 将起始顶点加入MST集合（标记为已处理）
        mst_vertices.add(start_vertex)

        # ========== 核心循环：逐步加入剩余顶点 ==========
        # MST需包含所有顶点，已加入1个，还需加入 vertex_count-1 个
        for _ in range(vertex_count - 1):
            # 1. 找「未加入MST」且「到MST最小边权最小」的顶点（贪心核心）
            current_min_edge_weight = float('inf')  # 临时存储当前找到的最小边权
            nearest_unvisited_vertex = -1           # 临时存储对应顶点编号
            
            # 遍历所有顶点，筛选符合条件的目标顶点
            for vertex_id in range(vertex_count):
                # 条件：① 未加入MST ② 到MST的边权 < 当前记录的最小边权
                if vertex_id not in mst_vertices and min_edge_weight_to_mst[vertex_id] < current_min_edge_weight:
                    current_min_edge_weight = min_edge_weight_to_mst[vertex_id]
                    nearest_unvisited_vertex = vertex_id
            
            # 异常处理：找不到有效顶点 → 图不连通，无MST
            if nearest_unvisited_vertex == -1:
                return -1
            
            # 2. 将找到的顶点加入MST，并累加边权到总权值
            total_mst_weight += current_min_edge_weight
            mst_vertices.add(nearest_unvisited_vertex)
            
            # 3. 用新加入的顶点更新「未加入MST顶点」的最小边权（核心更新逻辑）
            #    原因：新顶点加入后，未加入顶点可能通过该顶点获得更短的边权到MST
            for unvisited_vertex in range(vertex_count):
                # 条件：① 未加入MST ② 新顶点到该顶点的边权 < 原最小边权
                if (unvisited_vertex not in mst_vertices and 
                    min_edge_weight_to_mst[unvisited_vertex] > adjacency_matrix[nearest_unvisited_vertex][unvisited_vertex]):
                    # 更新为更小的边权
                    min_edge_weight_to_mst[unvisited_vertex] = adjacency_matrix[nearest_unvisited_vertex][unvisited_vertex]
        
        # ========== 返回结果 ==========
        return total_mst_weight



