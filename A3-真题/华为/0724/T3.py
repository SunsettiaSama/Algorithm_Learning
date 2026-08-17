from collections import deque
import sys

def solve():
    input = sys.stdin.readline
    n, p, T = map(int, input().split())
    times = [0] + list(map(int, input().split()))   # 每层计算时间，1-based
    comms = list(map(int, input().split()))         # 相邻层通信开销，长度 n-1

    # ---------- 前缀和：快速求任意连续区间的总计算时间 ----------
    prefix_sum = [0] * (n + 1)
    for i in range(1, n + 1):
        prefix_sum[i] = prefix_sum[i-1] + times[i]

    # cut_cost[k]：若在第 k 层后切一刀（即划分点位于 k 与 k+1 之间），付出的通信开销
    # cut_cost[0] = 0（最左边无切分），cut_cost[i] = comms[i-1]（i 从1到 n-1）
    cut_cost = [0] * (n + 1)
    for i in range(1, n):
        cut_cost[i] = comms[i-1]

    INF = 10**18

    # prev_dp[k]：前一轮（分成 j-1 段）覆盖前 k 层的最小总开销
    # 初始状态：分成 0 段覆盖前 0 层，代价为 0
    prev_dp = [INF] * (n + 1)
    prev_dp[0] = 0

    # ---------- 主循环：j 从 1 到 p（逐步增加阶段数） ----------
    for stage_num in range(1, p + 1):
        cur_dp = [INF] * (n + 1)          # 本轮（分成 stage_num 段）的答案
        mono_queue = deque()              # 单调队列，存 (k, 候选代价)，候选代价=prev_dp[k]+cut_cost[k]
        left_boundary = 0                 # 最小合法 k（保证最后一段不超时）

        # 遍历前 i 层（i 从 1 到 n）
        for i in range(1, n + 1):
            # ---------- 步骤1：更新左边界，剔除超时的候选 k ----------
            # 最后一段为 [k+1, i]，其计算时间 = prefix_sum[i] - prefix_sum[k]
            # 必须 ≤ T，所以 k 必须 ≥ 能使不等式成立的“最小左边界”
            while prefix_sum[i] - prefix_sum[left_boundary] > T:
                left_boundary += 1

            # ---------- 步骤2：把新的候选 k = i-1 加入队列 ----------
            k = i - 1
            if prev_dp[k] < INF:
                
                # 候选代价 = 前 stage_num-1 段覆盖前 k 层的最小代价 + 在 k 处切一刀的通信费
                candidate_cost = prev_dp[k] + cut_cost[k]
                # 维护单调递增队列（队头永远是最小代价）
                while mono_queue and mono_queue[-1][1] >= candidate_cost:
                    mono_queue.pop()
                mono_queue.append((k, candidate_cost))

            # ---------- 步骤3：移除队列中所有 k < left_boundary 的过期候选 ----------
            while mono_queue and mono_queue[0][0] < left_boundary:
                mono_queue.popleft()

            # ---------- 步骤4：取队头即为 dp[stage_num][i] 的最优值 ----------
            if mono_queue:
                cur_dp[i] = mono_queue[0][1]

        # 本轮结束，滚动到下一轮
        prev_dp = cur_dp

    # ---------- 输出最终答案 ----------
    ans = prev_dp[n]
    print(-1 if ans >= INF else ans)


if __name__ == "__main__":
    solve()