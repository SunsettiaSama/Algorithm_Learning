class Solution:
    res = []
    
    # 回溯体
    def backtrack(self, n, row, chessboard):
        """
        row: 当前行
        """
        # 也是递归体
        # 递归终止条件：所有的皇后都已得到了放置
        if row == n:
            # 记录结果
            # 将其整理为棋盘
            temp_result = []
            for temp_result_list in chessboard:
                temp_result_string = "".join(temp_result_list)
                temp_result.append(temp_result_string)
            Solution.res.append(temp_result)
            return 
        
        # 回溯体的选择与回溯
        for col in range(n):
            if self.isValid(n = n, row = row, col = col, chessboard = chessboard):
                chessboard[row][col] = "Q" # 选择
                self.backtrack(n, row = row + 1, chessboard = chessboard)
                chessboard[row][col] = "." # 回溯选择

    def isValid(self, n: int, row: int, col: int, chessboard):

        # 首先，该行只会有一个Q，不会有多个Q
        # 所以不用检查行，只需要检查列
        for line in chessboard:
            if line[col] == "Q":
                return False
            
        # 检查左对角线
        rowi, coli = row - 1, col - 1
        while rowi >= 0 and coli >= 0:
            if chessboard[rowi][coli] == "Q":
                return False
            
            rowi -= 1
            coli -= 1
        
        # 检查右上角
        rowi, coli = row - 1, col + 1
        while rowi >= 0 and coli < n:
            if chessboard[rowi][coli] == "Q":
                return False
            
            rowi -= 1
            coli += 1
        
        return True
        
    def solveNQueens(self, n: int):
        self.res.clear()
        chessboard = [['.' for _ in range(n)] for _ in range(n)]
        self.backtrack(n, 0, chessboard)

        return Solution.res
    

if __name__ == "__main__":
    s = Solution()
    result = s.solveNQueens(4)
    for chessboard in result:
        print("=" * 20)
        for row in chessboard:
            print(row)
