

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
    size = [1] * (n + 1)
    sumDist = [0] * (n + 1)
    ans = [0] * (n + 1)

    for u in reversed(order):
        cur_sz = 1
        cur_sum = 0
        cur_ans = 0
        for v in graph[u]:
            if v == parent[u]:
                continue
            to_u = sumDist[v] + size[v]
            cross = cur_sum * size[v] + to_u * cur_sz
            cur_ans += ans[v] + cross
            cur_sum += to_u
            cur_sz += size[v]
        size[u] = cur_sz
        sumDist[u] = cur_sum
        ans[u] = cur_ans
    return ans

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
    