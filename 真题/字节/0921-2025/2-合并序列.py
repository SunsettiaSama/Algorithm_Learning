

import sys

def get_input():

    lines = sys.stdin.read().split()
    n, k = map(int, lines[0]), map(int, lines[1])

    return n, k


def merge(array, k):
    """
    合并最长为k处的字串
    """
    if not array:
        return array
    
    # 双指针的做法，三种指针中选择快慢指针
    slow = 0
    fast = 0
    # 注意，快慢指针的终止条件有点模糊
    while fast < len(array):
        
        # 更新的方法也有点模糊了

        # 更新快指针，看看快指针和慢指针是否一致
        # 如果字符一致，那么扩大区间
        if array[fast] == array[slow] and fast - slow <= k:
            fast += 1
        # 否则，合并区间
        # 并且同步快慢指针
        else:
            array[slow: fast] = sum(array[slow: fast])
            slow = fast
    
    return array

# 那么此时的思路和当初做的那个最长重复序列很像，需要一个双指针搜索合并区间，然后重复搜索
def main():

    n, k = get_input()

    # 此时创建一个新的队列
    array = []

    # 外循环应该是n次操作，也就是for
    for index in range(n):
        array.append(1)
        # 检测是否有需要合并的项，尽可能合并
        array = merge(array, k)

    
    # 合并完成后，输出结果
    return array



"""
豆包认为，这道题本质上是数学规律题，给了个进制表示的解法

"""

def main():
    import sys
    input_line = sys.stdin.read().split()
    n = int(input_line[0])
    k = int(input_line[1])
    
    if n == 0:
        print()
        return
    
    # 步骤1：将n转为k进制，得到各位数字（从低位到高位）
    digits = []
    while n > 0:
        digits.append(n % k)
        n = n // k
    
    # 步骤2：按高位到低位生成结果（digits是低位在前，所以反转）
    res = []
    for i in reversed(range(len(digits))):
        cnt = digits[i]
        if cnt > 0:
            res.extend([str(i+1)] * cnt)
    
    # 输出结果
    print(' '.join(res))




"""
V1 手搓版

"""


import sys
from collections import defaultdict

def get_input():
    lines = sys.stdin.read().split(' ')
    n, k = map(int, lines)
    return n, k

# 【思路核心错误】merge函数完全违背题目合并规则，逻辑全错
def merge(cache: list[list], k):
    """
    合并
    """
    # 【错误1】queue初始值[-1]完全无意义，后续idx=-1的判断逻辑混乱
    queue = [-1]

    while queue:
        # 【错误2】pop(0)是队列操作，但queue里只有无效的-1，根本处理不到实际的合并位置
        idx = queue.pop(0)

        # 【错误3】cache[idx]对应cache的倒数第|idx|个元素，但你不知道这个元素是否是刚加的1，且len判断逻辑错
        if len(cache[idx]) == k:
        
            # 【错误4】abs(idx) > len(cache) 这个条件永远不成立（idx是负数，abs(idx)是正数，len(cache)是当前子列表数，不可能大于）
            if abs(idx) > len(cache):
                cache.insert(0, [])

            # 【错误5】合并规则是：k个x→1个x+1（替换原来的k个），但你却把x+1加到前一个列表里，完全违背题目！
            curr_num = cache[idx][0] + 1
            cache[idx - 1].append(curr_num)
            cache[idx] = []

            # 【错误6】只加了idx-1到队列，但连锁合并需要持续检查前一个位置，队列处理逻辑无效
            queue.append(idx - 1)

    return cache 

def main():
    n, k = get_input()
    cache = [[]]

    # 【思路错误】循环n次加1，但merge函数没正确处理合并，等于白加
    for i in range(n):
        cache[-1].append(1)
        cache = merge(cache, k)

    results = []
    for lis in cache:
        results.extend(lis)

    # 【语法错误】results是整数列表，join只能接字符串，必须转成str，否则直接报错
    print(' '.join(results))
        


