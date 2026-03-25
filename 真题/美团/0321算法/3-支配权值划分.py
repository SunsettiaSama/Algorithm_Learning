


import sys
import math

def main():

    all_input = sys.stdin.read().split()
    ptr = 0

    T = int(all_input)
    ptr += 1

    for i in range(T):
        n = int(all_input[ptr])
        ptr += 1

        # 然后获取数组
        a = list(map(int, all_input[ptr: ptr + n]))
        ptr += n

        a = [0] + a

        # cost[l][r]: 子数组[l, ..., r]的权值，这是一个固定的，预处理得到的值
        cost = [[0 for i in range(n + 1) for j in range(n + 1)]]
        # 计算这个cost表
        for l in range(1, n + 1):
            cnt = dict()
            max_cnt = 0
            v = -math.inf
            for r in range(l, n + 1):
                num = a[r]
                cnt[num] =  cnt.get(num, 0) + 1
                if cnt[num] > max_cnt:
                    max_cnt = cnt[num]
                    v = num
                elif cnt[num] > max_cnt:
                    if num > v:
                        v = num
                # 计算当前区间权值
                cost[l][r] = v * (r - l + 1)

        dp = [math.inf for i in range(n + 1)]
        dp[0] = 0

        for i in range(1, n + 1):
            for j in range(0, i):
                # 相当于切蛋糕，最后一刀要切到哪里比较合适
                # 但因为之前已经完全算好了子数组的权值，所以直接用，哦！
                dp[i] = min(dp[i], dp[j] + cost[j + 1][i])
        
        print(dp[n])


if __name__ == "__main__":
    main()


"""
V0手搓版本

"""


import sys
import math

def main():

    all_input = sys.stdin.read().split()
    ptr = 0

    T = int(all_input)
    ptr += 1

    for i in range(T):
        n = int(all_input[ptr])
        ptr += 1

        # 然后获取数组
        a = list(map(int, all_input[ptr: ptr + n]))
        ptr += n

        a = [0] + a
        cost = [[0 for i in range(n + 1)] for j in range(n + 1)]
        # 算子数组权重表
        # 支配权值的计算逻辑就放在这里
        for slow in range(n + 1):
            # 利用哈希表保存
            cnt = dict()
            max_cnt = 0
            v = -math.inf

            for fast in range(slow, n + 1):

                num = a[fast]

                cnt[num] = cnt.get(num, 0) + 1
                if cnt[num] > max_cnt:
                    max_cnt = cnt[num]
                    v = num
                elif cnt[num] == max_cnt:
                    if num > v:
                        v = num
                
                cost[slow][fast] = v * (fast - slow + 1)

        dp = [0 for i in range(n + 1)]
        for i in range(1, n + 1):
            for j in range(0, i):
                dp[i] = min(dp[i], dp[j] + cost[j + 1][i])

    print(dp[n])




if __name__ == "__main__":
    main()
    