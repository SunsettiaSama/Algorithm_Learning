class Solution:
    def isValid(self, s: str) -> bool:
        # 1. 奇数长度直接返回False（和原代码一致，这步很关键）
        if len(s) % 2 != 0:
            return False
        
        # 2. 字典映射：右括号 → 对应的左括号（核心优化点）
        bracket_map = {')': '(', ']': '[', '}': '{'}
        stack = []
        
        for char in s:
            # 3. 如果是右括号：查字典找对应左括号，判断是否匹配
            if char in bracket_map:
                # 栈空 或 栈顶不是对应左括号 → 不合法
                if not stack or stack[-1] != bracket_map[char]:
                    return False
                # 匹配成功，弹出栈顶
                stack.pop()
            # 4. 如果是左括号：直接入栈
            else:
                stack.append(char)
        
        # 5. 栈空说明全部匹配，否则有剩余左括号
        return len(stack) == 0