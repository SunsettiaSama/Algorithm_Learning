
"""
V0 大失败

"""

import sys
import numpy as np

def get_input():

    lines = sys.stdin.read().split("\n")
    m = int(lines[0])

    N = int(lines[1])

    alpha = float(lines[2])
    ptr = 3

    samples = []
    while ptr < len(lines) and len(samples) < m:
        line = lines[ptr].strip()
        ptr += 1
        if not line:
            continue

        sample = list(map(int, lines[ptr].split(' ')))
        samples.append(sample)

    return m, N, alpha, samples

def calculate_loss(y_pred, y_true):
    return 1 / 2 / len(y_pred) * np.sum(np.power(y_pred - y_true, 2))


def main():

    # 逐步操作
    m, N, alpha, samples = get_input()

    
    data = np.array(samples, dtype = np.float64)
    
    X = data[:, : 3]
    Y = data[:, 3]

    # 归一化
    min_x = np.min(X, axis = 0)
    max_x = np.min(X, axis = 0)
    X_norm = np.zeros_like(X)

    for j in range(3):
        if max_x[j] != min_x[j]:
            X_norm[:, j] = (X[:, j] - min_x[j]) / (max_x[j] - min_x[j])
        else:
            X_norm[:, j] = 0.0

    X_norm_aug = np.hstack([np.ones((m, 1)), X_norm])

    
    W = np.array([0 for i in range(4)])





"""
V0 没想明白，需要复习，今晚

"""

import sys
import numpy as np

def get_input():

    lines = sys.stdin.read().split("\n")
    m = int(lines[0])

    N = int(lines[1])

    alpha = float(lines[2])
    ptr = 3

    samples = []
    while ptr < len(lines) and len(samples) < m:
        line = lines[ptr].strip()
        ptr += 1
        if not line:
            continue

        sample = list(map(int, lines[ptr].split(' ')))
        samples.append(sample)

    return m, N, alpha, samples

def main():

    m, N, alpha, datas = get_input()

    X = np.array(datas[:, :3], dtype = np.float64)
    Y = np.array(datas[:, 3], dtype = np.float64)
    # 真实标签
    y_true = Y

    # 归一化
    x_max = np.max(X, axis = 0)
    x_min = np.min(X, axis = 0)
    X_norm = np.zeros_like(X)
    for i in range(len(X[:, 0])):
        if x_max != x_min:
            X_norm[:, i] = (X[i, :] - x_min) / (x_max - x_min)
        else:
            X_norm[:, i] = 0 # 
    
    X_norm_aug = np.hstack((np.array([0 for i in range(len(X[:, 0]))]), X))

    # 初始化
    W_norm = np.array([0 for i in range(4)], dtype = np.float64)
    # 训练，矩阵乘法，这里是特征列
    for epoch in range(N):
        y_pred = W_norm @ X_norm
        err = y_pred - y_true
        # 需求数学推导
        gradient  = (1.0 / m) * X_norm_aug.T @ err

        W_norm -= alpha * gradient
    
    # 得到了W，对W进行缩放
    W = np.zeros(4, dtype = np.float64)
    for j in range(1, 4):
        feature_idx = j - 1
        denom = x_max[feature_idx] - x_min[feature_idx]
        if denom != 0:
            W[j] = W_norm[j] / denom
        else:
            W[j] = 0.0

    # sum_term = 0.0
    # for j in range(1, 4):
    #     feature_idx = j - 1
    #     sum_term += w[j] * min_x[feature_idx]
    # w[0] = w_norm[0] - sum_term



"""
V0 手搓

"""

def get_input():

    data = sys.stdin.read().strip().split()
    ptr = 0

    sample_nums = int(data[ptr])
    ptr += 1

    total_epochs = int(data[ptr])
    ptr += 1

    lr = float(data[ptr])
    ptr += 1

    samples = []
    for i in range(sample_nums):
        arr = [int(data[ptr]), int(data[ptr + 1]), int(data[ptr + 2]), int(data[ptr + 3])]
        ptr += 4
        samples.append(arr)
    
    samples = np.array(samples, dtype = np.float64)

    return sample_nums, total_epochs, lr, samples

def init_model(poly_nums):
    return np.array([0 for i in range(poly_nums)], dtype = np.float64)


def forward(samples, W):

    # 真实标签
    y_real = samples[:, 3]

    # 预测标签
    y_pred = W @ samples[:, :3]

    return y_real, y_pred

