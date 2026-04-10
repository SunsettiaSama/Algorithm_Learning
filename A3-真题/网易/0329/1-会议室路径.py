"""

好，接下来我跟你描述一个真题，有一个公司大楼，可建模成3*5的房间，官方叫会议室，现在随机挑一个会议室，请问从该会议室到其他会议室的最短距离怎么求：
1. 上下楼要么走楼梯，要么坐电梯，电梯在边界上，楼梯在横坐标为3的房间位置，每次电梯上楼代价为2，下楼代价为2，楼梯上楼代价为6，下楼代价为3。有且只有电梯可以上下楼，除此之外的移动代价都为1
2. 求出所有其他会议室的最短距离
"""


import heapq

FLOORS = [1, 2, 3]
COLS = [1, 2, 3, 4, 5]
ELEVATOR_COLS = [1, 5]
STAIRS_COL = [3]

def get_neighbors(node):
    floor, col = node
    neighbors = []

    if col - 1 in COLS:
        neighbors.append(((floor, col - 1), 1))
    
    if col + 1 in COLS:
        neighbors.append( ((floor, col + 1), 1))
    
    if col in ELEVATOR_COLS:
        if floor - 1 in FLOORS:
            neighbors.append( ((floor - 1, col), 2) )
        if floor + 1 in FLOORS:
            neighbors.append( ((floor + 1, col), 2) )

    if col in STAIRS_COL:
        if floor - 1 in FLOORS:
            neighbors.append( ((floor - 1, col), 3) )
        if floor + 1 in FLOORS:
            neighbors.append( ((floor + 1, col), 6) )
    
    return neighbors

def dijkstra(start):

    INF = float('inf')
    dist = {}
    prev = {}

    for floor in FLOORS:
        for col in COLS:
            dist[(floor, col)] = INF
            prev[(floor, col)] = None

    dist[start] = 0

    heap = []
    heapq.heappush(heap, (0, start))
    while heap:
        current_dist, current_node = heapq.heappop(heap)

        if current_dist > dist[current_node]:
            continue

        for next_node, cost in get_neighbors(current_node):
            new_dist = dist[current_node] + cost

            if dist[next_node] > new_dist:
                dist[next_node] = new_dist
                prev[next_node] = current_node
                heapq.heappush(heap, (new_dist, next_node))

    return dist, prev


def get_path(prev, start, end):
    path = []
    curr = end  # 从终点往回倒着找

    # 一路回溯到起点
    while curr is not None:
        path.append(curr)
        curr = prev[curr]
    
    path.reverse()  # 反转 → 变成 起点→终点 的正确顺序
    return path

# ===================== 主程序：只需要改这里的起点！ =====================
# if __name__ == "__main__":
#     # 🎯 在这里设置随机起点 (楼层, 列数)
#     START_NODE = (2, 2)
    
#     # 运行算法，计算所有结果
#     min_distance, prev_node = dijkstra(START_NODE)

#     # ========== 打印结果 ==========
#     print("=" * 70)
#     print(f"起点房间：{START_NODE}")
#     print("输出：所有房间的【最短距离】+【行走路径】")
#     print("=" * 70)

#     # 按楼层打印，清晰直观
#     for floor in FLOORS:
#         print(f"\n--- 第 {floor} 层房间 ---")
#         for col in COLS:
#             end_node = (floor, col)
#             distance = min_distance[end_node]
#             full_path = get_path(prev_node, START_NODE, end_node)
#             print(f"房间{end_node}：最短距离={distance} | 路径={full_path}")



"""
V0 手搓

"""

import heapq

FLOORS = [1, 2, 3]
COLS = [1, 2, 3, 4, 5]
ELEVATOR_COLS = [1, 5]
# ❌ 错误1：楼梯是【单个位置3】，你写成了列表 [3]
# 原因：STAIRS_COL 应该是整数 3，不是列表，虽然语法不报错，但格式不统一且冗余
STAIRS_COL = [3]

def get_neighbors(node):
    floor, col = node
    neighbors = []

    if col - 1 in COLS:
        neighbors.append(((floor, col - 1), 1))
    
    if col + 1 in COLS:
        neighbors.append( ((floor, col + 1), 1))
    
    if col in ELEVATOR_COLS:
        if floor - 1 in FLOORS:
            neighbors.append( ((floor - 1, col), 2) )
        if floor + 1 in FLOORS:
            neighbors.append( ((floor + 1, col), 2) )

    # 因为上面 STAIRS_COL 是列表，这里 col in [3] 能运行，但不规范
    if col in STAIRS_COL:
        if floor - 1 in FLOORS:
            neighbors.append( ((floor - 1, col), 3) )
        if floor + 1 in FLOORS:
            neighbors.append( ((floor + 1, col), 6) )
    
    return neighbors


def dijkstra(start):

    INF = float('inf')

    # 到每个房间的最短距离
    dist = {}
    # 每个房间都是从哪个房间过来的
    prev_node = {}

    for floor in FLOORS:
        for col in COLS:
            dist[(floor, col)] = INF
            prev_node[(floor, col)] = None

    heap = []
    heapq.heappush(heap, (0, start))

    # ❌ 错误2：【致命核心错误】！！！
    # 原因：你把所有房间距离设为无穷大，但**没有给起点赋值 dist[start] = 0**
    # 算法会认为起点的距离也是无穷大，完全无法计算最短路径
    dist[start] = 0  # 👈 这一行你彻底漏掉了，必须加！

    while heap:
        cost, current_node = heapq.heappop(heap)

        # 剪枝：如果已经有更短路径，则剪枝
        if cost > dist[current_node]:
            continue

        for next_node, step_cost in get_neighbors(current_node):

            # ❌ 错误3：算法规范错误（隐性bug）
            # 原因：不能用 cost（弹出的旧值），必须用 dist[current_node]（当前节点的最短距离）
            # 虽然小案例结果一样，但复杂场景会出bug，这是Dijkstra标准写法
            # next_cost = cost + step_cost  ❌ 你的错误写法
            next_cost = dist[current_node] + step_cost  # ✅ 正确写法

            # 更新最短路径距离和最短路径的来头
            if next_cost < dist[next_node]:
                dist[next_node] = next_cost
                prev_node[next_node] = current_node
                heapq.heappush(heap, (next_cost, next_node))
    
    return dist, prev_node

def get_path(prev, start, end):
    path = []
    curr = end

    while curr is not None:
        path.append(curr)
        curr = prev[curr]

    path.reverse()
    return path


# ===================== 主程序：只需要改这里的起点！ =====================
if __name__ == "__main__":
    # 🎯 在这里设置随机起点 (楼层, 列数)
    START_NODE = (2, 2)
    
    # 运行算法，计算所有结果
    min_distance, prev_node = dijkstra(START_NODE)

    # ========== 打印结果 ==========
    print("=" * 70)
    print(f"起点房间：{START_NODE}")
    print("输出：所有房间的【最短距离】+【行走路径】")
    print("=" * 70)

    # 按楼层打印，清晰直观
    for floor in FLOORS:
        print(f"\n--- 第 {floor} 层房间 ---")
        for col in COLS:
            end_node = (floor, col)
            distance = min_distance[end_node]
            full_path = get_path(prev_node, START_NODE, end_node)
            print(f"房间{end_node}：最短距离={distance} | 路径={full_path}")


