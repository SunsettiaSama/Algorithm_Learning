




# 查括号，这不是堆栈么，我记得，左括号入栈，右括号匹配，然后看嵌套程度如何


import sys

def get_input():
    lines = sys.stdin.read().strip().split("\n")

    return lines

def is_available(s):

    if len(s) <= 4:
        return False
    
    # 使用堆栈
    stack = []
    # 左括号
    format_string = ""

    # 从左向右扫
    for index in range(len(s)):

        # 如果是左花括号，入栈
        if s[index] == "{":
            stack.append("{")

        # 如果是右花括号，则弹出栈
        elif s[index] == "}":
            stack.pop()

        # 进入普通字符串的判定
        # 遇到字符串时：
            # 堆栈内为1个括号，则弹出否
            # 堆栈括号大于三个，则弹出否
        elif s[index] == "}" and s[index - 1] == "{":
            return False

        else:
            if len(stack) == 1 or len(stack) > 2:
                return False
            # 其他情况则记录字符串是否有效，作为模板字符串
            format_string += s[index]
    
    return len(format_string.strip()) > 0 and len(stack) == 0 # ERROR 忘记了，要检查堆栈是否是0啊！！！

def main():


    lines = get_input()
    for s in lines:
        print(str(is_available(s)).lower())

if __name__ == "__main__":
    main()