

import sys


# 计算最少需要多少个学期
def min_semesters(n, parent):
    # memo[i] 表示课程 i 的深度（也就是最早可安排的学期）
    memo = [0] * (n + 1)

    # 记忆化递归计算课程 x 的深度
    def get_depth(x):
        # 如果已经计算过，直接返回
        if memo[x] != 0:
            return memo[x]

        # 没有先修课，深度为 1
        if parent[x] == -1:
            memo[x] = 1
        else:
            # 否则深度等于直接先修课深度 + 1
            memo[x] = get_depth(parent[x]) + 1
        return memo[x]

    ans = 0
    for i in range(1, n + 1):
        ans = max(ans, get_depth(i))
    return ans


def main():
    input = sys.stdin.readline
    n = int(input().strip())

    # parent[i] 表示课程 i 的直接先修课
    parent = [0] * (n + 1)
    for i in range(1, n + 1):
        parent[i] = int(input().strip())

    print(min_semesters(n, parent))




"""
V1手搓


总的来说,这个题目可以用树来解决,但是走了弯路,最好用链表来做

"""

# 计算最少需要多少个学期
def min_semesters(n, parent):
    # memo[i] 表示课程 i 的深度（也就是最早可安排的学期）
    memo = [0] * (n + 1)

    def get_depth(x):
        if memo[x] != 0:
            return memo[x]
        
        if parent[x] == -1:
            memo[x] = 1

        else:
            memo[x] = get_depth(parent[x]) + 1
        
        return memo[x]
    
    ans = 0
    for i in range(1, n + 1):
        ans = max(ans, get_depth(i))

    return ans


def main():
    input = sys.stdin.readline
    n = int(input().strip())

    # parent[i] 表示课程 i 的直接先修课
    parent = [0] * (n + 1)
    for i in range(1, n + 1):
        parent[i] = int(input().strip())

    print(min_semesters(n, parent))









if __name__ == "__main__":
    main()


