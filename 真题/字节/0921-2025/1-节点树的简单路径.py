



def get_input():
    import sys

    lines = sys.stdin.read().splitlines()

    n = int(lines[0])
    node_values = list(map(int, lines[1].split()))
    paths = []

    for _ in lines[2: ]:
        a, b = list(map(int, lines[1].split()))
        paths.append((a, b))
    
    return n, node_values, paths

# 哦，原来是边的意思，那就好说了啊

def search_nums():
    
    from collections import deque

    n, node_values, paths = get_input()

    queue = deque()
    queue.append(node_values)

    while queue:
         
        start_node, end_node = queue.popleft()
        # 判断两个条件

        # 1. 是否在路径上

        # 2. 如果在路径上，那么是否满足ax = ay的值

        # 但这里有一个问题我们没有处理过：如何对边进行广搜，我们都是对节点进行广搜的






    return 



