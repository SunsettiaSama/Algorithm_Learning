


def max_safe_consecutive_points(initial_weight, max_safe_weight, weights):
    # cur 表示当前途经点处理后的实际载重
    cur = initial_weight
    # cnt 表示当前连续安全途经点数量
    cnt = 0
    # ans 表示最大连续安全途经点数量
    ans = 0

    for change in weights:
        # 到达当前途经点后，更新载重
        cur = max(0,cur+change)

        # 如果当前载重不超过安全上限，则当前点安全
        if cur <= max_safe_weight:
            cnt += 1
            ans = max(ans, cnt)
        else:
            # 当前点不安全，连续计数中断
            cnt = 0

    # 如果没有任何安全途经点，返回 -1
    return -1 if ans == 0 else ans


def main():
    # 读取第一行：初始载重、最大安全载重、途经点数量
    initial_weight, max_safe_weight, n = map(int, input().split())
    # 读取第二行：每个途经点的载重变化
    weights = list(map(int, input().split()))

    print(max_safe_consecutive_points(initial_weight, max_safe_weight, weights))


if __name__ == "__main__":
    main()

"""
V1 手搓
第一遍手搓是在考场上哈哈哈

"""

def get_ans(initialWeight, maxSafeWeight, N, weight_arr):

    # 线性扫描 + 前缀和 + 状态转移
    curr_weight = initialWeight
    ans = 0
    curr_ans = 0

    for index in range(N): # 这里是左节点,只能判断前方的路径,不能判断后方的路径 . _ . _ . _ 只能判断右侧的,可以看出来吧

        if not curr_weight > maxSafeWeight:
            curr_ans += 1
            ans = max(ans, curr_ans)
        else:
            curr_ans = 0 # 清零
        
        # 离开这个点时，装载或者卸载
        curr_weight = max(0, curr_weight + weight_arr[index])
    
    return curr_ans

def main():
    # 读取第一行：初始载重、最大安全载重、途经点数量
    initial_weight, max_safe_weight, n = map(int, input().split())
    # 读取第二行：每个途经点的载重变化
    weights = list(map(int, input().split()))

    print(max_safe_consecutive_points(initial_weight, max_safe_weight, weights))


if __name__ == "__main__":
    main()


"""
V1 修复

"""

def get_ans(initialWeight, maxSafeWeight, N, weight_arr):

    # 线性扫描 + 前缀和 + 状态转移
    curr_weight = initialWeight
    ans = 0
    curr_ans = 0

    for index in range(N):

        # 离开这个点时，装载或者卸载
        curr_weight = max(0, curr_weight + weight_arr[index])

        if curr_weight <= maxSafeWeight:
            curr_ans += 1
            ans = max(ans, curr_ans)
        else:
            curr_ans = 0 # 清零

    return -1 if ans == 0 else ans

def main():
    # 读取第一行：初始载重、最大安全载重、途经点数量
    initial_weight, max_safe_weight, n = map(int, input().split())
    # 读取第二行：每个途经点的载重变化
    weights = list(map(int, input().split()))

    print(get_ans(initial_weight, max_safe_weight, weights))


if __name__ == "__main__":
    main()
