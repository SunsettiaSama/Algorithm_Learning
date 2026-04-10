

class Solution:
    def findPaths(self, m: int, n: int, maxMove: int, startRow: int, startColumn: int) -> int:
        MOD = 10**9 + 7
        # 方向数组：上下左右
        dirs = [(-1,0), (1,0), (0,-1), (0,1)]
        # 优化空间：只用两个二维数组（当前步、上一步）
        prev_dp = [[0]*n for _ in range(m)]
        prev_dp[startRow][startColumn] = 1  # 初始状态
        res = 0
        
        for _ in range(maxMove):
            curr_dp = [[0]*n for _ in range(m)]                                                                                                 
            for i in range(m):
                for j in range(n):
                    if prev_dp[i][j] == 0:
                        continue
                    # 遍历四个方向
                    for dx, dy in dirs:
                        ni, nj = i + dx, j + dy
                        # 出界：累加路径数到结果
                        if ni < 0 or ni >= m or nj < 0 or nj >= n:
                            res = (res + prev_dp[i][j]) % MOD
                        # 未出界：累加到当前步的位置
                        else:
                            curr_dp[ni][nj] = (curr_dp[ni][nj] + prev_dp[i][j]) % MOD
            prev_dp = curr_dp
        
        return res
    
"""

例:递归解法:
"""

class Solution:
    def findPaths(self, m: int, n: int, maxMove: int, startRow: int, startColumn: int) -> int:
        MOD = 10**9 + 7
        # 记忆化缓存：memo[i][j][k] 表示从(i,j)出发，剩余k步时出界的路径数
        memo = [[[-1]* (maxMove + 1) for _ in range(n)] for __ in range(m)]
        
        # 递归函数：i,j=当前位置，k=剩余移动次数
        def dfs(i, j, k):
            # 终止条件1：出界 → 路径有效，返回1
            if i < 0 or i >= m or j < 0 or j >= n:
                return 1
            # 终止条件2：步数用完但没出界 → 路径无效，返回0
            if k == 0:
                return 0
            # 记忆化：如果已经计算过，直接返回缓存值
            if memo[i][j][k] != -1:
                return memo[i][j][k]
            
            # 递归计算四个方向的路径数之和
            up = dfs(i-1, j, k-1)
            down = dfs(i+1, j, k-1)
            left = dfs(i, j-1, k-1)
            right = dfs(i, j+1, k-1)
            
            # 缓存结果并取模（防止数值溢出）
            memo[i][j][k] = (up + down + left + right) % MOD
            return memo[i][j][k]
        
        # 初始调用：起始位置，剩余maxMove步
        return dfs(startRow, startColumn, maxMove)


"""
V0 动态规划算法

"""

