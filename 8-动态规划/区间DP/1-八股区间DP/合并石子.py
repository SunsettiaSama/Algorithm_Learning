



def stone_merge_min_cost(stones):

    n = len(stones)
    if n == 0:
        return 0

    a = [0] + stones[:]

    pre = [0] * (n + 1)
    for i in range(1, n + 1):
        pre[i] = pre[i - 1] + a[i]

    INF = float('inf')
    dp = [[INF] * (n + 2) for _ in range(n + 2)]
    for i in range(1, n + 1):
        dp[i][i] = 0

    for length in range(2, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1

            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + (pre[j] - pre[i - 1])
                if cost < dp[i][j]:
                    dp[i][j] = cost

    return dp[1][n]


# ===============================================



def stone_merge_min_cost(stones):

    n = len(stones)
    if n == 0:
        return 0

    # 区间dp，合并区间的代价
    # 状态定义，dp[i][j] = min(dp[i][k] + dp[k + 1][j] + sum(i, j))

    # 先算一个前缀和
    # 转化成1-base索引
    a = [0] + stones

    pre = [0] * (n + 1)
    for i in range(1, n + 1):
        pre[i] += pre[i - 1] + a[i]

    # 初始化dp表格，dp为最小代价，那么初始化就应该是INF
    INF = float('inf')
    dp = [[INF] * (n + 2) for _ in range(n + 2)] # 这里为什么是 n + 2 ？
    for i in range(n + 2): dp[i][i] = 0 # 对角线，区间长度为0时不用进行分割，无分割代价

    # 这里有一个严格的顺序
    # 先长度、再左区间、再右区间，原因见下

    # 计算dp值时，依赖 dp[i][k] 和 dp[k + 1][j]，这两个值必须提前订好；
    # 那么求任意dp[i][j]，就严格要求区间 [i, j] 内部所有值已经确定
    # 因此，若长度在外侧，那么每一轮的值就已经确定，全部填充完毕
    # 否则，长度在内侧时，会出现没算完的情况，比如划分左顶点i后，对length遍历，那么拿到的新结果中，j值有算了的，有没算的，结果就炸了

    for length in range(2, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1

            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + (pre[j] - pre[i - 1])
                if cost < dp[i][j]:
                    dp[i][j] = cost

    return dp[1][n]


# ====================================================

def stone_merge_min_cost(stones):


    n = len(stones)
    if n == 0:
        return 0

    a = [0] + stones
    pre = [0] * (n + 1) # 前缀和，1-base
    for i in range(1, n + 1): # p3
        pre[i] = pre[i - 1] + a[i] # p1

    # dp初始化
    # dp[i][j]被定义为区间i、j内的求解最小值
    INF = float('inf')
    dp = [[INF] * (n + 2) for j in range(n + 2)]

    # 对角线为0
    for i in range(n + 2):
        dp[i][i] = 0


    for length in range(2, n + 1):
        for i in range(1, n - length + 2): # p2
            j = i + length - 1 # 闭区间

            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + pre[j] - pre[i - 1] # 前缀和快速计算区间和
                if cost < dp[i][j]: # 寻找每一个可能的最优值
                    dp[i][j] = cost

    return dp[1][n]


# ---------- 测试 ----------
if __name__ == "__main__":
    # 4堆石子，重量分别为 4, 2, 3, 1
    stones = [4, 2, 3, 1]
    result = stone_merge_min_cost(stones)
    print(f"最小合并代价为: {result}")  # 输出: 20

    # 再测一个简单例子 [1, 2, 3]
    # 最优策略：先合并 1+2=3 (代价3)，再合并 3+3=6 (代价6)，总代价 9
    print(f"[1,2,3] 的最小合并代价: {stone_merge_min_cost([1, 2, 3])}")  # 输出: 9