def backward(X, y_real: np.array, y_pred: np.array, W, lr):

    sample_nums = X.shape[0]

    err = y_real - y_pred

    # 2. 计算梯度
    # 公式: (1/m) * X.T * error
    # 如果损失函数定义为 1/2m * MSE，则系数 2 省略
    gradient = (1 / sample_nums) * X.T @ err

    W_new = W - lr * gradient

    return W_new

def norm(X):
    return (X - np.min(X, axis = 0)) / (np.max(X, axis = 0) - np.min(X, axis = 0))

def main():
    
    sample_nums, total_epochs, lr, samples = get_input()
    poly_nums = 4

    X = samples[:, :3]
    y_real = "没想明白"
    # 做归一化
    X_norm = norm(X)
    
    W = init_model(poly_nums)

    # 其实这就是一个简单的线性层
    for epoch in total_epochs:

        # 前向传播
        y_real, y_pred = forward(X_norm, W)

        W = backward(X, y_real, y_pred, W, lr)


"""
V0 修复学习

"""

def preprocess_data(samples):
    """
    params: 
        samples (m, 4) 的 numpy 数组，前3列是特征，第4列是标签
    output: 
        X_final (m, 4) 归一化后的特征矩阵（第1列是偏置1，后3列是特征），
        y (m,) 标签向量， 
        x_min (3,) 和 x_range (3,) 用于后续还原
    """
    
    # --- 1. 数据切片 ---
    # X_raw: (m, 3) -> 取出前3列特征
    X_raw = samples[:, :3] 
    
    # y: (m,) -> 取出最后一列标签 (虽然你原代码没返回y，但训练肯定需要)
    y = samples[:, 3]

    # --- 2. 统计极值 ---
    # x_min: (3,) -> 每一列的最小值
    # x_max: (3,) -> 每一列的最大值
    x_min, x_max = np.min(X_raw, axis=0), np.max(X_raw, axis=0)
    
    # x_range: (3,) -> 每一列的范围 (用于还原公式的分母)
    x_range = x_max - x_min 

    # --- 3. 归一化计算 (这里有 Bug) ---
    # X_norm: (m, 3) -> 初始化空矩阵
    X_norm = np.zeros_like(X_raw, dtype=np.float64)
    
    for i in range(X_raw.shape[1]): # 循环 3 次 (i=0, 1, 2)
        if x_range[i] != 0:
            # ❌ 原代码错误：你写了 (X_norm[:, i] - x_min[i])
            # 此时 X_norm 刚初始化全是 0，用 0 减去最小值，逻辑全错了！
            # ✅ 修正：应该用原始数据 X_raw 减去最小值
            X_norm[:, i] = (X_raw[:, i] - x_min[i]) / x_range[i]
        else:
            X_norm[:, i] = 0.0

    # --- 4. 拼接偏置列 ---
    # np.ones(...): (m, 1) -> 创建全 1 列向量
    # np.hstack: 水平拼接
    # X_final: (m, 4) -> 结构变为 [1, x1_norm, x2_norm, x3_norm]
    # 注意：hstack 接收的是一个元组，所以要加括号 ((..., ...))
    X_final = np.hstack((np.ones((X_raw.shape[0], 1)), X_norm))

    return X_final, y, x_min, x_range


def forward(X, W):
    return X @ W

def backward(X, y_real, y_pred, W, lr):
    """
    输入: X (m, 4), y_real (m,), y_pred (m,), W (4,), lr (float)
    输出: W_new (4,) 更新后的权重
    """
    m = X.shape[0]
    err = y_pred - y_real  # (m,) 注意：题目公式是 pred - true
    
    # 向量化梯度计算: (1/m) * X.T @ err
    # X.T 是 (4, m), err 是 (m,) -> 结果是 (4,)
    gradient = (1.0 / m) * (X.T @ err)
    
    W_new = W - lr * gradient
    return W_new

def restore_weights(W_norm, x_min, x_range):
    """
    输入: W_norm (4,) 训练好的归一化权重, x_min (3,), x_range (3,)
    输出: W_real (4,) 还原后的原始权重
    """
    W_real = np.zeros(4, dtype=np.float64)
    
    # 1. 还原特征权重 w1, w2, w3
    for j in range(3):
        if x_range[j] != 0:
            W_real[j+1] = W_norm[j+1] / x_range[j]
        else:
            W_real[j+1] = 0.0
            
    # 2. 还原偏置权重 w0
    # w0 = w0_norm - sum(w_real_j * min_j)
    bias_correction = np.sum(W_real[1:] * x_min)
    W_real[0] = W_norm[0] - bias_correction
    
    return W_real







