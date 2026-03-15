
"""
思考一下，图论DFS几大组件

1. 当前节点判断模块：判断该节点怎么个事情
2. 当前节点处理模块：针对该节点要做什么动作
3. 邻接点获取块：获取该节点的附近节点，可以是子节点，也可以是临近节点
4. 递归模块：组装节点判断模块
    - 判断模块作为终止条件
    - 处理模块处理当前节点
    - 邻接点获取模块指定下一个探索的方向
5. 题解模块：这个就用来处理题解，相当于main部分
"""


"""
V0

"""

class Solution:
    def isValid(self, grid, curr_row, curr_col):
        if  0 <= curr_row < len(grid) and 0 <= curr_col < len(grid[0]) and grid[curr_row][curr_col] == "1":
            return True

        return False
    
    def processNode(self, grid, curr_row, curr_col):
        """"""
        # 标记为已经处理
        grid[curr_row][curr_col] = "0"

    def get_neighbors(self, curr_row, curr_col):
        return [(curr_row -1, curr_col), (curr_row +1, curr_col), (curr_row , curr_col-1), (curr_row, curr_col+1)]

    def dfs(self, grid, curr_row, curr_col):
        
        # 递归终止条件：当前节点是否可用
        if not self.isValid(grid, curr_row, curr_col):
            return 
        
        # 处理当前节点
        self.processNode(grid, curr_row, curr_col)

        # 递归体：处理2d平面每个点
        for neighbor_row, neighbor_col in self.get_neighbors(curr_row, curr_col):
            self.dfs(grid, neighbor_row, neighbor_col)
        
    
    def numIslands(self, grid):
        if not grid or not grid[0]:
            return 0
        
        count = 0
        total_row, total_col = len(grid), len(grid[0])

        for i in range(total_row):
            for j in range(total_col):
                if grid[i][j] == '1':
                    self.dfs(grid, curr_row = i, curr_col = j)
                    count += 1
                
        return count
    

"""
V1 
"""
class Solution:
    def numIslands(self, grid):
        # 边界
        if not grid or not grid[0]:
            return 0
        
        counts = 0

        # 启用深度搜索，对每个相邻点，进行以深度优先的岛屿搜索过程
        # 先标记grid，以供修改
        for m in range(len(grid)):
            for n in range(len(grid[0])):
                if grid[m][n] == 1:
                    # ERROR 1：递归函数searchIsland可能返回None（边界条件触发时），赋值给grid会导致后续遍历报错
                    grid = self.searchIsland(grid, m, n)
                    counts += 1

        return counts

    def searchIsland(self, grid, m, n):
        # ERROR 2：边界条件错误，索引合法范围是m >=0 and m < len(grid)、n >=0 and n < len(grid[0])，用m<=0/n<=0会误判m=0/n=0为越界
        if m >= len(grid) or m <= 0 or n >= len(grid[0]) or n <= 0:
            return  # ERROR 3：此处无返回值，主函数接收后grid会被赋值为None
        
        if grid[m][n] == 0:
            return  # ERROR 3：同上，无返回值
        
        # 对当前格子进行处理
        if grid[m][n] == 1:
            # ERROR 4：修改为字符串"0"，与原grid中的整数1/0类型不一致，后续判断grid[m][n]==1会失效（如递归中再次访问该位置时）
            grid[m][n] = "0"

        # ERROR 1延续：递归调用返回值赋值给grid，叠加None风险；且列表是可变对象，无需返回赋值，直接修改即可
        grid = self.searchIsland(grid, m - 1, n)
        grid = self.searchIsland(grid, m + 1, n)
        grid = self.searchIsland(grid, m, n - 1)
        grid = self.searchIsland(grid, m, n + 1)

        return grid
    
"""
V1 修复版：思路没问题，代码自己有问题
"""
class Solution:
    def numIslands(self, grid) -> int:
        def dfs(grid, i, j):
            if not 0 <= i < len(grid) or not 0 <= j < len(grid[0]) or grid[i][j] == '0': return
            grid[i][j] = '0'
            dfs(grid, i + 1, j)
            dfs(grid, i, j + 1)
            dfs(grid, i - 1, j)
            dfs(grid, i, j - 1)
        count = 0
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == '1':
                    dfs(grid, i, j)
                    count += 1
        return count
    
"""
V2
"""
from typing import List

