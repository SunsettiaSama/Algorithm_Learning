


# 冒泡排序函数：把列表里的数从小到大排
def bubble_sort(num_list):
    # 先看有多少个数（比如3个数，循环2趟就够）
    n = len(num_list)
    # 外层循环：控制要排几趟（n个数排n-1趟）
    for i in range(n-1):
        # 内层循环：每一趟从头比到“还没排好的位置”
        for j in range(n-1 - i):
            # 如果前一个数比后一个大，就换位置
            if num_list[j] > num_list[j+1]:
                num_list[j], num_list[j+1] = num_list[j+1], num_list[j]

# 试一下：排[3,1,2]
nums = [3,1,2]
bubble_sort(nums)
print(nums)  # 输出 [1,2,3]