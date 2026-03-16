### BFS核心模板（矩阵/图遍历）
#### 1. 核心流程（精简版）
1. 初始化：队列存入起始坐标，标记为已访问；
2. 循环：队列非空时，取出队首元素（当前处理节点）；
3. 扩展：遍历当前节点邻域（如矩阵四方向），合法且未访问则标记+入队；
4. 终止：队列为空，遍历完成。

#### 2. 模板代码（Python）
```python
import collections
from typing import Any, List

def general_bfs(
    start_node: Any,          # 起始节点（可传坐标/节点对象/值）
    get_neighbors: callable,  # 自定义：获取当前节点的所有邻接节点
    is_valid: callable,       # 自定义：判断邻接节点是否合法（边界/条件）
    mark_visited: callable    # 自定义：标记节点为已访问
) -> None:
    # 1. 初始化队列 + 标记起始节点已访问
    queue = collections.deque([start_node])
    mark_visited(start_node)
    
    # 2. 核心循环：队列非空则处理
    while queue:
        curr_node = queue.popleft()  # 必须取队首（BFS核心：先进先出）
        
        # 3. 遍历所有邻接节点
        for neighbor in get_neighbors(curr_node):
            # 4. 过滤：合法且未访问才处理
            if is_valid(neighbor):
                mark_visited(neighbor)
                queue.append(neighbor)
```

#### 3. 关键要点
- 核心动作：`popleft()` 取队首 + 邻域入队 + 标记已访问；
- 适配调整：`directions` 可改（如八方向），标记方式可选`visited`数组；
- 多源BFS：初始化时将所有起点入队即可。