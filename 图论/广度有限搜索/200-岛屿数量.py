

from typing import List
import collections

class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        
        if not grid or not grid[0]:
            return 0
        
        row_nums = len(grid)
        col_nums = len(grid[0])
        count = 0

        def searchIsland(row, col):

            # bfs，队列中存储的应该是需要处理的位置
            queue = collections.deque()
            queue.append((row, col))

            grid[row][col] = '0'

            while queue:

                curr_row, curr_col = queue.popleft()
                directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

                for diff_row, diff_col in directions:

                    new_row = curr_row + diff_row
                    new_col = curr_col + diff_col

                    if 0 <= new_row < row_nums and 0 <= new_col < col_nums and grid[new_row][new_col] == '1':
                        # 标记已访问，避免重复入队
                        grid[new_row][new_col] = '0'
                        # 邻域入队，后续处理
                        queue.append((new_row, new_col))
            
        for i in range(row_nums):
            for j in range(col_nums):
                if grid[i][j] == '1':
                    count += 1
                    searchIsland(i, j)
        
        return count


"""

V0 复刻

"""
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        # 错误1：空网格返回值错误（题目要求返回岛屿数量，应返回0而非None；且未判断grid[0]为空的情况）
        if not grid:
            return None
        
        row_nums = len(grid)
        col_nums = len(grid[0])
        counts = 0

        def searchIsland(row_index, col_index):
            queue = collections.deque()
            queue.append((row_index, col_index))
            directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]

            while queue:
                # 错误2：未取出队列中的元素（BFS核心！队列里的坐标永远不会被处理，只堆不拿）
                # 错误3：标记已访问的坐标错误（一直修改初始的row_index/col_index，而非队列取出的当前坐标）
                grid[row_index][col_index] = '0'

                # 向四个方向搜索
                for row_diff, col_diff in directions:
                    if row_index + row_diff >= row_nums or row_index + row_diff < 0 or col_index + col_diff >= col_nums or col_index + col_diff < 0:
                        continue
                    
                    if grid[row_index + row_diff][col_index + col_diff] == '1':
                        grid[row_index + row_diff][col_index + col_diff] = '0'
                        # 错误4：邻域入队后永远不会被处理（因为没取队首，队列只加不减）
                        queue.append((row_index + row_diff, col_index + col_diff))
        
        # 错误5：外层触发条件完全反了（应该是grid[i][j] == '1'时启动BFS，而非'0'）
        for row_index in range(row_nums):
            for col_index in range(col_nums):
                if grid[row_index][col_index] == '0':
                    counts += 1
                    searchIsland(row_index, col_index)
        
        return counts

"""

V0 修复
"""

class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        # 错误1：空网格返回值错误（题目要求返回岛屿数量，应返回0而非None；且未判断grid[0]为空的情况）
        if not grid:
            return None
        
        row_nums = len(grid)
        col_nums = len(grid[0])
        counts = 0

        def searchIsland(row_index, col_index):
            queue = collections.deque()
            queue.append((row_index, col_index))
            directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]

            while queue:
                # 先取出
                row_index, col_index = queue.popleft()
            
                grid[row_index][col_index] = '0'

                # 向四个方向搜索
                for row_diff, col_diff in directions:
                    if row_index + row_diff >= row_nums or row_index + row_diff < 0 or col_index + col_diff >= col_nums or col_index + col_diff < 0:
                        continue
                    
                    if grid[row_index + row_diff][col_index + col_diff] == '1':
                        grid[row_index + row_diff][col_index + col_diff] = '0'

                        queue.append((row_index + row_diff, col_index + col_diff))
        
        for row_index in range(row_nums):
            for col_index in range(col_nums):
                if grid[row_index][col_index] == '1':
                    counts += 1
                    searchIsland(row_index, col_index)
        
        return counts


