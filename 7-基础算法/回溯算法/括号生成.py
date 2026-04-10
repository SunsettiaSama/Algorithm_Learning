class Solution:
    def generateParenthesis(self, n: int):
        parentheses = []            # 存放所有括号组合
        parenthesis = []            # 存放当前括号组合
        def backtrack(symbol, index):
            # 选择，复杂的选择
            # 但核心的选择为index位置的括号字符串

            # 这里又有所创新，原来的回溯算法递归层总是一个列表，因此一个for就可以搞定
            # 但是这个题目不同，这个题目给的选择不多
            # 关键在于是否有额外的budget
                # 分支一：在添加了左括号后，budget就会+1
                # 分支二：而在选择了右括号，则budget-1
            # 每个分支的回溯得单独写出来
            
            # 递归终止条件
            if 2 * n == index: # 必须在最后一步的时候花光右括号的预算，才算依次完整的结果
                if symbol == 0: 
                    parentheses.append("".join(parenthesis))
                    return 
                
            
            else:
                if symbol < n:
                    # 进入选择一：
                    parenthesis.append("(")
                    backtrack(symbol = symbol + 1, index = index + 1)
                    parenthesis.pop()
                if symbol > 0:
                    parenthesis.append(")")
                    backtrack(symbol = symbol - 1, index = index + 1)
                    parenthesis.pop()
        backtrack(0, 0)
        return parentheses
    