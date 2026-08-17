import sys
import heapq

def max_match(n, m, intervals, slots):
    """
    计算最多可以匹配的内容数量
    :param n: 内容条数
    :param m: 推荐位数
    :param intervals: 列表，每个元素为 (l_i, r_i)
    :param slots: 列表，每个元素为 s_j
    :return: 最大匹配数
    """
    # 1. 排序
    intervals.sort(key=lambda x: x[0])   # 按左端点升序
    slots.sort()                         # 推荐位热度升序

    # 2. 贪心匹配
    pq = []          # 最小堆，存储当前可用的区间的右端点
    idx = 0          # intervals 的指针
    matched = 0

    for s in slots:
        # 将所有左端点 <= s 的区间加入堆
        while idx < n and intervals[idx][0] <= s:
            heapq.heappush(pq, intervals[idx][1])
            idx += 1

        # 移除所有右端点 < s 的区间（无法匹配当前及后续更大的 s）
        while pq and pq[0] < s:
            heapq.heappop(pq)

        # 如果还有可用区间，选右端点最小的一个匹配当前推荐位
        if pq:
            heapq.heappop(pq)
            matched += 1

    return matched


def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    T = int(next(it))
    out_lines = []

    for _ in range(T):
        n = int(next(it))
        m = int(next(it))
        intervals = []
        for _ in range(n):
            l = int(next(it))
            r = int(next(it))
            intervals.append((l, r))
        slots = [int(next(it)) for _ in range(m)]

        result = max_match(n, m, intervals, slots)
        out_lines.append(str(result))

    sys.stdout.write("\n".join(out_lines))


if __name__ == "__main__":
    solve()



import sys
import heapq

def max_match(n, m, intervals, slots):

    intervals.sort(key = lambda x: x[0])
    slots.sort()

    pq = []
    idx = 0
    matched = 0

    for s in slots:
        # 将所有左端点 <= s 的区间加入堆
        while idx < n and intervals[idx][0] <= s:
            heapq.heappush(pq, intervals[idx][1])
            idx += 1
        
        while pq and pq[0] < s:
            heapq.heappop(pq)
        
        if pq:
            heapq.heappop(pq)
            matched += 1
    
    return matched

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    T = int(next(it))
    out_lines = []

    for _ in range(T):
        n = int(next(it))
        m = int(next(it))
        intervals = []
        for _ in range(n):
            l = int(next(it))
            r = int(next(it))
            intervals.append((l, r))
        slots = [int(next(it)) for _ in range(m)]

        result = max_match(n, m, intervals, slots)
        out_lines.append(str(result))

    sys.stdout.write("\n".join(out_lines))


if __name__ == "__main__":
    solve()




def max_match(n, m, intervals, slots):

    slots.sort()
    intervals.sort(key = lambda interval: interval[0])

    # 最小堆，仅维护右端点
    pq =[]
    idx = 0
    matched = 0

    for s in slots:

        # 搜索一段区间，找到intervals中符合要求的左端点
        # 此时压入右端点
        # idx的目的是仅迭代一遍，找到所有符合条件的区间
        while idx < n and intervals[idx][0] <= s:
            heapq.heappush(pq, item = intervals[idx][1])
            idx += 1
        
        # 清理掉超出界限的右端点
        while pq and s > pq[0]:
            heapq.heappop(pq)

        # 展开匹配，此时依旧存在合法值，则弹出堆顶
        if pq:
            heapq.heappop(pq)
            matched += 1
    
    return matched





def max_match(n, m, intervals, slots):

    intervals.sort(key = lambda x: x[0])
    slots.sort()

    pq = []
    idx = 0
    matched = 0

    for s in slots:

        while idx < n and intervals[idx][0] <= s:
            heapq.heappush(pq, item = intervals[idx][1])
            idx += 1
        
        # 清理掉不符合条件的区间
        while pq and s > pq[0]:
            heapq.heappop(pq)

        # 
        if pq:
            matched += 1
            heapq.heappop(pq)

    return matched
