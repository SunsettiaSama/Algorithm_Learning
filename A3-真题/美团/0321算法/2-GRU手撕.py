import numpy as np
import json
import sys


def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def parse_gru_input(json_str):
    data = json.loads(json_str)

    Wx = np.array(data["Wx"], dtype = np.float64)
    Wh = np.array(data["Wh"], dtype = np.float64)
    b = np.array(data["b"], dtype = np.float64)
    h0 = np.array(data["h0"], dtype = np.float64)
    X = np.array(data["X"], dtype = np.float64)

    d = Wx.shape[0]
    h = h0.shape[0]
    T = X.shape[0]

    Wxr, Wxz, Wxh = np.hsplit(Wx, 3)
    Whr, Whz, Whh = np.hsplit(Wh, 3)
    br, bz, bh = np.split(b, 3)

    return Wxr, Wxz, Wxh, Whr, Whz, Whh, br, bz, bh, h0, X, d, h, T

def gru_forward(Wxr, Wxz, Wxh, Whr, Whz, Whh, br, bz, bh, h0, X, d, h, T):

    h_prev = h0.copy()
    T = X.shape[0]

    for t in range(T):
        x_t = X[t]

            
        rt = sigmoid(x_t @ Wxr + h_prev @ Whr + br)
        zt = sigmoid(x_t @ Wxz + h_prev @ Whz + bz)

        h_tilde = np.tanh(x_t @ Wxh + rt * h_prev @ Whh + bh)
        h_t = (1 - zt) * h_prev + zt * h_tilde

        h_prev = h_t

    return np.round(h_prev, 6)


def main():
    # 一次性读取标准输入（避免重复读流导致空字符串）
    json_str = sys.stdin.read().strip()
    # 解析参数
    params = parse_gru_input(json_str)
    # 执行前向传播
    h_T = gru_forward(*params)
    # 输出结果（转成列表，保留 6 位小数）
    print(h_T.tolist())

if __name__ == "__main__":
    main()

















