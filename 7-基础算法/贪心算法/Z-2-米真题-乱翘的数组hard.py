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


if __name__ == "__main__":
    n = int(input().strip())
    nums = list(map(int, input().split()))
    print(solve(nums))


"""
小巧思
V0手搓版本——最长摆动数组

"""