class Solution:
    def findPaths(self, m: int, n: int, maxMove: int, startRow: int, startColumn: int) -> int:
        MOD = 10 ** 9 + 7

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        # 初始化动态规划
        # 注意，这里用到了两个步，一个是当前步、一个是上一步，两个棋盘
        dp = [[0 for i in range(n)] for j in range(m)]
        dp[startRow][startColumn] = 1  # 初始状态正确：0次移动时，球在起始位置的路径数为1
        ans = 0

        for _ in range(maxMove):
            # 错误1：prev_dp初始化逻辑完全颠倒
            # 错误原因：prev_dp应该承接上一轮的dp（即移动k-1次后的路径数），但此处每次循环都初始化为全0，
            # 导致后续判断prev_dp[row_idx][col_idx]时直接跳过所有逻辑，没有任何路径数被处理
            prev_dp = [[0 for i in range(n)] for j in range(m)]
            
            for row_idx in range(m):
                for col_idx in range(n):
                    # 错误2：判断条件写反 + 逻辑错误
                    # 错误原因：prev_dp刚被初始化为全0，此条件等价于"if 0:"，会直接continue跳过所有格子的处理，
                    # 正确逻辑应该是：判断上一轮的dp（即当前的prev_dp）中该位置是否有路径数（>0），若没有则跳过；
                    # 且此处应该用dp（上一轮的状态）而非prev_dp（新初始化的空数组）
                    if prev_dp[row_idx][col_idx]:
                        continue

                    # 假设现在dp每一个格子就是一个贪婪解？不对，这里的dp含义应该是移动k次后，球到row_idx, col_idx的路径数
                    for dx, dy in directions:
                        # 错误3：出界判断条件错误（> 改为 >=）
                        # 错误原因：网格的行索引范围是0~m-1，列是0~n-1，出界条件应为">=m"或"<0"，而非">m"；
                        # 例如m=2时，row_idx+dx=2就已经出界，但2>2不成立，会错误判定为未出界
                        if row_idx + dx < 0 or row_idx + dx > m or col_idx + dy < 0 or col_idx + dy > n:
                            # 错误4：累加的路径数来源错误
                            # 错误原因：prev_dp[row_idx][col_idx]此时是0（刚初始化），正确应该累加的是上一轮dp中该位置的路径数（dp[row_idx][col_idx]）
                            ans += prev_dp[row_idx][col_idx]
                            continue

                        # 错误5：路径数更新逻辑完全错误
                        # 错误原因：1. 应该从当前位置(row_idx, col_idx)移动到新位置(row_idx+dx, col_idx+dy)，
                        # 而非更新原位置；2. 应该用上一轮的dp值（dp[row_idx][col_idx]）累加，而非prev_dp（空值）；
                        # 3. prev_dp是当前轮要更新的数组，而非dp
                        dp[row_idx][col_idx] = (dp[row_idx][col_idx] + prev_dp[row_idx][col_idx]) % MOD
                        
                        # 错误6：prev_dp赋值时机+方式错误
                        # 错误原因：1. 在方向循环内直接将prev_dp赋值为dp，会导致浅拷贝且覆盖当前轮的更新；
                        # 2. 正确时机应该是每轮maxMove循环结束后，将prev_dp更新为当前轮的curr_dp
                        prev_dp = dp
                    
        return ans % MOD
    


"""
V1 递归手搓

"""
MOD = 10**9 + 7

class Solution:
    def findPaths(self, m: int, n: int, maxMove: int, startRow: int, startColumn: int) -> int:
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        # 记忆化递归
        memo = dict()
        # 构筑递归

        def dfs(i, j, k):
            # 假设在第i, j个格子时，k为剩余步数
            # 错误1：边界判断逻辑错误（优先级+越界条件）
            # 1. and优先级高于or，导致条件等价于 i<0 or i>m or j<0 or (j>n and k>=0)，逻辑完全错误
            # 2. 越界条件错误：矩阵行范围是0~m-1，列是0~n-1，应该是i>=m 而非i>m，j>=n而非j>n
            # 3. k>=0是冗余条件（k是剩余步数，递归中k只会>=0）
            if i < 0 or i > m or j < 0 or j > n and k >= 0: # if i < 0 or i >= m or j < 0 or j >= n:
                return 1
            
            # 反之，在界内
            if k == 0:
                return 0
            
            if (i, j, k) in memo:
                return memo[(i, j, k)]

            # 计算第i、j步还能往哪边走
            # 四个方向都尝试一下
            res = 0
            # 错误2：变量拼写错误：j_idff 应为 j_diff
            for i_diff, j_idff in directions:
                res += dfs(i + i_diff, j + j_idff, k - 1)
                # 错误3：累加时未取模，可能导致中间值溢出（即使最后取模，大数累加也会降低效率）

            memo[(i, j, k)] = res % MOD
            return memo[(i, j, k)]
        
        return dfs(startRow, startColumn, maxMove)


"""
V1 递归修复

"""
MOD = 10**9 + 7

