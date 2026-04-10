

"""
豆包版
"""


import sys
# 定义无穷小（表示状态不可达）
INF = -float('inf')

def calculate_prefix_max(arr):
    """
    计算数组的前缀最大值数组
    作用：快速查询 arr[0..v-1] 的最大值（用于上升状态转移）
    参数：arr - 输入数组（长度256）
    返回：prefix_max - prefix_max[v] = max(arr[0], arr[1], ..., arr[v])
    """
    prefix_max = [0] * 256
    # 初始化第一个位置
    prefix_max[0] = arr[0]
    # 从左到右遍历，逐个更新前缀最大值
    for v in range(1, 256):
        prefix_max[v] = max(prefix_max[v-1], arr[v])
    return prefix_max

def calculate_suffix_max(arr):
    """
    计算数组的后缀最大值数组
    作用：快速查询 arr[v+1..255] 的最大值（用于下降状态转移）
    参数：arr - 输入数组（长度256）
    返回：suffix_max - suffix_max[v] = max(arr[v], arr[v+1], ..., arr[255])
    """
    suffix_max = [0] * 256
    # 初始化最后一个位置
    suffix_max[255] = arr[255]
    # 从右到左遍历，逐个更新后缀最大值
    for v in range(254, -1, -1):
        suffix_max[v] = max(suffix_max[v+1], arr[v])
    return suffix_max

def main():
    # 读取输入（适配竞赛场景的快速输入）
    input_data = sys.stdin.read().split()
    ptr = 0  # 输入指针，用于逐个读取数据
    t = int(input_data[ptr])  # 测试用例数
    ptr += 1
    
    for _ in range(t):
        n = int(input_data[ptr])  # 数组长度
        ptr += 1
        a = list(map(int, input_data[ptr:ptr+n]))  # 原始数组
        ptr += n
        
        # ========== 核心状态初始化 ==========
        # s：前缀异或和（s[i] = a[0]^a[1]^...^a[i-1]，初始s=0对应空前缀）
        prefix_xor = 0
        # up[v]：以异或值v结尾，且最后一步是「上升」（前一个异或值 < v）时的最大段数
        up = [INF] * 256
        # down[v]：以异或值v结尾，且最后一步是「下降」（前一个异或值 > v）时的最大段数
        down = [INF] * 256
        # 初始状态：空前缀（异或值0），段数为0（既可以作为上升的起点，也可以作为下降的起点）
        up[0] = 0
        down[0] = 0
        
        # ========== 遍历数组，动态规划更新状态 ==========
        for num in a:
            # 1. 更新当前前缀异或和（对应前i个元素的异或值）
            prefix_xor ^= num
            current_xor = prefix_xor  # 当前异或值v
            
            # 2. 预处理前缀/后缀最大值（优化状态转移的效率）
            # 前缀最大值：down[0..v]的最大值（用于找「前一个异或值 < current_xor」的最大down值）
            prefix_max_down = calculate_prefix_max(down)
            # 后缀最大值：up[v..255]的最大值（用于找「前一个异或值 > current_xor」的最大up值）
            suffix_max_up = calculate_suffix_max(up)
            
            # 3. 计算「上升状态」的新值（new_up）
            # 上升规则：前一步必须是下降，且前一个异或值 < current_xor
            if current_xor > 0:
                # 找所有 < current_xor 的异或值中，down的最大值
                max_prev_down = prefix_max_down[current_xor - 1]
            else:
                # current_xor=0时，没有比它小的异或值，无法上升
                max_prev_down = INF
            # 若前序状态可达，则新段数=前序段数+1；否则初始化为1（单独一段）
            new_up = max_prev_down + 1 if max_prev_down != INF else 1
            
            # 4. 计算「下降状态」的新值（new_down）
            # 下降规则：前一步必须是上升，且前一个异或值 > current_xor
            if current_xor < 255:
                # 找所有 > current_xor 的异或值中，up的最大值
                max_prev_up = suffix_max_up[current_xor + 1]
            else:
                # current_xor=255时，没有比它大的异或值，无法下降
                max_prev_up = INF
            # 若前序状态可达，则新段数=前序段数+1；否则初始化为1（单独一段）
            new_down = max_prev_up + 1 if max_prev_up != INF else 1
            
            # 5. 更新当前异或值对应的状态（取最大值，保证段数最多）
            if new_up > up[current_xor]:
                up[current_xor] = new_up
            if new_down > down[current_xor]:
                down[current_xor] = new_down
        
        # ========== 计算最终结果 ==========
        # 所有异或值对应的up/down的最大值，就是最多能划分的段数
        max_up = max(up)
        max_down = max(down)
        result = max(max_up, max_down)
        print(result)

# 程序入口
if __name__ == '__main__':
    main()