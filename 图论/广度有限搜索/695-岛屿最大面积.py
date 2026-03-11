import collections
from typing import List
"""
V0
以下为深搜版本

"""
class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        # 这图可以用深搜或者广搜来解决

        if not grid:
            return None
        
        total_rows = len(grid)
        total_columns = len(grid[0])

        result_list = []

        for row_index in range(total_rows):
            for column_index in range(total_columns):
                if grid[row_index][column_index] == 1:
                    result_list.append(searchIslandArea(grid, row_index, column_index))

        return max(result_list) if len(result_list) != 0 else 0

def searchIslandArea(grid, row_index, column_index):

    if row_index < 0 or row_index >= len(grid):
        return 0
    
    if column_index < 0 or column_index >= len(grid[0]):
        return 0
    
    if grid[row_index][column_index] == 0:
        return 0

    # 覆盖为海水
    grid[row_index][column_index] = 0

    return 1 + \
        searchIslandArea(grid, row_index - 1, column_index) + \
        searchIslandArea(grid, row_index + 1, column_index) + \
        searchIslandArea(grid, row_index, column_index - 1) + \
        searchIslandArea(grid, row_index, column_index + 1)


"""
V0
以下为广搜版本
广搜需要在更高的层级建立队列,然后再一同遍历
因此才需要队列作为核心

"""



class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        # 这图可以用深搜或者广搜来解决
        directs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        rows, cols = len(grid), len(grid[0])
        ans = 0

        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 1:
                    # ❌ 错误位置：这里用了==（比较），不是=（赋值）！
                    # 您想把当前水稻格子标成0（防止重复数），但==是“判断相等”，不是“赋值”
                    # 比如a == 0是“看a是不是等于0”，a = 0才是“把a改成0”
                    grid[i][j] == 0  
                    # ✅ 正确写法：grid[i][j] = 0
                    temp_ans = 1

                    queue = collections.deque([(i, j)])
                    while queue:
                        i, j = queue.popleft()

                        for direct in directs:
                            new_i = i + direct[0]
                            new_j = j + direct[1]

                            if new_i < 0 or new_i >= rows or new_j < 0 or new_j >= cols or grid[new_i][new_j] == 0:
                                continue

                            grid[new_i][new_j] = 0

                            queue.append((new_i, new_j))

                            temp_ans += 1
                        
                    ans = max(ans, temp_ans)

        return ans






