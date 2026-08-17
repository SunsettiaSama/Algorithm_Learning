import sys 
import numpy as np


def get_data():

    all_nums = sys.stdin.read().split()
    ptr = 0


    d_in, d_hidden, d_out = int(all_nums[ptr + 0]), int(all_nums[ptr + 1]), int(all_nums[ptr + 2])
    ptr += 3

    W1 = np.array([[float(all_nums[ptr + i + d_in * j]) for i in range(d_in)] for j in range(d_hidden)], dtype = float)
    ptr += d_hidden * d_in

    b1 = np.array([float(all_nums[ptr + i]) for i in range(d_hidden)], dtype = float)
    ptr += d_hidden

    # 问题一，维度绑定问题
    W2 = np.array([[float(all_nums[ptr + i + d_hidden * j]) for i in range(d_hidden)] for j in range(d_out)], dtype = float)
    ptr += d_hidden * d_out

    b2 = np.array([float(all_nums[ptr + i]) for i in range(d_out)], dtype = float)
    ptr += d_out

    x = np.array([float(all_nums[ptr + i]) for i in range(d_in)], dtype = float)
    ptr += d_in

    y = np.array([float(all_nums[ptr + i]) for i in range(d_out)], dtype = float)
    ptr += d_out

    zeta = float(all_nums[ptr])
    ptr += 1

    return d_in, d_hidden, d_out, W1, b1, W2, b2, x, y, zeta

# 问题二，relu写法问题
def relu(z):
    return np.maximum(z, 0)   # 或 z * (z >= 0)

# 问题三，导数写法问题
def relu_(z):
    return np.array(np.where(z >= 0, 1.0, 0.0), dtype = float)

# 问题四，print函数问题
def print_array(arr):
    """
    按数组原始形状打印，每个元素保留六位小数。
    同一行用空格分隔，不同行换行，高维矩阵之间加空行。
    """
    def _print(a):
        if a.ndim == 1:
            # 最后一维：一行内元素用空格连接
            print(' '.join(f'{x:.6f}' for x in a))
        else:
            for i, sub in enumerate(a):
                _print(sub)                 # 递归打印子数组
                # 当前维度不是最后一维（a.ndim>2）且不是最后一个子数组时，加空行分隔
                if a.ndim > 2 and i != len(a) - 1:
                    print()
    _print(arr)


def solve():
    d_in, d_hidden, d_out, W1, b1, W2, b2, x, y, zeta = get_data()

    z1 = W1 @ x + b1
    a1 = relu(z1)

    # 问题五，这里不用写维度
    z2 = W2 @ a1 + b2
    y_pred = z2 # size: (d_out, )


    # 问题六，更新次序问题
    delta2 = y_pred - y
    delta1 = (W2.T @ delta2) * relu_(z1)

    W1 = W1 - zeta * np.outer(delta1, x)
    b1 = b1 - zeta * delta1

    W2 = W2 - zeta * np.outer(delta2, a1)
    b2 = b2 - zeta * delta2

    np.set_printoptions(precision=6, suppress=True)

    print_array(W1)
    print_array(b1)
    print_array(W2)
    print_array(b2)
    print_array(y_pred)

if __name__ == "__main__":
    solve()




# =======================================






# 三层全连接网络
import sys
import numpy as np


def get_data():

    all_nums = sys.stdin.read().split()
    ptr = 0

    d_in, d_hidden, d_out = int(all_nums[ptr]), int(all_nums[ptr + 1]), int(all_nums[ptr + 2])
    ptr += 3

    W1 = np.array([[all_nums[ptr + i + j * d_in] 
                    for i in range(d_in)] for j in range(d_hidden)], dtype = float)
    ptr += d_in * d_hidden

    b1 = np.array([all_nums[ptr + i] 
                    for i in range(d_hidden)], dtype = float)
    ptr += d_hidden

    W2 = np.array([[all_nums[ptr + i + j * d_hidden] 
                    for i in range(d_hidden)] for j in range(d_out)], dtype = float)
    ptr += d_hidden * d_out

    b2 = np.array([all_nums[ptr + i] 
                    for i in range(d_out)], dtype = float)
    ptr += d_out

    x = np.array([all_nums[ptr + i] 
                    for i in range(d_in)], dtype = float)
    ptr += d_in

    y = np.array([all_nums[ptr + i] 
                    for i in range(d_out)], dtype = float)
    ptr += d_out

    zeta = float(all_nums[ptr])

    # 捕获正确
    return d_in, d_hidden, d_out, W1, b1, W2, b2, x, y, zeta

def relu(x):
    return np.maximum(x, 0)

def d_relu(x: np.array):
    return np.array(x > 0, dtype = float)

def print_array(arr: np.array):

    def print_(sub_a: np.array):
        # 递归打印
        if sub_a.ndim == 1:
            # 维度仅剩1，则直接打印就好了
            print(' '.join(f'{v:.6f}' for v in arr))
        else:
            # 一般维度，维度还剩很多
            for row in arr:
                print_array(row)

    print_(arr)

def solve():

    d_in, d_hidden, d_out, W1, b1, W2, b2, x, y, zeta = get_data()

    # 第一轮前向
    z1 = W1 @ x + b1
    a1 = relu(z1)
    y_pred = W2 @ a1 + b2

    # 均方根loss
    # 直接算残差
    delta2 = y_pred - y
    # 这里注意是矩阵乘法，不是逐元素相乘
    # 题意中量张量贴在一起，就是默认矩阵乘法
    delta1 = (W2.T @ delta2) * d_relu(z1)

    d_W2 = np.outer(delta2, a1)
    d_b2 = delta2

    d_W1 = np.outer(delta1, x)
    d_b1 = delta1

    # W1有轻微的不同
    W1 = W1 - zeta * d_W1
    b1 = b1 - zeta * d_b1

    W2 = W2 - zeta * d_W2
    b2 = b2 - zeta * d_b2

    print_array(W1)
    print_array(b1)
    print_array(W2)
    print_array(b2)
    print_array(y_pred)



    return 


if __name__ == "__main__":
    solve()
