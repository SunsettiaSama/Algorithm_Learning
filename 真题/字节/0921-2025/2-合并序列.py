

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

