










import sys
import math
import numpy as np


import math
import numpy as np

def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def kmeans(points, K, max_iter=100):
    sorted_points = sorted(points, key=lambda p: (euclidean_distance(p, (0, 0)), points.index(p)))
    centers = [sorted_points[i] for i in range(K)]
    for _ in range(max_iter):
        clusters = [[] for _ in range(K)]
        for p in points:
            closest_center = min(range(K), key=lambda i: euclidean_distance(p, centers[i]))
            clusters[closest_center].append(p)
        new_centers = [(np.mean([p[0] for p in cluster]), np.mean([p[1] for p in cluster])) if cluster else centers[i] for i, cluster in enumerate(clusters)]
        if sum(euclidean_distance(centers[i], new_centers[i]) for i in range(K)) < 1e-4:
            break
        centers = new_centers
    return centers

def calculate_total_time(K, N, speed, points):
    centers = kmeans(points, K)
    distances = sorted([(euclidean_distance(center, (0, 0)), center) for center in centers])
    total_distance = sum(euclidean_distance(distances[i][1], distances[i+1][1]) for i in range(len(distances) - 1)) + euclidean_distance(distances[-1][1], (0, 0))
    return int((total_distance / speed) * 3600)



"""
V0 模仿

"""

import sys
import math
import numpy
def distance(a, b):
    diff = a - b
    return math.sqrt(diff[0] * diff[0] + diff[1] * diff[1])

def kmeans(points, k, max_iters = 50, tol = 1e-4):

    n = len(points)

    # 聚类中心数量
    m = min(k, n)

    # 不建议随意初始化，尽量选择较近的点进行初始化
    order = sorted(range(n), key = lambda i: (points[i][0] ** 2 + points[i][1] * 2, i))
    centers = points[order[:m]].copy()


    labels = np.zeros(n, dtype = int)

    for _ in range(max_iters):

        old_centers = centers.copy()

        # 第一步：把每个点分配到最近的聚类中心，形成簇
        for i in range(n):
            best_idx = 0
            best_dist = float("inf")

            for j in range(m):
                d = distance(points[i], centers[j])
                if d < best_dist:
                    best_dist = d
                    best_idx = j
            labels[i] = best_idx

        # 重新计算簇中心
        new_centers = centers.copy()
        for j in range(m):
            cluster_points = points[labels == j]

            if len(cluster_points) > 0:
                new_centers[j] = cluster_points.mean(axis = 0)
            
        centers = new_centers

        move_sum = 0.0
        for j in range(m):
            move_sum += distance(old_centers[j], centers[j])
        
        if move_sum < tol:
            break

    return centers

def solve(k, n, speed, points):

    centers = kmeans(points, k)
    centers = sorted(centers, 
                     key = lambda point: point[0] * point[0] + point[1] * point[1])
    
    origin = np.array([0.0, 0.0])

    total_dist = 0.0
    prev = origin

    for center in centers:
        total_dist += distance(prev, center)
        prev = center
    
    total_dist += distance(prev, origin)

    total_time = math.floor(total_dist * 3600 / speed)
    return total_time
def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return

    k = int(data[0])
    n = int(data[1])
    speed = int(data[2])

    vals = list(map(float, data[3:]))
    points = []
    for i in range(0, 2 * n, 2):
        points.append([vals[i], vals[i + 1]])

    points = np.array(points, dtype=float)

    ans = solve(k, n, speed, points)
    print(ans)


if __name__ == "__main__":
    main()


"""
V0 手搓

"""

def euclidean_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def init_clusters(points, K) -> list:
    
    # 取离原点最近的k个点作为簇中心
    sorted_points_idx = sorted(range(len(points)), 
                           key = lambda p_idx: (euclidean_distance(points[p_idx], (0, 0)), p_idx))
    
    # 错误：Python列表不支持这种索引方式
    # 修正：使用列表推导式获取排序后的点
    # return points[sorted_points_idx[: K]]
    return [points[i] for i in sorted_points_idx[:K]]

