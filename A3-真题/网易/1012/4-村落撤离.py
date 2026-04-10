

"""
V0版本，llm版

"""

import sys
import heapq



def compute_min_escape_water_level(grid):
    """
    计算逃生需要的最低水位（核心：动态规划 + 贪心优先队列 = Dijkstra）
    :param grid: 村子的海拔网格
    :return: 最低安全水位
    """
    # 获取网格大小 n*n
    grid_size = len(grid)
    # 优先队列（最小堆）：每次取出【当前路径最高海拔最低】的格子
    # 存储格式：(当前路径的最高海拔, 横坐标x, 纵坐标y)
    # 其实这里就是最优的状态
    priority_queue = [(grid[0][0], 0, 0)]
    
    # 标记：这个格子的【最优解（最低水位）】已经确定，不会再修改（DP无后效性）
    confirmed_optimal = [[False] * grid_size for _ in range(grid_size)]
    
    # 四个移动方向：上、下、左、右
    move_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # 开始贪心遍历（动态规划的核心：先算最优子问题）
    while priority_queue:
        # 取出：当前路径最高海拔最小的格子
        current_max_height, x, y = heapq.heappop(priority_queue)

        # 如果这个格子的最优解已经确定，直接跳过
        if confirmed_optimal[x][y]:
            continue
        
        # 标记：这个格子的最优解已确定，永不修改（DP无后效性）
        confirmed_optimal[x][y] = True

        # 到达终点！当前的最高海拔就是答案（最低水位）
        if x == grid_size - 1 and y == grid_size - 1:
            return current_max_height

        # 遍历上下左右四个相邻格子
        for dx, dy in move_directions:
            # 计算相邻格子的坐标
            next_x = x + dx
            next_y = y + dy

            # 判断：相邻格子在网格内 + 最优解未确定
            if 0 <= next_x < grid_size and \
                0 <= next_y < grid_size and \
                not confirmed_optimal[next_x][next_y]:
                # 新路径的最高海拔 = max(原路径最高海拔, 相邻格子的海拔)
                new_max_height = max(current_max_height, grid[next_x][next_y])

                # 把新状态加入优先队列
                heapq.heappush(priority_queue, (new_max_height, next_x, next_y))

    # 题目保证有解，这里不会执行
    return -1

def main():
    # 读取所有输入数据
    input_data = sys.stdin.read().strip().split()
    if not input_data:
        return

    # 解析输入：第一个数字是n，后面n*n个数字是网格海拔
    data_iterator = iter(input_data)
    n = int(next(data_iterator))
    
    # 构建n*n的海拔网格
    grid = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            grid[i][j] = int(next(data_iterator))

    # 计算答案并输出
    answer = compute_min_escape_water_level(grid)
    print(answer)

if __name__ == "__main__":
    main()



"""
V0 手搓版本

核心点：最小堆、Dijkstra、动态规划等

"""
import sys
import heapq

def compute_min_escape_water_level(grid):
    # 使用dijkstra进行搜索
    n = len(grid)

    # 最小堆
    # (抵达当前的最短耗时，坐标x，坐标y)
    queue = [(grid[0][0], 0, 0)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    visited = [[False for i in range(n)] for i in range(n)]

    while queue:
        # 这里一定要弹出最小的高度进行处理
        cost, x, y = heapq.heappop(queue)

        # 访问过，则不予处理
        if visited[x][y] == True:
            continue

        # 抵达终点，则返回结果
        if x == n - 1 and y == n - 1:
            return cost
        
        # 遍历四个方向
        for diff_x, diff_y in directions:
            # 四个方向一定要选最小值，么？
            next_x = x + diff_x
            next_y = y + diff_y

            if 0 <= next_x < n and 0 <= next_y < n \
                and not visited[next_x][next_y]:
                # 这里该怎么写，思考一下
                # 给出了四个方向，那么要更新队列
                # 此时要保证路径最短，那么，上下四个的最短路径，更新当前的路径

                # 这么理解，如果当前的最短路径我们已经清楚
                # 那么接下来四个状态下的最短路径我们也就都知道了，就是简单的和当前海拔比较
                # 如果当前海拔较高，那么以海拔为准，否则需要以cost为准
                # 举一个反例，比如路程要花费时间1，那么此时就不是cost，而是cost+1
                next_cost = max(cost, grid[next_x][next_y])
                heapq.heappush(queue, (next_cost, next_x, next_y))


        # 但注意,这里有一个最小堆的弹出逻辑
        # 如果是队列之类的东西,那么可能会漫无目的的搜索,举个例子,如果是距离为1, 2, 3
        # 那么从距离3搜到1的临近位置时候,更新了最短路径,但这里不再是最短路径了,因为它违背了我们说的不再更新的原则
        # 这样会导致结果都是错的

    return -1

def main():

    inputs = sys.stdin.read().strip().split()
    inputs = iter(inputs)

    n = int(next(inputs))

    # 初始化网格
    grid = [[0 for i in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            grid[i][j] = int(next(inputs))

    # 搜索网格
    print(compute_min_escape_water_level(grid))

