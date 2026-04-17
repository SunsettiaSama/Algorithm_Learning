


# 这个题和当初找素数的题目有异曲同工之妙

# 但是素数有一个快速解法是筛

# 这个能快速解么
import sys

def get_input() -> list[int]:

    lines = sys.stdin.read().split('\n')
    array = map(int, lines)

    return array


# 记忆化搜索过程
memo = {}

def findSuperUpperNumber(num):

    count = 0

    # 如何判定十进制不再下降呢？转化成字符串即可
    def upper_condition(current_num):
        
        if current_num < 10:
            return True
        
        current_num_string = list(str(current_num)) # 笔误问题
        for index in range(1, len(current_num_string)):
            if current_num_string[index - 1] > current_num_string[index]:
                return False
            
        return True
    
    for current_num in range(num + 1): # 遍历范围错误
        if current_num in memo:
            count += memo[current_num]

        # 对于其中的任意值，判定自身是否为超级上升数
        if upper_condition(current_num) and upper_condition(current_num * current_num): # 条件判断问题
            # 若是，则记录自身 
            memo[current_num] = 1
            count += 1
        else:
            memo[current_num] = 0

    return count


def main():

    array = get_input()

    counts = []

    # 寻找超级上升数
    for num in array:
        counts.append(findSuperUpperNumber(num))
    

    print('\n'.join(counts))




"""
豆包神力,woc,我确实没想到可以这么解,我以为是素数那套做法,草

磨刀不误砍柴功啊，多看会题目，多审题，而且要记住这种变化，太妙了

"""
# 所以逻辑被改换成了
# 1. 通过二分查找+字符串的排列组合

import bisect

# ---------------------- 步骤1：预生成所有上升数（1~1e18） ----------------------
def generate_increasing_numbers():
    """
    用DFS生成所有十进制上升数（各位非递减，如112、123、555）
    上升数的生成逻辑：从高位到低位选数字，后一位≥前一位，避免重复
    """
    increasing_nums = []
    
    def dfs(current_num, last_digit):
        """
        递归生成上升数
        :param current_num: 当前拼接的数
        :param last_digit: 最后一位数字（保证下一位≥它）
        """
        # 终止条件：超过1e18则停止（题目m最大1e18）
        if current_num > 10**18:
            return
        # 非0的数才加入（题目讨论的是正整数）
        if current_num != 0:
            increasing_nums.append(current_num)
        # 遍历下一位数字：从last_digit到9（保证非递减）
        for d in range(last_digit, 10):
            next_num = current_num * 10 + d
            dfs(next_num, d)
    
    # 初始调用：从0开始，第一位可以选1~9（避免前导0）
    dfs(0, 1)
    return increasing_nums

# ---------------------- 步骤2：筛选超级上升数（自身+平方都是上升数） ----------------------
def is_increasing(n: int) -> bool:
    """判断一个数是否是上升数（各位非递减）"""
    s = list(str(n))
    for i in range(1, len(s)):
        if s[i] < s[i-1]:
            return False
    return True

def filter_super_increasing_numbers(increasing_nums: list) -> list:
    """筛选出超级上升数：自身是上升数，且平方也是上升数"""
    super_nums = []
    for num in increasing_nums:
        square = num * num
        if is_increasing(square):
            super_nums.append(num)
    # 排序（后续二分查询需要有序）
    super_nums.sort()
    return super_nums

# ---------------------- 步骤3：处理输入+查询 ----------------------
def get_input():
    """正确读取输入：第一行T，后续T行是m"""
    import sys
    # 读取所有输入，按行分割并过滤空行（避免换行符/空格干扰）
    lines = [line.strip() for line in sys.stdin.read().splitlines() if line.strip()]
    T = int(lines[0])  # 测试组数
    m_list = [int(line) for line in lines[1:T+1]]  # 每组的m
    return T, m_list

def main():
    # 预生成所有上升数（只做一次，全局复用）
    print("预生成上升数中...（仅首次执行）", file=sys.stderr)
    increasing_nums = generate_increasing_numbers()
    # 筛选超级上升数
    super_nums = filter_super_increasing_numbers(increasing_nums)
    print(f"预生成完成，超级上升数总数：{len(super_nums)}", file=sys.stderr)
    
    # 读取输入
    T, m_list = get_input()
    
    # 处理每个查询：二分查找≤m的超级上升数数量
    results = []
    for m in m_list:
        # bisect_right返回第一个>m的位置，即≤m的数量
        count = bisect.bisect_right(super_nums, m)
        results.append(str(count))
    
    # 输出结果（每行一个）
    print('\n'.join(results))

if __name__ == "__main__":
    main()


"""
V1 手搓
"""

from typing import List

