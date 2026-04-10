


class Solution:
    def decodeString(self, s: str) -> str:
        

        stack = []

        current_str = ""
        current_num = 0
        
        # 寻找前一个匹配的括号和数字，然后再对括号内的内容展开
        # 括号可以用栈来解决，数字也可以用一个栈，字符也可以用一个栈

        for c in s:
            if c.isdigit():

                current_num = current_num * 10 + int(c)

            elif c == '[':
                stack.append((current_str, current_num))
                current_str = ""
                current_num = 0
            elif c == ']':
                prev_str, k = stack.pop()
                current_str = prev_str + current_str * k

            else:
                current_str += c

        return current_str