def delivery_clusters(points, clusters):

    labels = [0 for i in range(len(points))]

    for p_idx, point in enumerate(points):
        # 记录最佳标签
        best_idx = 0
        best_dis = float('inf')
        for idx, cluster in enumerate(clusters):
            curr_dis = euclidean_distance(cluster, point)
            if curr_dis < best_dis:
                best_dis = curr_dis
                best_idx = idx

        labels[p_idx] = best_idx
    
    return labels
        
def count_new_clusters(points, labels, K):

    clusters = [(0, 0) for i in range(K)]
    for cluster_idx in range(K):
        # 错误：列表不支持布尔索引
        # 修正：用列表推导式获取属于当前簇的点
        # clusters[cluster_idx] = np.mean(points[labels == cluster_idx], axis = 0)
        cluster_points = [points[i] for i in range(len(points)) if labels[i] == cluster_idx]
        if cluster_points:  # 处理空簇情况
            clusters[cluster_idx] = np.mean(cluster_points, axis = 0)

    return clusters

def need_break(clusters, new_clusters, err):

    total_dis = 0
    for idx in range(len(clusters)):
        total_dis += euclidean_distance(clusters[idx], new_clusters[idx])
    
    return total_dis < err


def kmeans(points, K, max_epoch = 50, err = 1e-4):

    K = min(len(points), K)
    clusters = init_clusters(points, K)

    for epoch in range(max_epoch):

        # 初始化完成后，为每一个点分配标签
        labels = delivery_clusters(points, clusters)

        # 计算新的中心
        new_clusters = count_new_clusters(points, labels, K)

        if need_break(clusters, new_clusters, err):
            break

        clusters = new_clusters

    return clusters

def solve_time(clusters, speed):
    # 计算配送时间，这一小块的逻辑有点弄不明白了

    sorted_clusters_idx = sorted(range(len(clusters)), 
                        key = lambda p_idx: (euclidean_distance(clusters[p_idx], (0, 0)), p_idx))
    
    # 错误：Python列表不支持这种索引方式
    # 修正：用列表推导式获取排序后的簇
    # sorted_clusters = clusters[sorted_clusters_idx]
    sorted_clusters = [clusters[i] for i in sorted_clusters_idx]

    total_distance = 0.0

    if not sorted_clusters:
        return 0
    
    # 关键在这个位置
    start_point = (0, 0)
    curr_pos = start_point

    # 错误：循环的是原始clusters列表，而不是排序后的sorted_clusters
    # 修正：遍历排序后的簇，计算连续路径
    # for next_pos in clusters:
    for next_pos in sorted_clusters:
        # 错误：没更新当前位置，导致每次都从起点计算
        # 修正：计算从当前位置到下一个位置的距离，并更新当前位置
        # total_distance += euclidean_distance(curr_pos, next_pos)
        dist = euclidean_distance(curr_pos, next_pos)
        total_distance += dist
        curr_pos = next_pos  # 更新当前位置
    
    # 最后回到起点
    # 错误：最后回到起点时，curr_pos应该是最后一个中心点
    # 修正：确保从最后一个中心点返回起点
    total_distance += euclidean_distance(curr_pos, (0, 0))

    # 错误：np.floor返回的是numpy标量，可能需要转换为int
    # 修正：确保返回整数
    # return np.floor(total_distance / speed * 3600)
    return int(np.floor(total_distance / speed * 3600))


def main():
    # 错误：未导入sys模块
    # 修正：添加import sys
    import sys
    data = sys.stdin.read().strip().split()
    if not data:
        return

    K = int(data[0])
    N = int(data[1])
    speed = int(data[2])
    ptr = 3

    points = []

    for i in range(N):
        points.append( (float(data[ptr]), float(data[ptr + 1])) ) 
        ptr += 2

    clusters = kmeans(points, K)
    # 计算配送时间
    total_time = solve_time(clusters, speed)

    # 确保输出整数
    print(int(total_time))



    """
    ===========================================================================================
    计算配送时间这一块，没做出来，需要学习
    """

