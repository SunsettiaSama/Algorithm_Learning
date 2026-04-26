

import sys

def read_input():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    n = int(next(it))
    m = int(next(it))
    edges = []
    for _ in range(n - 1):
        u = int(next(it)); v = int(next(it))
        edges.append((u, v))
    queries = [int(next(it)) for _ in range(m)]
    return n, m, edges, queries

def build_graph(n, edges):
    g = [[] for _ in range(n + 1)]
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)
    return g

def get_parents_and_order(root, graph):
    parent = [0] * (len(graph))
    order = []
    stack = [root]
    parent[root] = -1
    while stack:
        u = stack.pop()
        order.append(u)
        for v in graph[u]:
            if v != parent[u]:
                parent[v] = u
                stack.append(v)
    return parent, order

def compute_answers(n, graph, parent, order):
    """
    自底向上计算每个节点的子树内所有点对距离和。
    参数:
        n: 节点总数
        graph: 邻接表
        parent: 每个节点的父节点（根节点的父节点为 -1）
        order: 前序遍历顺序（父节点在子节点之前）
    返回:
        ans: 每个节点对应子树的答案（所有点对距离和）
    """
    # 子树大小（包括节点自身）
    subtree_size = [1] * (n + 1)
    # 子树内所有节点到当前节点的距离之和
    sum_dist_to_node = [0] * (n + 1)
    # 最终答案：子树内所有点对的距离和
    answer = [0] * (n + 1)

    # 逆序遍历前序顺序 = 后序顺序（孩子先于父亲）
    for node in reversed(order):
        # 初始化当前正在合并的集合（开始时只有 node 自己）
        merged_size = 1          # 已经合并的节点综述
        merged_sum_dist = 0      # 这些已合并集合中所有节点到 node 的距离和。
        merged_pair_sum = 0      # 已合并集合内部所有点对的距离和（即子树内跨合并部分但已经计算过的答案，不包含后续将合并的新子树部分）。

        # 现在要合并一个新的子树 child 的节点集合。
        # order+逆序模拟dfs
        for child in graph[node]:
            # 跳过父节点，只处理真正的子节点
            if child == parent[node]:
                continue

            dist_child_to_node = sum_dist_to_node[child] + subtree_size[child]
            # 这里是推导出来的公式啊woc，原来如此
            cross_pairs = merged_sum_dist * subtree_size[child] + dist_child_to_node * merged_size
            merged_pair_sum += answer[child] + cross_pairs

            # 合并统计信息
            merged_sum_dist += dist_child_to_node
            merged_size += subtree_size[child]

        # 将 node 的最终统计信息存入数组
        subtree_size[node] = merged_size
        sum_dist_to_node[node] = merged_sum_dist
        answer[node] = merged_pair_sum

    return answer

def output_answers(ans, queries):
    out_lines = [str(ans[q]) for q in queries]
    sys.stdout.write("\n".join(out_lines))

def main():
    n, m, edges, queries = read_input()
    graph = build_graph(n, edges)
    parent, order = get_parents_and_order(1, graph)
    ans = compute_answers(n, graph, parent, order)
    output_answers(ans, queries)

if __name__ == "__main__":
    main()
    