# 我知道这个题怎么做了
def get_input():
    """正确读取输入：第一行T，后续T行是m"""
    import sys
    # 读取所有输入，按行分割并过滤空行（避免换行符/空格干扰）
    lines = [line.strip() for line in sys.stdin.read().splitlines() if line.strip()]
    T = int(lines[0])  # 测试组数
    m_list = [int(line) for line in lines[1:T+1]]  # 每组的m
    return T, m_list


def preloadUpperNums() -> List[int]:

    # 预先生成上升数，上升数数目极少，二分查找近似O(1)
    # 先用dfs来查找上升数

    upper_nums = []

    def dfs(curr_num, total_string: str):

        # 如果当前的选择比之前的更小，那么就可以弹出
        if len(total_string) == 18:
            upper_nums.append(int(total_string))
            return 
        
        # 不对，我是来做排列组合的
        # 对当前的情况进行处理：添加大于的数字
        total_string += str(curr_num)

        for candidate in range(curr_num, 10):
            # 这里导致candidate一定是单增加，不减的

            # 进行下一个数字的选择
            dfs(candidate, total_string = total_string)

            # 弹出该选择
            total_string = total_string[:-1]

        # 这样，就拿到了所有疑似上升数的数字
        # 顺带，它是有序的

    # 初始化，第一轮得我们自己做？
    for curr_num in range(1, 10):
        dfs(curr_num = curr_num, total_string = '')
    
    # 好，这样就找到了所有的上升数
    return upper_nums

def isSupperUpper(num):

    temp = str(num * num)

    # 超级上升数也不能大于10 ** 10
    if len(temp) > 10:
        return False
    
    for index in range(1, len(temp)):
        if not temp[index] > temp[index - 1]:
            return False
        
    return True

def SearchIndex(target, num_list):

    left = 0
    right = len(num_list) - 1

    while left <= right:
        mid = (left + right) // 2

        if target > num_list[mid]:
            left = mid + 1
        elif target < num_list[mid]:
            right = mid - 1
        else:
            return mid
        
    # 小于该mid的值
    return right

def main():

    T, m_list = get_input()

    upper_num_list = preloadUpperNums()
    super_upper_list = []

    results = []

    # 初始化超级上升数列表
    for num in upper_num_list:
        if isSupperUpper(num):
            super_upper_list.append(num)

    # 那么现在有了超级上升数列表，接下来进行二分查找
    for i in range(T):
        m = m_list[i]
        results.append(SearchIndex(m, num_list = super_upper_list))

    print(" ".join(map(str, results)))










"""
V2
再来一遍
"""
def generate_increasing_numbers():

    # 使用深搜，来获取超级上升数
    # 字符串操作
    # 递归加上记忆化，这里需要记忆

    # 递归记忆，也不一定非得用一张表来保存，直接使用记忆的即可
    increasing_nums = []
    def dfs(current_num, last_digit):

        if current_num > 1e18:   # [问题] 1e18 是浮点数，建议用 10**18 保持整数比较
            return 

        # 当前操作
        if current_num != 0:
            increasing_nums.append(current_num)

        for d_i in range(last_digit, 10):
            next_num = current_num * 10 + next_num   # [严重错误] next_num 变量未定义，应该是 current_num * 10 + d_i
            dfs(next_num, d_i)   # [问题] 递归调用后没有剪枝，但可以接受

    dfs(current_num = 0, last_digit = 1)   # [问题] 参数名写对了，但注意 current_num=0 会被过滤掉（正确）

    return increasing_nums


def is_super_increasing_numbers(increasing_num):

    res = increasing_num * increasing_num 
    res = str(res)

    prev_item = res[0]
    for item in res[1: ]:
        if not item > prev_item:   # [问题] 逻辑错误：应该是 item < prev_item 时返回 False
            return False
        
        prev_item = item
    
    return True

def filter_super_increasing_numbers(increasing_nums):

    super_increasing_numbers = []
    for increasing_num in increasing_nums:
        if is_super_increasing_numbers(increasing_num):
            super_increasing_numbers.append(increasing_num)
    
    return super_increasing_numbers # [警告] 这时返回的理论上有序，但可以进一步重排

import bisect

import bisect   # 别忘了导入

def search_target(target, super_increasing_numbers):
    """
    返回 super_increasing_numbers 中 ≤ target 的元素个数
    """
    # super_increasing_numbers 必须是有序列表（升序）
    # bisect_right 返回第一个 > target 的索引，该索引就是 ≤ target 的元素个数
    count = bisect.bisect_right(super_increasing_numbers, target)
    return count


def main():
    import sys
    target = int(sys.stdin.read().strip())   # [问题] 只读取了一个整数，但题目第一行是 T，后面有 T 个 m
    increasing_nums = generate_increasing_numbers()
    super_increasing_numbers = filter_super_increasing_numbers(increasing_nums)

    return search_target(target, super_increasing_numbers)   # [问题] 应该输出结果，而不是 return（而且 search_target 逻辑错误）








































if __name__ == "__main__":
    main()




