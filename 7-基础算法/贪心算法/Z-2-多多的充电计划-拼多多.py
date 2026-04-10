# 题目功能函数：返回到达终点的最小充电费用
def solve(L, C, n, stations):
    # 拆分位置和价格，方便处理
    d = [0] * (n + 2)
    p = [0] * (n + 2)

    for i in range(1, n + 1):
        d[i], p[i] = stations[i - 1]

    # 加入终点这个虚拟站点，价格设为 0
    d[n + 1] = L
    p[n + 1] = 0

    # 先判断是否存在无法跨越的区间
    if n > 0 and d[1] > C:
        return -1
    for i in range(1, n + 2):
        if d[i] - d[i - 1] > C:
            return -1

    ans = 0
    battery = C   # 初始满电
    prev = 0      # 上一个位置，初始在起点

    # 依次处理每个真实充电站
    for i in range(1, n + 1):
        # 先从上一个位置开到当前站
        battery -= d[i] - prev
        prev = d[i]

        # 找续航范围内第一个比当前站更便宜的站
        j = i + 1
        while j <= n + 1 and d[j] - d[i] <= C:
            if p[j] < p[i]:
                break
            j += 1

        # 需要带着多少电离开当前站
        if j <= n + 1 and d[j] - d[i] <= C:
            # 有更便宜的站，只充到刚好能到那里
            need = d[j] - d[i]
        else:
            # 没有更便宜的站，直接充满
            need = C

        # 如果当前电量不足，则补足
        if battery < need:
            ans += (need - battery) * p[i]
            battery = need

    return ans



if __name__ == "__main__":
    # ACM 风格输入
    L, C, n = map(int, input().split())
    stations = []
    for _ in range(n):
        di, pi = map(int, input().split())
        stations.append((di, pi))

    print(solve(L, C, n, stations))


"""
V0修复版
"""

import sys
import math

# 1. 读取输入函数（无难点，纯读取数据）
def get_input():
    lines = sys.stdin.read().strip().split("\n")
    ptr = 0
    # 读取：总距离、满电续航、充电站数量
    TargetDistance, MaxBatteryVolumn, nums = list(map(int, lines[ptr].split()))
    ptr += 1

    ChargeStation = []
    # 读取每个充电站的（位置，电价）
    for n in range(nums):
        d, p = list(map(int, lines[ptr].split()))
        ChargeStation.append((d, p))
        ptr += 1
    # 🔥 关键：把终点当成虚拟充电站（电价0，不用充电）
    ChargeStation.append((TargetDistance, 0))

    return TargetDistance, MaxBatteryVolumn, ChargeStation, nums

def main():
    # 接收输入数据
    TargetDistance, MaxBatteryVolumn, ChargeStation, nums = get_input()

    # 2. 边界检查：判断是否能到达终点（任意一段超续航=无解）
    prev_distance = 0  # 初始位置=起点0
    for curr_distance, charge_fee in ChargeStation:
        # 相邻两个站点的距离 > 满电续航 → 到不了
        if curr_distance - prev_distance > MaxBatteryVolumn:
            return -1
        prev_distance = curr_distance  # 更新上一个站点位置

    # 3. 初始化核心状态（起点状态）
    curr_battery = MaxBatteryVolumn  # 起点满电
    total_cost = 0                   # 初始花费0
    curr_position = 0                # 初始位置=起点0

    # 4. 🔥 核心：贪心处理每一个充电站（最后一个是终点，不用处理）
    for idx in range(len(ChargeStation) - 1):
        # 当前要处理的充电站：位置、电价
        curr_station_dist, curr_station_price = ChargeStation[idx]

        # ---------------------
        # 步骤1：更新行驶状态（必做！）
        # ---------------------
        drive_distance = curr_station_dist - curr_position  # 计算：从上一个位置开到当前站的路程
        curr_battery -= drive_distance                     # 扣除电量：跑了多少路，耗多少电
        curr_position = curr_station_dist                  # 更新位置：车已经开到当前充电站了

        # ---------------------
        # 步骤2：贪心核心 → 找【续航范围内第一个更便宜的充电站】
        # ---------------------
        next_cheaper_idx = -1  # 初始值：没找到更便宜的站
        # 从当前站的下一个站开始向后遍历
        for j in range(idx + 1, len(ChargeStation)):
            next_station_dist, next_station_price = ChargeStation[j]
            # 条件1：超出当前站的满电续航 → 不用再往后找了，直接退出
            if next_station_dist - curr_station_dist > MaxBatteryVolumn:
                break
            # 条件2：找到第一个比当前站便宜的站 → 标记下标，立刻停止寻找
            if next_station_price < curr_station_price:
                next_cheaper_idx = j
                break

        # ---------------------
        # 步骤3：终极贪心决策 → 充多少电？（最关键！）
        # ---------------------
        # 情况A：找到了更便宜的站 → 只充到【刚好能开到那里】
        if next_cheaper_idx != -1:
            target_dist, _ = ChargeStation[next_cheaper_idx]  # 便宜站的位置
            need = target_dist - curr_position                  # 计算：开到便宜站需要跑多远
            charge = max(0, need - curr_battery)               # 计算：需要充多少电（剩余电不够才充）
            total_cost += charge * curr_station_price          # 累加花费：充电量 × 当前站电价
            curr_battery = curr_battery + charge - need       # 更新电量：充完电→开到便宜站，剩余电量

        # 情况B：没找到更便宜的站 → 当前站是附近最便宜的！直接充满电
        else:
            charge = MaxBatteryVolumn - curr_battery           # 计算：充满需要充多少电
            total_cost += charge * curr_station_price          # 累加花费
            curr_battery = MaxBatteryVolumn                    # 电量更新为满电

    # 所有充电站处理完毕，返回总花费
    return total_cost

# 运行代码
print(main())













