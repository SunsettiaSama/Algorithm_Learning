"""
=============
V0
=============
"""

class Solution:
    def isPalindrome(self, s: str) -> bool:
        
        left_index = 0
        right_index = 1  # ERROR 1：右指针初始化错误，应指向字符串末尾（len(s)-1），而非索引1
        
        s = s.lower() # 注：转小写逻辑本身没错，但注释标注为ERROR是你自己的疑问，实际是正确操作（忽略大小写）
        s.replace(' ', '')  # ERROR 2：①只去除空格，未过滤标点/符号等非字母数字；②replace返回新字符串，未赋值，等于没执行；③注释错误（需求是保留数字，而非去除）

        while left_index < right_index:  # 循环条件本身没错，但指针移动逻辑错误导致无意义

            left_s = s[left_index]
            right_s = s[right_index]

            if not left_s == right_s:  # ERROR 3：未跳过非字母/数字字符，直接比较（比如遇到标点会误判）
                return False

            left_index += 1
            right_index += 1  # ERROR 4：右指针应向左移动（-=1），而非向右（+=1），相向双指针核心逻辑错误

        return True

"""
=============
V1
=============
"""

class Solution:
    def isPalindrome(self, s: str) -> bool:
        
        # ERROR 1：列表初始化错误
        # ① extend是原地操作，返回None，导致num_list = None；② 逻辑完全反了（题目要求保留数字，你却想把数字加入过滤列表）；③ 仅考虑空格+数字，未过滤标点/符号等非字母数字
        num_list = [' '].extend([f'{i}' for i in range(10)])

        # ERROR 2：注释错误（你标注为ERROR，但right_index = len(s)-1是正确的！）
        # 补充：未处理len(s)=0的边界（如s=""时，len(s)-1=-1，后续循环直接不执行，返回True，虽结果对但可补充边界判断）
        right_index = len(s) - 1 # ERROR：右侧永远是-1，这个点总是会不太记得

        # ERROR 3：注释错误（你标注为ERROR，但s.lower()是正确操作，用于忽略大小写）
        s = s.lower() # ERROR: 这里需要记忆, 大小写

        while left_index < right_index:
            left_s = s[left_index]
            right_s = s[right_index]

            # ERROR 4：过滤逻辑错误
            # ① 只过滤空格+数字（违背题目要求：保留数字）；② 仅单次跳过（连续多个非有效字符时只跳一个）；③ 跳过字符后直接取新索引值，未判断left_index < right_index，易导致索引越界
            if left_s in num_list:
                left_index += 1
                left_s = s[left_index]
            elif right_s in num_list:
                right_index -= 1
                right_s = s[right_index]

            # ERROR 5：比较逻辑错误（跳过字符后未重新判断left_index < right_index，直接比较，可能越界或错误比较）
            if not left_s == right_s:
                return False

            left_index += 1
            right_index -= 1

        return True


"""
=============
V1 豆包修复版
=============
"""

class Solution:
    def isPalindrome(self, s: str) -> bool:
        # 【记忆点1】初始化相向双指针：左头右尾
        left = 0
        right = len(s) - 1
        # 【记忆点2】统一转小写（忽略大小写）
        s_lower = s.lower()

        while left < right:
            # 调用封装的跳过函数，更新指针位置
            left = self._skip_non_alnum_left(s_lower, left, right)
            right = self._skip_non_alnum_right(s_lower, left, right)

            # 指针相遇则说明所有有效字符已比较完
            if left >= right:
                break

            # 核心比较逻辑：有效字符不相等则不是回文
            if s_lower[left] != s_lower[right]:
                return False

            # 指针向中间移动
            left += 1
            right -= 1

        return True

    # 封装：左指针向右跳过所有非字母/数字字符
    def _skip_non_alnum_left(self, s: str, left: int, right: int) -> int:
        """
        左指针从当前位置向右跳，直到找到字母/数字 或 left >= right
        :param s: 小写后的字符串
        :param left: 当前左指针位置
        :param right: 右指针位置（避免越界）
        :return: 更新后的左指针位置
        """
        while left < right and not s[left].isalnum():
            left += 1
        return left

    # 封装：右指针向左跳过所有非字母/数字字符
    def _skip_non_alnum_right(self, s: str, left: int, right: int) -> int:
        """
        右指针从当前位置向左跳，直到找到字母/数字 或 left >= right
        :param s: 小写后的字符串
        :param left: 左指针位置（避免越界）
        :param right: 当前右指针位置
        :return: 更新后的右指针位置
        """
        while left < right and not s[right].isalnum():
            right -= 1
        return right



"""
=============
V2
=============
"""
class Solution:
    def isPalindrome(self, s: str) -> bool:
        
        left_index = 0
        right_index = len(s) - 1

        while left_index < right_index:

            left_index = skip_nums(s, index = left_index, left = left_index, right = right_index, step = 1)
            right_index = skip_nums(s, index = right_index, left = left_index, right = right_index, step = -1)
            
            if not left_index < right_index:
                break

            if s[left_index] != s[right_index]:
                return False
            
            left_index += 1
            right_index -= 1
        
        return True

def skip_nums(s: str, index, left, right, step = 1):

    # ERROR 判定条件错误，左指针不应该大于右指针
    # ERROR 这里的逻辑需要重构
    while left < right and not s[index].isalnum(): # ERROR: 这里需要一个内置函数才行，得记住
        index += step
    
    return index


"""
=============
V3 20260303
=============
"""
class Solution:
    def isPalindrome(self, s: str) -> bool:
        left_index = 0
        right_index = len(s) - 1
        # ERROR: 没有全部转成小写
        while left_index < right_index:
            
            left_index = skip_left_nums(left_index, right_index, s) # ERROR：没有加上判定条件，所有字符应当比较完成后，要跳出循环
            right_index = skip_right_nums(left_index, right_index, s)

            if not s[left_index] == s[right_index]:
                return False

            left_index += 1
            right_index -= 1
        
        return True
    

def skip_left_nums(left_index, right_index, s:str):
    while left_index < right_index and not s[left_index].isalnum():
        left_index += 1
    return left_index

def skip_right_nums(left_index, right_index, s:str):
    while left_index < right_index and not s[right_index].isalnum():
        right_index -= 1
    return right_index





"""
=============
V3 20260303 修复版
=============
"""
class Solution:
    def isPalindrome(self, s: str) -> bool:
        left_index = 0
        right_index = len(s) - 1
        s = s.lower()

        while left_index < right_index:
            
            left_index = skip_left_nums(left_index, right_index, s) 
            right_index = skip_right_nums(left_index, right_index, s)

            if left_index == right_index: 
                break
            if not s[left_index] == s[right_index]:
                return False

            left_index += 1
            right_index -= 1
        
        return True
    
# !!请注意，这里判定语句中，left_index < right_index作为条件，然后再让left_index += 1，这会使得在某些情况下
# left_index会和right_index相撞
# 举例而言，如果left = 3，right = 4，下述判定依然成立，+1会使得left == right
# 也就是说：
#             if left_index == right_index: 
#                 break
# 等于就够用了，不需要小于

def skip_left_nums(left_index, right_index, s:str):
    while left_index < right_index and not s[left_index].isalnum(): 
        left_index += 1
    return left_index

def skip_right_nums(left_index, right_index, s:str):
    while left_index < right_index and not s[right_index].isalnum():
        right_index -= 1
    return right_index