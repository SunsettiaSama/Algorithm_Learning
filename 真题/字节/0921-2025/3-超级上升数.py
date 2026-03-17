


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
# 虽然有10^18次方个数，但实际上，这个题目其实是字符串的排列组合，问不大于该数的前提下，有多少种排列组合的做法
# 比如给一个数字18，那么要从0~9中间，抽取两个数，然后判断是否有超级上升数
# 不行，11：54 0317 换个其他的思路来做吧，这个先留着





