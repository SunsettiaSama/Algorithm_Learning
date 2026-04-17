def dfs_topsort(graph):
    visited = [0] * n          # 0未访问 1访问中 2已完成
    result = []
    
    def dfs(node):
        visited[node] = 1      # 标记为正在访问
        for neighbor in graph[node]:
            if visited[neighbor] == 1:
                raise Exception("有环，无法拓扑排序")
            if visited[neighbor] == 0:
                dfs(neighbor)
        visited[node] = 2      # 标记为已完成
        result.append(node)    # 后序加入
    
    for v in range(n):
        if visited[v] == 0:
            dfs(v)
    
    return result[::-1]        # 逆序得到拓扑序