class Solution:
    def findPaths(self, m: int, n: int, maxMove: int, startRow: int, startColumn: int) -> int:
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        # 记忆化递归
        memo = dict()
        # 构筑递归

        def dfs(i, j, k):
            if i < 0 or i >= m or j < 0 or j >= n: # 
                return 1
            
            # 反之，在界内
            if k == 0:
                return 0
            
            if (i, j, k) in memo:
                return memo[(i, j, k)]

            # 计算第i、j步还能往哪边走
            # 四个方向都尝试一下
            res = 0
            # 错误2：变量拼写错误：j_idff 应为 j_diff
            for i_diff, j_idff in directions:
                res += dfs(i + i_diff, j + j_idff, k - 1) % MOD

            memo[(i, j, k)] = res % MOD
            return memo[(i, j, k)]
        
        return dfs(startRow, startColumn, maxMove)


"""
V1 动态规划算法 手搓

"""

MOD = 10**9 + 7
import copy

class Solution:
    def findPaths(self, m: int, n: int, maxMove: int, startRow: int, startColumn: int) -> int:

        directions = [(-1,0), (1,0), (0,-1), (0,1)]

        # 初始化，很显然，初始化 一个网格
        # 每个网格代表当前位置可以将球移出边界的路径数
        dp = [[0 for i in range(n)] for j in range(m)] # ERROR: 行和列方向错误
        
        # 初始化错误
        dp[startRow][startColumn] = 1

        dp_each_step = self.build_prev_grid(m, n, directions)

        # 那么关键就在于，需要一新一旧的网格，在时间步长上，如果在第i步，走到第i+1步，那么会产生多少个出界的可能
        # ERROR:需要copy一个新的网格以实现逻辑,不能在原网格上修改,原网格上修改会炸,所以不行
        for k in range(1, maxMove + 1):
            prev_dp = copy.deepcopy(dp)

            for i in range(m):
                for j in range(n):
                    # 一定不会出界，这是前提条件
                    # 所以其实是四个格子叠加到当前格子，然后还要求不能出界
                    # 出界就炸
                    for i_diff, j_diff in directions:
                        if not (i + i_diff < 0 or i + i_diff >= m or j + j_diff < 0 or j + j_diff >= n):
                            dp[i][j] = (prev_dp[i + i_diff][j + j_diff] + dp_each_step[i][j]) % MOD

        return dp[startRow][startColumn] % MOD

    def build_prev_grid(self, m, n, directions):

        # 从第i步走到第i+1步
        dp_each_step = [[0 for i in range(n)] for j in range(m)]

        for i in range(m):
            for j in range(n):
                for i_diff, j_diff in directions:
                    if i + i_diff < 0 or i + i_diff >= m or j + j_diff < 0 or j + j_diff >= n:
                        dp_each_step[i][j] = (dp_each_step[i][j] + 1) % MOD

        return dp_each_step




"""
V1 动态规划算法 修复版

"""



MOD = 10**9 + 7

class Solution:
    def findPaths(self, m: int, n: int, maxMove: int, startRow: int, startColumn: int) -> int:

        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        # 初始化，很显然，初始化 一个网格
        # 每个网格代表当前位置可以将球移出边界的路径数
        prev_dp = [[0 for i in range(n)] for j in range(n)]

        # 所以,状态转移方程不仅仅是空间上的,更是在其他方向上也可以发生状态转移方程
        # 比如之前的题目就是i i+1 j j+1的关系,也即空间上的关系,而在该题目中,状态转移发生在步长上,和空间完全无关,反而和时间相关,类比一下的话

        for k in range(1, maxMove + 1):
            curr_dp = [[0 for _ in range(n)] for _ in range(m)]

            for i in range(m):
                for j in range(n):
                    for di, dj in directions:
                        ni, nj = i + di, j + dj

                        if ni < 0 or ni >= m or nj < 0 or nj >= n:
                            curr_dp[i][j] = (curr_dp[i][j] + 1) % MOD
                        else:
                            curr_dp[i][j] = (curr_dp[i][j] + prev_dp[ni][nj]) % MOD
        
            prev_dp = curr_dp

        return prev_dp[startRow][startColumn]


