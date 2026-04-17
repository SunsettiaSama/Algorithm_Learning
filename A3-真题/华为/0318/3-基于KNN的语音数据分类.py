

import sys
from typing import List, Tuple

# ========== 模块1：数据读取 ==========
def read_input() -> Tuple[int, int, List[Tuple[Tuple[float, float, float], int]], Tuple[float, float, float]]:
    """
    从标准输入读取数据，解析为：
    N: 已知样本数量
    K: 邻居个数
    train_data: 列表，每个元素为 ((x1, x2, x3), label)
    test_sample: 待分类的三维向量 (x1, x2, x3)
    """
    data = sys.stdin.read().strip().split()
    if not data:
        return None
    it = iter(data)
    N = int(next(it))
    K = int(next(it))

    train_data = []
    for _ in range(N):
        x1 = float(next(it))
        x2 = float(next(it))
        x3 = float(next(it))
        label = int(next(it))
        train_data.append(((x1, x2, x3), label))

    test_sample = (float(next(it)), float(next(it)), float(next(it)))

    return N, K, train_data, test_sample

# ========== 模块2：距离计算 ==========
def euclidean_distance(vec1: Tuple[float, float, float],
                       vec2: Tuple[float, float, float]) -> float:
    """
    计算两个三维向量的欧氏距离
    公式：sqrt((x1-y1)^2 + (x2-y2)^2 + (x3-y3)^2)
    """
    return ((vec1[0] - vec2[0]) ** 2 +
            (vec1[1] - vec2[1]) ** 2 +
            (vec1[2] - vec2[2]) ** 2) ** 0.5

def knn_classify(train_data: List[Tuple[Tuple[float, float, float], int]], 
                 test_sample: Tuple[float, float, float], 
                 k: int):
    
    distances = []
    for features, label in train_data:
        dist = euclidean_distance(test_sample, features)
        distances.append((dist, label))
    
    distances.sort(key = lambda x: x[0])

    k_nearest_labels = [label for _, label in distances[:k]]

    label_count = {}
    for lbl in k_nearest_labels:
        label_count[lbl] = label_count.get(lbl, 0) + 1
    
    predicted_label = max(label_count.items(), key = lambda x: x[1])[0]

    return predicted_label

# ========== 模块4：主函数 ==========
def main() -> None:
    """读取输入，调用KNN分类，输出结果"""
    result = read_input()
    if result is None:
        return
    N, K, train_data, test_sample = result

    # 使用KNN进行分类
    predicted = knn_classify(train_data, test_sample, K)

    # 输出结果
    print(predicted)




"""
V0 手搓

"""
import sys
import numpy as np
from typing import Tuple, List  # !!! 缺少导入，会导致运行时 NameError

def get_input(all_data = None) -> Tuple[int, int, 
                         List[Tuple[Tuple[float, float, float], int]],
                         Tuple[float, float, float]]:
    
    if not all_data:
        all_data = sys.stdin.read()

    all_data = all_data.strip().split()

    ptr = 0

    N, K = int(all_data[ptr]), int(all_data[ptr + 1])
    ptr += 2

    datas = []
    for i in range(N):
        data = list(map(float, all_data[ptr: ptr + 3]))
        label = int(all_data[ptr + 3])

        datas.append((data, label))  # data 是 list，后面可以和 tuple 计算距离
        ptr += 4
    
    sample = tuple(map(float, all_data[ptr: ptr + 3]))

    return N, K, datas, sample

def euclidean_distance(arr1: Tuple, arr2: Tuple):
    """
    使用欧氏距离
    """
    if not len(arr1) == len(arr2):
        raise ValueError("欧氏距离计算数组不等长")
    
    ans = 0.0
    for i in range(len(arr1)):
        ans += (arr1[i] - arr2[i])  ** 2

    return np.sqrt(ans)  # 没问题，但可以用 math.sqrt 避免 numpy 依赖

def knn_classify(train_datas, predict_data, k) -> int:

    distances = []
    for train_data, train_label in train_datas:
        dist = euclidean_distance(predict_data, train_data)
        distances.append((dist, train_label))

    distances.sort(key = lambda x: x[0])
    sorted_distances = distances  # 多余，可以直接用 distances

    valid_label = [label for dist, label in sorted_distances[: k]]

    # !!! 错误：统计 label 次数时写成了 label += 1，这修改了循环变量，且未更新 memo 中的值
    memo = {}
    for label in valid_label:
        if label in memo:
            label += 1          # 错误！应该是 memo[label] += 1
        else:
            memo[label] = 1

    # !!! 上述错误导致 memo 中永远只有每个 label 出现一次（因为 label 被修改后变成了新值）
    # 修正后的代码：
    # for label in valid_label:
    #     memo[label] = memo.get(label, 0) + 1

    max_num_label = -1
    max_num_counts = -1
    for label, counts in memo.items():
        if counts > max_num_counts:
            max_num_label = label
            max_num_counts = counts
    
    return max_num_label

def main(all_data = None):

    N, K, datas, sample = get_input(all_data)  # all_data 参数未使用，但无影响

    predict_label = knn_classify(train_datas = datas, 
                                 predict_data = sample, 
                                 k = K)
    
    return predict_label

if __name__ == "__main__":
    print(main())





"""
V0 修复版
"""


import sys
import numpy as np
from typing import Tuple, List  # !!! 缺少导入，会导致运行时 NameError

def get_input(all_data = None) -> Tuple[int, int, 
                         List[Tuple[Tuple[float, float, float], int]],
                         Tuple[float, float, float]]:
    
    if not all_data:
        all_data = sys.stdin.read()

    all_data = all_data.strip().split()

    ptr = 0

    N, K = int(all_data[ptr]), int(all_data[ptr + 1])
    ptr += 2

    datas = []
    for i in range(N):
        data = list(map(float, all_data[ptr: ptr + 3]))
        label = int(all_data[ptr + 3])

        datas.append((data, label))  # data 是 list，后面可以和 tuple 计算距离
        ptr += 4
    
    sample = tuple(map(float, all_data[ptr: ptr + 3]))

    return N, K, datas, sample

def euclidean_distance(arr1: Tuple, arr2: Tuple):
    """
    使用欧氏距离
    """
    if not len(arr1) == len(arr2):
        raise ValueError("欧氏距离计算数组不等长")
    
    ans = 0.0
    for i in range(len(arr1)):
        ans += (arr1[i] - arr2[i])  ** 2

    return np.sqrt(ans)  # 没问题，但可以用 math.sqrt 避免 numpy 依赖

def knn_classify(train_datas, predict_data, k) -> int:

    distances = []
    for train_data, train_label in train_datas:
        dist = euclidean_distance(predict_data, train_data)
        distances.append((dist, train_label))

    distances.sort(key = lambda x: x[0])
    sorted_distances = distances  # 多余，可以直接用 distances

    valid_label = [label for dist, label in sorted_distances[: k]]

    memo = {}
    for label in valid_label:
        memo[label] = memo.get(label, 0) + 1

    max_num_label = -1
    max_num_counts = -1
    for label, counts in memo.items():
        if counts > max_num_counts:
            max_num_label = label
            max_num_counts = counts
    
    return max_num_label

def main(all_data = None):

    N, K, datas, sample = get_input(all_data)  # all_data 参数未使用，但无影响

    predict_label = knn_classify(train_datas = datas, 
                                 predict_data = sample, 
                                 k = K)
    
    return predict_label

if __name__ == "__main__":
    print(main())