class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        
        # 边界
        if not grid:
            return None
        
        total_rows = len(grid)
        total_columns = len(grid[0])

        # 计数器，最外围：counts
        counts = 0

        for row_index in range(total_rows):
            for column_index in range(total_columns):
                # 如果为陆地，则展开搜索
                if grid[row_index][column_index] == "1":
                    counts += 1
                    searchIsland(grid, row_index, column_index)
        
        return counts


def searchIsland(grid, row_index, column_index):

    # 这里需要一个递归体
    # 边界判定
    if row_index < 0 or row_index > len(grid) - 1:
        return 
    
    if column_index < 0 or column_index > len(grid[0]) - 1:
        return 
    
    # 如果当前格为海水，不执行
    if grid[row_index][column_index] == "0":
        return 
    
    # 执行递归内容
    grid[row_index][column_index] = "0"

    # 调用递归
    # 上下左右
    searchIsland(grid, row_index - 1, column_index)
    searchIsland(grid, row_index + 1, column_index)
    searchIsland(grid, row_index, column_index - 1)
    searchIsland(grid, row_index, column_index + 1)


"""
V3 手搓版本

"""

from typing import List

class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        
        # 深搜DFS
        row_nums = len(grid)
        col_nums = len(grid[0])

        counts = 0

        for row_index in range(row_nums):
            for col_index in range(col_nums):

                if grid[row_index][col_index] == "1":
                    counts += 1
                    self.searchIsland(grid, row_index, col_index)
        
        return counts

        
    # 岛屿搜索
    def searchIsland(self, grid, row_index, col_index):
        
        if row_index < 0 or row_index >= len(grid) or col_index < 0 or col_index >= len(grid[0]):
            return 

        if grid[row_index][col_index] == "0":
            return 
        
        # DFS
        grid[row_index][col_index] = "0"

        # 上下左右拓展，深度搜索
        self.searchIsland(grid, row_index + 1, col_index)
        self.searchIsland(grid, row_index - 1, col_index)
        self.searchIsland(grid, row_index, col_index + 1)
        self.searchIsland(grid, row_index, col_index - 1)


"""
V3 手搓版本

BFS

"""
from collections import deque

class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        # BFS
        row_nums = len(grid)
        col_nums = len(grid[0])  # 问题1：未处理grid为空的情况（比如grid=[]），直接取grid[0]会报错

        counts = 0

        for row_index in range(row_nums):
            for col_index in range(col_nums):
                if grid[row_index][col_index] == "1":
                    counts += 1
                    self.searchIsland(grid, row_index, col_index)
        
        return counts
    
    def searchIsland(self, grid, row_index, col_index):
        # BFS核心：队列初始化
        queue = deque()
        queue.append((row_index, col_index))

        while queue:
            # 取出队列头部元素
            curr_row_index, curr_col_index = queue.popleft()

            # 问题2：未检查坐标是否越界（比如row=-1/row>=行数，列同理），直接访问grid会触发索引越界报错
            # 问题3：逻辑死循环！判断当前是"1"就把自己重新加入队列，队列永远不为空，无限循环
            if grid[curr_row_index][curr_col_index] == "1":
                queue.append((curr_row_index, curr_col_index))
            
            # 问题4：仅把当前节点置为"0"，未遍历上下左右四个方向，无法把整个岛屿的"1"都置为"0"，导致重复计数
            grid[curr_row_index][curr_col_index] = "0"

        return 
    


    def searchIsland(self, grid, row_index, col_index):
        row_nums = len(grid)
        col_nums = len(grid[0])
        queue = deque()
        # 先把初始陆地置为"0"（避免重复加入队列），再加入队列
        grid[row_index][col_index] = "0"
        queue.append((row_index, col_index))

        # 定义上下左右四个方向（核心：遍历相邻陆地）
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            # 取出当前陆地坐标
            curr_row, curr_col = queue.popleft()

            # 遍历四个方向的相邻坐标（修复问题4）
            for dr, dc in directions:
                new_row = curr_row + dr
                new_col = curr_col + dc

                # 检查新坐标是否有效（不越界）+ 是未访问的陆地（修复问题2）
                if 0 <= new_row < row_nums and 0 <= new_col < col_nums and grid[new_row][new_col] == "1":
                    # 置为"0"标记已访问，避免重复处理（修复问题3）
                    grid[new_row][new_col] = "0"
                    # 加入队列，后续处理它的相邻陆地
                    queue.append((new_row, new_col))
        return





