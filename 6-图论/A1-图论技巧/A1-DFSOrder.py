def dfs_order_tree_to_array(root, graph):
    """
    树转数组：DFS Order 方法（迭代DFS实现）
    :param root: 树的根节点
    :param graph: 树的邻接表（无向图存储）
    :return: parent: 每个节点的父节点数组; order: 树的DFS序数组（树转数组的结果）
    """
    node_count = len(graph)  # 节点总数
    parent = [0] * node_count  # 记录每个节点的父节点
    order = []  # 【核心】DFS序数组，存储树转数组后的结果
    stack = [root]  # 栈模拟DFS遍历
    parent[root] = -1  # 根节点无父节点，标记为-1

    while stack:
        # 弹出栈顶节点，加入DFS序数组
        current_node = stack.pop()
        order.append(current_node)
        
        # 遍历邻接节点，跳过父节点（无向树避免回头遍历）
        for neighbor in graph[current_node]:
            if neighbor != parent[current_node]:
                parent[neighbor] = current_node
                stack.append(neighbor)
    
    return parent, order



"""
复现

"""

def get_parents_and_order(root, graph):
    parent = [0] * (len(graph))
    order = []
    stack = [root]

    parent[root] = -1

    while stack:
        u = stack.pop()
        order.append(u)
        for neighbor in graph[u]:
            if neighbor != parent[u]:
                parent[neighbor] = u
                stack.append(neighbor)

    return parent, order


def compute_answers(n, graph, parent, order):

    subtree_size = [1] * (n + 1)
    sum_dist_to_node = [0] * (n + 1)
    ans = [0] * (n + 1)

    for node in reversed(order):

        merged_size = 1
        merged_sum_dist = 0 # 所有已经合并进来的dist总和
        merged_pair_sum = 0

        for child in graph[node]:
            if child == parent[node]:
                continue

            dist_child_to_node = sum_dist_to_node[child] + subtree_size[child]

            cross_pairs = merged_sum_dist * subtree_size[child] + dist_child_to_node * merged_size

            merged_pair_sum += ans[child] + cross_pairs

            # 合并统计信息
            merged_sum_dist += dist_child_to_node
            merged_size += subtree_size[child]
            
        subtree_size[node] = merged_size
        sum_dist_to_node[node] = merged_sum_dist
        ans[node] = merged_pair_sum
    
    return ans