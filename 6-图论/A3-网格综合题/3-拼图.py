import sys
from collections import deque

def opposite(direction):
    """返回相反方向"""
    return {'U': 'B', 'B': 'U', 'L': 'R', 'R': 'L'}[direction]

def read_input():
    data = sys.stdin.read().strip().split()
    if not data:
        return None
    it = iter(data)
    n = int(next(it))
    m = int(next(it))
    k = int(next(it))
    edges = []
    for _ in range(k):
        a = int(next(it))
        b = int(next(it))
        d = next(it)
        edges.append((a, b, d))
    return n, m, edges

def build_graph(n, m, edges):
    total = n * m
    graph = [[] for _ in range(total + 1)]  # 1-indexed
    for a, b, d in edges:
        # a 在 b 的 d 方向 -> 有向边 b->a 方向 d
        graph[b].append((a, d))
        # 反向边
        graph[a].append((b, opposite(d)))
    return graph

def bfs_coords(graph, total_nodes):
    coords = [None] * (total_nodes + 1)
    start = 1  # 任意起点，题目保证连通且编号≥1
    coords[start] = (0, 0)
    q = deque([start])
    while q:
        u = q.popleft()
        r, c = coords[u]
        for v, dir_ in graph[u]:
            if coords[v] is None:
                if dir_ == 'U':
                    coords[v] = (r - 1, c)
                elif dir_ == 'B':
                    coords[v] = (r + 1, c)
                elif dir_ == 'L':
                    coords[v] = (r, c - 1)
                else:  # 'R'
                    coords[v] = (r, c + 1)
                q.append(v)
    return coords

def normalize_coords(coords, n, m):
    # coords[1]..coords[n*m] 都是 (r, c)
    # 找出最小行和最小列
    min_r = min(r for r, _ in coords[1:] if r is not None)
    min_c = min(c for _, c in coords[1:] if c is not None)
    # 创建网格并填入编号
    grid = [[0] * m for _ in range(n)]
    for i in range(1, n * m + 1):
        r, c = coords[i]
        nr = r - min_r
        nc = c - min_c
        # 理论上 nr, nc 一定在 [0, n-1]×[0, m-1] 内
        grid[nr][nc] = i
    return grid

def print_grid(grid):
    out_lines = []
    for row in grid:
        out_lines.append(' '.join(map(str, row)))
    sys.stdout.write('\n'.join(out_lines))

def solve():
    input_data = read_input()
    if input_data is None:
        return
    n, m, edges = input_data
    graph = build_graph(n, m, edges)
    coords = bfs_coords(graph, n * m)
    grid = normalize_coords(coords, n, m)
    print_grid(grid)

if __name__ == "__main__":
    solve()














def opposite(direction):
    return {'U': 'B', 'B': 'U', 'L': 'R', 'R': 'L'}[direction]

def read_input():
    data = sys.stdin.read().strip().split()
    if not data:
        return None
    it = iter(data)
    n = int(next(it))
    m = int(next(it))
    k = int(next(it))
    edges = []
    for _ in range(k):
        a = int(next(it))
        b = int(next(it))
        d = next(it)
        edges.append((a, b, d))
    return n, m, edges

def build_graph(n, m, edges):
    """
    Node: (neighbor, direction)
    """
    total = n * m
    graph = [[] for _ in range(total + 1)]

    for a, b, d in edges:
        graph[b].append((a, d))
        graph[a].append((b, opposite(d)))
    return graph

def bfs_coords(graph, total_nodes):
    coords = [None] * (total_nodes + 1)
    start = 1

    coords[start] = (0, 0)
    q = deque([start])

    while q:
        u = q.popleft()
        r, c = coords[u]
        for v, dir_ in graph[u]:
            if coords[v] is None:
                if dir_ == 'U':
                    coords[v] = (r - 1, c)
                elif dir_ == 'B':
                    coords[v] = (r + 1, c)
                elif dir_ == 'L':
                    coords[v] = (r, c - 1)
                elif dir_ == 'R':
                    coords[v] = (r, c + 1)
                q.append(v)
    
    return coords

def normalize_coords(coords, n, m):

    min_r = min(r for r, _ in coords[1: ] if r is not None)
    min_c = min(c for _, c in coords[1: ] if c is not None)

    grid = [[0] * m for _ in range(n)]
    for i in range(1, n * m + 1):
        r, c = coords[i]
        nr = r - min_r
        nc = c - min_c
        grid[nr][nc] = i
    
    return grid

def print_grid(grid):
    out_lines = []
    for row in grid:
        out_lines.append(' '.join(map(str, row)))
    sys.stdout.write('\n'.join(out_lines))

def solve():
    input_data = read_input()
    if input_data is None:
        return
    n, m, edges = input_data
    graph = build_graph(n, m, edges)
    coords = bfs_coords(graph, n * m)
    grid = normalize_coords(coords, n, m)
    print_grid(grid)

if __name__ == "__main__":
    solve()













def opposite(direction):
    return {
        'U': 'B',
        'B': 'U',
        'L': 'R',
        'R': 'L'
    }

def read_input():
    data = sys.stdin.read().strip().split()
    if not data:
        return None
    it = iter(data)
    n = int(next(it))
    m = int(next(it))
    k = int(next(it))
    edges = []
    for _ in range(k):
        a = int(next(it))
        b = int(next(it))
        d = next(it)
        edges.append((a, b, d))
    return n, m, edges

def build_graph(n, m, edges):
    total = n * m
    graph = [[] for _ in range(total + 1)]

    for a, b, d in edges:
        graph[b].append((a, d))
        graph[a].append((b, opposite(d)))

    return graph

def bfs_coords(graph, total_nodes):
    coords = [None] * (total_nodes + 1)

    start = 1
    coords[start] = (0, 0)
    q = deque([start])

    while q:
        u = q.popleft(u)

        r, c = coords[u]
        #
        for v, dir_ in graph[u]:
            if coords[v] is None:
                if dir_ == 'U':
                    coords[v] = (r - 1, c)
                elif dir_ == 'B':
                    coords[v] = (r + 1, c)
                elif dir_ == 'L':
                    coords[v] = (r, c - 1)
                elif dir_ == 'R':
                    coords[v] = (r, c + 1)

                q.append(v)


    return coords

def norm(n, m, coords):
    diff_r = min(r for r, _ in coords[1: ] if r is not None)
    diff_c = min(c for _, c in coords[1: ] if c is not None)

    grid = [[0 for i in range(m)] for j in range(n)]
    idx = 1
    nodes = [i for i in range(1, n*m + 1)]

    for node in nodes:
        r, c = coords[node]
        new_r, new_c = r - diff_r, c - diff_c

        grid[new_r][new_c] = idx

        idx += 1
    
    return grid

def print_grid(grid):
    out_lines = []
    for row in grid:
        out_lines.append(' '.join(map(str, row)))
    sys.stdout.write('\n'.join(out_lines))


def solve():
    input_data = read_input()
    if input_data is None:
        return
    n, m, edges = input_data
    graph = build_graph(n, m, edges)
    coords = bfs_coords(graph, n * m)
    grid = norm(coords, n, m)
    print_grid(grid)

if __name__ == "__main__":
    solve()