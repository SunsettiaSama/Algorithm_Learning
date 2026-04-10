


import numpy as np
import json
import sys



def parse_lstm_input(json_str):
    data = json.loads(json_str)

    Wx = np.array(data["Wx"], dtype = np.float64)
    Wh = np.array(data["Wh"], dtype = np.float64)
    b = np.array(data["b"], dtype = np.float64)
    h0 = np.array(data["h0"], dtype = np.float64)
    c0 = np.array(data["c0"], dtype = np.float64)
    X = np.array(data["X"], dtype = np.float64)

    d = Wx.shape[0]
    h = h0.shape[0]
    T = X.shape[0]

    Wxf, Wxi, Wxc, Wxo = np.hsplit(Wx, 4)
    Whf, Whi, Whc, Who = np.hsplit(Wh, 4)
    bf, bi, bc, bo = np.split(b, 4)

    return Wxf, Wxi, Wxc, Wxo, Whf, Whi, Whc, Who, bf, bi, bc, bo, h0, c0, X

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def lstm_forward(Wxf, Wxi, Wxc, Wxo, Whf, Whi, Whc, Who, bf, bi, bc, bo, h0, c0, X):

    h_prev = h0.copy()
    c_prev = c0.copy()

    for x_t in X:

        f_t = sigmoid(x_t @ Wxf + h_prev @ Whf + bf)

        i_t = sigmoid(x_t @ Wxi + h_prev @ Whi + bi)

        c_tilde = np.tanh(x_t @ Wxc + h_prev @ Whc + bc)
        C_t = f_t * c_prev + i_t + c_tilde

        o_t = sigmoid(x_t @ Wxo + h_prev @ Who + bo)
        h_t = o_t + np.tanh(C_t)

    return np.round(h_prev, 6)


if __name__ == "__main__":
    # 一次性读取输入流
    json_str = sys.stdin.read().strip()
    # 解析参数
    params = parse_lstm_input(json_str)
    # 前向计算
    h_final = lstm_forward(*params)
    # 输出结果（列表格式）
    print(h_final.tolist())