"""
所以这道题用堆栈解是不可能的，因为它有10^18次操作的可能性，必须使用数学解法
进制解法

"""


import sys

def main():
    n, k = map(int, sys.stdin.read().split())
    if n == 0:
        print(0)
        return
    
    # 步骤1：转k进制，得到「低位到高位」的 digits
    digits = []
    temp = n
    while temp > 0:
        digits.append(temp % k)
        temp = temp // k
    
    # 步骤2：反转成「高位到低位」（关键！之前的核心bug就在这）
    digits = digits[::-1]
    
    res = []
    # 步骤3：遍历每一位，计算对应幂次
    # 总位数是 len(digits)，最高位幂次是 len(digits)-1
    current_power = len(digits) - 1
    for d in digits:
        if d > 0:
            # 该位有d个 (power+1)，拼接d次
            res.append(str(current_power + 1) * d)
        current_power -= 1
    
    # 步骤4：输出拼接结果（注意：不要加空格！）
    print(''.join(res))

if __name__ == "__main__":
    main()


"""

V1 手搓，战损版
"""

import sys
from collections import defaultdict

def get_input():
    lines = sys.stdin.read().split(' ')
    n, k = map(int, lines)
    return n, k


def main():
    n, k = get_input()

    digits = []

    while n > k: # 这里注意条件，是n > 0,不然会有溢出的数，没有添加进来的

        digits.append(n % k)
        n = n // k
    
    # 得到了一整条序列
    res_str = ""
    for i in range(len(digits)):
        # 这里注意一个问题，他有一个转换的过程，本质上它的含义是幂次，所以有问题
        res_str = str(digits[i]) + res_str 

    print(res_str)
    
if __name__ == "__main__":
    main()


"""

V1 手搓，修复版
"""

import sys
from collections import defaultdict

def get_input():
    lines = sys.stdin.read().split()  # 去掉' '，自动过滤空字符
    n = int(lines[0])
    k = int(lines[1])
    return n, k


def main():
    n, k = get_input()
    digits = []
    temp = n  # 新增：用temp存n，避免修改原n（不影响，但更规范）
    while temp > 0:
        digits.append(temp % k)
        temp = temp // k
    
    res_str = ""
    # 修正错误1+2：遍历digits，计算正确的幂次和重复次数
    for i in range(len(digits)):
        cnt = digits[i]  # 重复次数（digits[i]）
        if cnt > 0:
            power = i  # 正确幂次：digits[i]对应2^i
            num = power + 1  # 要输出的数字（幂次+1）
            new_part = str(num) * cnt  # 重复cnt次，比如num=1,cnt=366→"111...1"
            res_str = new_part + res_str  # 高位在前拼接
    
    print(res_str)

if __name__ == "__main__":
    main()

    
"""
V2 手搓版
"""

# 这个题目我记得需要动用一些小乔四,因为k有10^5次操作,这个操作量相当大,所以不可能一蹴而就
import sys
def get_input():

    string = sys.stdin.read()
    n, k = map(int, string.split(' '))

    return n, k


def main():

    n, k = get_input()

    # 结果保存表，表的含义为，该位置的余数
    res = []

    # 处理第一次
    temp = n
    # 如果没有除尽
    while temp != 0:
        
        # 这样就会得到一张反转的表，k进制表
        res.append(temp % k)
        temp = temp // k

    # 十进制拼接
    res_string = ''

    # 注意，这里不再需要反转
    for index in range(len(res)):
        counts = res[index] # 重复的频次

        if counts > 0:
            # 问题来了，这个位置该如何计算，重复的次数
            # 我知道了，我被二进制误导了，这里实际上确实是重复的次数，二进制因为很特殊，只有一个位，所以被误导了
            # 实际上，13个1形成的digits = [4, 2]的5进制，允许22111这种东西，所以才会有它的这种实现过程
            item_string = str((index + 1)) * counts
            res_string = item_string + res_string

    print(res_string)
        

if __name__ == "__main__":
    main()

