
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

    sum_term = 0.0
    for j in range(1, 4):
        feature_idx = j - 1
        sum_term += w[j] * min_x[feature_idx]
    w[0] = w_norm[0] - sum_term











