# 本质上是kmeans分类算法


import sys
import numpy as np

def get_data():
    data = sys.stdin.read().strip().split()
    if not data: return

    idx = 0

    k = int(data[idx])
    idx += 1

    centers = []
    for _ in range(k):
        x, y, z = list(map(float, data[idx: idx + 2 + 1])) # 尾部截断
        centers.append([x, y, z])
        idx += 3

    centers = np.array(centers, dtype = float) # (k, 3)
        
    epoch = int(data[idx])
    idx += 1
    
    m = int(data[idx])
    idx += 1

    samples = []
    for sample_idx in range(m):

        x, y, z = list(map(float, data[idx: idx + 2 + 1])) # 尾部截断
        samples.append([x, y, z])

        idx += 3

    samples = np.array(samples, dtype = float) # (m, 3)
    
    return k, centers, epoch, m, samples
    


def solve():


    k, centers, epochs, m, samples = get_data()
    if centers is None: return 

    labels = [0 for i in range(len(samples))]
    for epoch in range(epochs): # s -> (m, 3), c -> (k, 3) -> (k, 1, 3)
        # delta -> (k, m, 3)
        # L2(delta) -> (k, m)
        distances = np.linalg.norm(samples[:, np.newaxis, :] - centers, axis = 2) 

        # Label(L2(deta)) -> (m, ) // k被压缩了
        labels = np.argmin(distances, axis = 1)

        # 此时所有点完成归类，迭代到新的点上
        new_centers = np.zeros_like(centers)
        for i in range(k):
            cluster_points = samples[labels == i] # (label_sample_size, 3)
            if len(cluster_points) > 0:
                new_centers[i] = np.mean(cluster_points, axis = 0)
            else:
                new_centers[i] = centers[i]

        centers = new_centers
    
    for center in centers:
        print(f"{center[0]:.2f} {center[1]:.2f} {center[2]:.2f}")


# if __name__ == "__main__":
#     solve()



# ==============================================
# 第二次尝试
# ==============================================

import sys
import numpy as np


def get_data():

    all_nums = sys.stdin.read().split()
    ptr = 0

    k = int(all_nums[ptr])
    ptr += 1

    # 聚类点，拿到手了
    centers = []
    for _ in range(k):
        center = list(map(float, all_nums[ptr: ptr + 3]))
        ptr += 3
        centers.append(center)
    centers = np.array(centers, dtype = float)

    epochs = int(all_nums[ptr])
    ptr += 1

    m = int(all_nums[ptr])
    ptr += 1

    # 样本点
    samples = []
    for _ in range(m):
        sample = list(map(float, all_nums[ptr: ptr + 3]))
        ptr += 3
        samples.append(sample)
    samples = np.array(samples, dtype = float)


    return k, centers, epochs, m, samples

def solve():

    k, centers, epochs, m, samples = get_data()

    # 接下来开始做聚类

    # 据类具体的算法是，
    # 对任意一个点，根据L2范数，拿到欧氏距离最近的中心点，并归类
    # 当所有样本归类完成，则更新中心点，如此往复循环

    # 广播 
    samples = samples[np.newaxis, :, :]
    centers = centers[:, np.newaxis, :]
    for epoch in range(epochs):
        
        # 这里其实可以用代数方法，批量算出，而不需要for循环
        # centers: size = (k, 3) -> (k, m, 3)
        # samples: size = (m, 3) -> (k, m, 3)
        labels = np.argmin(np.linalg.norm(samples - centers, axis = 2), axis = 0)
        # samples[0, labels == i, :] -> (M_i, 3) -> (1, 3) -> (k, 3)
        new_centers = np.array([np.mean(samples[0, labels == i, :], axis = 0) for i in range(k)], dtype = float)
        centers = new_centers[:, np.newaxis, :]

    centers = centers[:, 0, :]

    for center in centers:
        print(f"{center[0]:.2f} {center[1]:.2f} {center[2]:.2f}")

if __name__ == "__main__":
    solve()