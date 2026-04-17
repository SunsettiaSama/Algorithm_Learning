def longest_wiggle_length(nums):
    # 计算最长摆动子序列长度
    up = 1
    down = 1

    for i in range(1, len(nums)):
        # 当前是上升，更新以上升结尾的最长长度
        if nums[i] > nums[i - 1]:
            up = down + 1
        # 当前是下降，更新以下降结尾的最长长度
        elif nums[i] < nums[i - 1]:
            down = up + 1

    return max(up, down)


def solve(nums):
    # 最少删除数量 = 原长度 - 最长摆动子序列长度
    return len(nums) - longest_wiggle_length(nums)


"""
小巧思
V0手搓版本——最长摆动数组

"""
import sys

def get_longest_wiggle_length(nums):
    # 错误1：初始值错误！单个数字本身就是长度为1的摆动序列
    # 正确：up = 1, down = 1（代表以上升/下降结尾的摆动序列长度）
    up = 0
    down = 0

    for i in range(1, len(nums)):
        if nums[i] > nums[i - 1]:
            # 错误2：核心逻辑错误！直接累加是统计【上升次数】，不是摆动序列长度
            # 正确：摆动必须交替上升下降 → up = down + 1（只能接在下降序列后）
            up += 1
        elif nums[i] < nums[i - 1]:
            # 错误3：核心逻辑错误！直接累加是统计【下降次数】，无视连续下降的规则
            # 正确：摆动必须交替上升下降 → down = up + 1（只能接在上升序列后）
            down += 1
    
    # 错误4：返回值错误！这里返回的是涨跌次数的最大值，不是最长摆动序列长度
    return max(up, down)

def get_input(input_string = None):
    # 此函数功能无错误，但代码冗余（官方直接input()更简洁），不影响结果
    if not input_string:
        strings = sys.stdin.read()
    else:
        strings = input_string

    ptr = 0
    strings = strings.strip().split()
    n = int(strings[ptr])
    ptr += 1

    nums = list(map(int, strings[ptr: ]))
    return n, nums


def main(input_string = None):
    n, nums = get_input(input_string)
    # 错误根源：调用了错误的摆动长度计算函数，导致最终结果错误
    return len(nums) - get_longest_wiggle_length(nums)


if __name__ == "__main__":
    print(main(
"""
7
1 3 1 4 5 2 0
"""
    ))