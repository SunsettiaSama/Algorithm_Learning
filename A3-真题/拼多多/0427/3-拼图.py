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

import sys

def read_input():
    """读取输入数据"""
    data = sys.stdin.read().strip().split()
    if not data:
        return None
    it = iter(data)
    n = int(next(it))
    m = int(next(it))
    t = int(next(it))
    tasks = []
    for _ in range(n):
        a = int(next(it))  # 常规模式token
        b = int(next(it))  # 常规模式时间
        c = int(next(it))  # 降耗模式token
        d = int(next(it))  # 降耗模式时间
        tasks.append((a, b, c, d))
    return n, m, t, tasks


def init_dp(m, t):
    """
    初始化DP数组
    dp[i][j] = 消耗i个token、j个时间时，能完成的最大任务数
    初始状态：只有(0,0)可达，任务数为0，其余为-1（不可达）
    """
    dp = [[-1] * (t + 1) for _ in range(m + 1)]
    dp[0][0] = 0
    return dp


def update_dp(dp, a, b, c, d, m, t):
    """
    对单个任务更新DP状态（倒序遍历，避免重复选择）
    三种选择：不执行、常规模式、降耗模式
    """
    # 倒序遍历token和时间，模拟01背包的状态转移
    for i in range(m, -1, -1):
        for j in range(t, -1, -1):
            if dp[i][j] == -1:
                continue  # 当前状态不可达，跳过
            
            # 选择1：不执行任务，状态不变，无需操作
            
            # 选择2：常规模式
            ni, nj = i + a, j + b
            if ni <= m and nj <= t:
                if dp[ni][nj] < dp[i][j] + 1:
                    dp[ni][nj] = dp[i][j] + 1
            
            # 选择3：降耗模式
            ni, nj = i + c, j + d
            if ni <= m and nj <= t:
                if dp[ni][nj] < dp[i][j] + 1:
                    dp[ni][nj] = dp[i][j] + 1


def compute_max_tasks(dp, m, t):
    """遍历所有状态，计算最大可完成任务数"""
    max_count = 0
    for i in range(m + 1):
        for j in range(t + 1):
            if dp[i][j] > max_count:
                max_count = dp[i][j]
    return max_count


def solve():
    """主函数：串联所有模块"""
    input_data = read_input()
    if input_data is None:
        return
    n, m, t, tasks = input_data
    
    # 初始化DP
    dp = init_dp(m, t)
    
    # 逐个任务更新DP
    for a, b, c, d in tasks:
        update_dp(dp, a, b, c, d, m, t)
    
    # 计算结果
    result = compute_max_tasks(dp, m, t)
    print(result)


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





"""

==========================================

"""
import sys
from collections import deque

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
    total = n * m
    graph = [[] for _ in range(total + 1)]

    for a, b, d in edges:
        graph[b].append((a, d))

        graph[a].append((b, opposite(d)))

    return graph

def bfs_coords(graph, n, m):
    # 利用一维度的坐标存储所有的值
    coords = [None] * (n * m + 1)

    start = 1
    coords[start] = (0, 0)

    # bfs
    q = deque([start])

    while q:
        u = q.popleft()
        r, c = coords[u]

        for v, d in graph[u]:
            if d == 'U':
                coords[v] = (r - 1, c)
            elif d == 'B':
                coords[v] = (r + 1, c)
            elif d == 'L':
                coords[v] = (r, c - 1)
            elif d == 'R':
                coords[v] = (r, c + 1)

            q.append(v)
    
    return coords

def normalize_grid(coords, n, m):

    min_r = min(r for r, _ in coords[1: ] if r is not None)
    min_c = min(c for _, c in coords[1: ] if r is not None)


    grid = [[0] * m for _ in range(n)]

    for i in range(1, n * m + 1):
        r, c = coords[i]
        nr = r - min_r
        nc = c - min_c
        # 理论上 nr, nc 一定在 [0, n-1]×[0, m-1] 内
        grid[nr][nc] = i
    return grid


def main():

    n, m, edges = read_input()

    graph = build_graph(n, m, edges)
    coords = bfs_coords(graph, n, m)
    grid = normalize_coords(coords, n, m)

    for row in grid:
        for item in row:
            print(item, end = " ")
        
        print("")



if __name__ == "__main__":
    main()

















