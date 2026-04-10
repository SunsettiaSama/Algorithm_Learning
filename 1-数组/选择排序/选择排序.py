# 912题：排序数组 - 选择排序实现
def sortArray(nums):
    n = len(nums)
    # 外层循环：控制“要摆的位置”（从0到n-2，最后一个位置不用摆）
    for i in range(n - 1):
        # 第一步：先假设当前位置i的数字是最小值（记下来位置）
        min_index = i
        # 内层循环：在i后面的数字里，找真正的最小值位置
        for j in range(i + 1, n):
            if nums[j] < nums[min_index]:
                min_index = j  # 找到更小的，更新最小值位置
        # 第二步：把最小值和位置i的数字交换（一次换到位）
        nums[i], nums[min_index] = nums[min_index], nums[i]
    return nums

# 测试912题例子：[5,2,3,1] → 输出[1,2,3,5]
if __name__ == "__main__":
    test_nums = [5,2,3,1]
    sorted_nums = sortArray(test_nums)
    print("排好的数组：", sorted_nums)  # 输出 [1,2,3,5] ✅