

import sys

def get_input():

    lines = sys.stdin.read().strip().split('\n')
    ptr = 0

    m = int(lines[ptr])
    ptr += 1

    k = int(lines[ptr])
    ptr += 1

    n = int(lines[ptr])
    ptr += 1

    array = list(map(int, lines[ptr].split(' ')))
    ptr += 1

    return m, k, n, array

def main():

    m, k, n, prices = get_input()

    IMPOSSIBLE = -10**30

    # 股票模型
    dp0 = 0
    dp1 = IMPOSSIBLE

    for today_price in prices: # ERROR 时间错误,买入错误
        # 今天未持有
            # 1. 今天摆烂，也不持有
            # 2. 不摆烂，买入   # ERROR 这个状态一定是不能买入的，我们只能假定可以卖出之前的东西
                # 2. 昨天持有商品，今天卖掉，赚差价
        dp0_cache = max(
            dp0 + m, 
            dp1 + today_price - k
        )
        # 今天持有
            # 1. 昨天就持有
            # 2. 昨天空闲，今日买入
        dp1_cache = max(
            dp1, 
            dp0 - today_price - k
        )

        dp0, dp1 = dp0_cache, dp1_cache

    print(dp0)

if __name__ == "__main__":
    main()

