



import sys
from collections import defaultdict

# ---------------------- 工具函数：计算组合数 C(n,2) ----------------------
# 作用：计算n个元素中选2个的组合数（无序对数量）
def comb2(n):
    if n < 2:
        return 0
    return n * (n - 1) // 2

# ---------------------- 步骤1：处理输入，转化为邻接表 ----------------------
def get_input():
    # 读取所有输入并拆分成数字列表（避免按行处理的坑）
    all_nums = sys.stdin.read().split()
    pointer = 0  # 指针：记录当前读到哪个数字
    
    # 第一步：读节点总数n
    node_count = int(all_nums[pointer])
    pointer += 1
    
    # 第二步：读每个节点的权值（节点1对应索引0，节点2对应索引1...）
    node_values = list(map(int, all_nums[pointer:pointer + node_count]))
    pointer += node_count
    
    # 第三步：构建邻接表（1-based，索引0不用）
    # adj[current_node] 存储和current_node相连的所有节点
    adjacency_list = [[] for _ in range(node_count + 1)]
    # 树有n-1条边，循环读n-1次
    for _ in range(node_count - 1):
        u = int(all_nums[pointer])    # 边的第一个节点
        v = int(all_nums[pointer+1])  # 边的第二个节点
        adjacency_list[u].append(v)   # 无向边：双向添加
        adjacency_list[v].append(u)
        pointer += 2
    
    return node_count, node_values, adjacency_list

# ---------------------- 步骤2：递归DFS遍历树，计算答案 ----------------------
def dfs(current_node, parent_node, node_values, adjacency_list, cnt, current_sum, ans):
    """
    递归DFS遍历树，维护路径状态并计算答案
    :param current_node: 当前遍历的节点
    :param parent_node: 父节点（避免走回头路）
    :param node_values: 所有节点的权值
    :param adjacency_list: 邻接表
    :param cnt: 字典，记录当前路径上各值的出现次数
    :param current_sum: 当前路径上符合条件的无序对总数
    :param ans: 结果数组，ans[i]存储节点i的答案
    """
    # 1. 拿到当前节点的权值（节点编号是1-based，数组是0-based）
    current_val = node_values[current_node - 1]
    
    # 2. 记录更新前的计数（用于计算组合数增量）
    old_count = cnt[current_val]
    
    # 3. 更新当前值的计数：当前路径上多了一个该值的节点
    cnt[current_val] += 1
    
    # 4. 计算组合数增量：新的组合数 - 旧的组合数
    new_comb = comb2(cnt[current_val])
    old_comb = comb2(old_count)
    current_sum += (new_comb - old_comb)
    
    # 5. 记录当前节点的答案（此时current_sum就是1→current_node路径的答案）
    ans[current_node] = current_sum
    
    # 6. 遍历当前节点的所有邻居（递归访问子节点）
    for neighbor in adjacency_list[current_node]:
        # 跳过父节点，避免走回头路（保证路径是1→current_node→neighbor）
        if neighbor != parent_node:
            # 递归访问子节点，传递更新后的状态
            dfs(neighbor, current_node, node_values, adjacency_list, cnt, current_sum, ans)
    
    # 7. 回溯：离开当前节点时，恢复状态（不影响其他分支的遍历）
    cnt[current_val] -= 1
    # 如果计数归0，删除键（节省空间，可选）
    if cnt[current_val] == 0:
        del cnt[current_val]

# ---------------------- 主函数：整合所有逻辑 ----------------------
def main():
    # 步骤1：读取输入
    node_count, node_values, adjacency_list = get_input()
    
    # 初始化：结果数组（1-based）
    ans = [0] * (node_count + 1)
    
    # 初始化：记录路径上各值的出现次数（默认值0）
    value_count = defaultdict(int)
    
    # 步骤2：从根节点1开始DFS（父节点设为-1，表示没有父节点）
    dfs(current_node=1, 
        parent_node=-1, 
        node_values=node_values, 
        adjacency_list=adjacency_list, 
        cnt=value_count, 
        current_sum=0, 
        ans=ans)
    
    # 步骤3：输出结果（节点1到节点n的答案）
    print(' '.join(map(str, ans[1:node_count+1])))

# 程序入口
if __name__ == "__main__":
    main()


"""
V0手搓
"""
def get_input():
    """
    获取输入
    """
    import sys
    lines = sys.stdin.read().split('\n')

    n = int(lines[0])
    # ERROR1：语法/逻辑错误 - lines[1]是整行字符串，直接map会按字符拆分，且未转列表（map对象不可索引）
    node_values = map(int, lines[1])  # 也就是这里有一个处理上的问题,需要split来进行处理

    edges = []

    for line in lines[2: ]:
        # ERROR2：语法/逻辑错误 - 未拆分line（按空格），且map对象不可迭代为元组，未过滤空行
        edges.append(map(int, line))  
    
    return n, node_values, edges

def get_adj(n, edges):
    """
    获取邻接表
    """
    # 邻接表如何保存值呢？
    # 当前点，邻居节点，值？
    # ERROR3：逻辑错误 - 节点通常从1开始，range(n)会导致索引0~n-1，节点n越界
    adj = [[] for i in range(n)]  

    for u, v in edges:
        # ERROR4：语法错误 - append是方法，应使用()而非[]
        # 这小细节错误,我日
        adj[u].append[v]  
        adj[v].append[u]  
    
    return adj

def main():
    n, node_values, edges = get_input()

    # ERROR5：参数错误 - get_adj定义仅接收n和edges，此处传了3个参数（多传node_values）
    adj = get_adj(n, node_values, edges)  

    # 用以记录结果的表
    results = [0 for i in range(n)]

    visited_node = []

    def dfs(node_index, adj):
        # 处理当前节点
        neighbor_nodes = adj[node_index]
        # ERROR6：语法错误 - append是方法，应使用()而非[]
        visited_node.append[node_index]  

        # 如果不存在邻居点，则回退
        # 无需进一步处理
        if len(adj[node_index]) == 0:
            return 

        for neighbor_node in neighbor_nodes:
            # 访问邻接点
            # 这里有两个条件，如题所述，一个要求是简单路径，另一个要求是ax=ay

            # 简单路径的条件是这样：只要该节点没有回头，就可以算是简单路径，必须逐层向下深入
            # ERROR7：性能/逻辑错误 - in操作在列表中是O(n)，且未回溯visited_node（递归返回后未移除节点，导致路径错误）
            if neighbor_node in visited_node:
                continue 
            
            # 而另一个条件也比较简单，就是前后两个节点之间要比较大小
            # ERROR8：逻辑错误 - node_values是map对象不可索引，且未判断节点值相等的统计逻辑错误（仅统计相邻，未统计路径上所有）
            if node_values[node_index] == node_values[neighbor_node]:
                # 此时视作有效结果
                results[neighbor_node] += 1
            
            dfs(neighbor_node, adj)

    # ERROR9：逻辑错误 - 节点索引从0开始不符合常规（题目节点通常从1开始），且未处理父节点导致重复访问
    dfs(0, adj)  

    print(' '.join(map(str, results)))

"""
修正版：统计从根节点（1）到每个节点的简单路径上值相等的节点对数量

这个题目综合性很高,需要再捋一捋,重新写一遍
"""
import sys
from collections import defaultdict

def get_input():
    """
    正确处理输入：按空格拆分，过滤空行，返回节点数、节点值、边列表
    """
    data = sys.stdin.read().split()  # 一次性读取所有输入并按空格拆分
    ptr = 0
    n = int(data[ptr])
    ptr += 1
    
    # 节点值：索引1~n（匹配题目节点编号）
    node_values = [0] * (n + 1)
    for i in range(1, n + 1):
        node_values[i] = int(data[ptr])
        ptr += 1
    
    # 边列表：过滤空行，转为元组
    edges = []
    for _ in range(n - 1):
        u = int(data[ptr])
        v = int(data[ptr + 1])
        edges.append((u, v))
        ptr += 2
    
    return n, node_values, edges

def get_adj(n, edges):
    """
    构建邻接表：索引1~n
    """
    adj = [[] for _ in range(n + 1)]  # 节点1~n
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj

def main():

    n, node_values, edges = get_input()  # 拿题目给的“家底”：n是节点总数，node_values是每个节点的值（比如node_values[2]=1就是节点2的值是1），edges是节点间的连线（比如1和2连着）
    adj = get_adj(n, edges)              # 做个“邻居表”：比如adj[2]里存着2的所有邻居（1和3），方便找“谁家和谁家挨着”
    res = [0] * (n + 1)                  # 结果本初始化：一开始所有节点的答案都是0（索引0不用，节点从1开始）
    # 这个其实就起到了一个历史路径的作用,相当于用哈希表,存了一个之前的值,如果发现这个值走过了,于是就跳过
    cnt = defaultdict(int)               # 计数器本初始化：一开始空的，没记任何值,

    
    def dfs(u, parent):
        # 1. 先看当前节点u的值是多少，再算新增的相等对数量
        val = node_values[u]          # 比如u是2，val就是节点2的值（假设是1）
        old_cnt = cnt[val]            # 查计数器本：之前走的路上，值为val的节点见过多少次？比如之前见过1次值为1的，old_cnt=1
        cnt[val] += 1                 # 计数器本更新：现在又见到1个val值的节点，数量+1（比如从1变成2）
        
        # 2. 记当前节点的答案：父节点（上一个节点）的答案 + 这次新增的相等对
        res[u] = res[parent] + old_cnt  # 比如父节点1的答案是0，这次新增1对，那节点2的答案就是0+1=1
        
        # 3. 去拜访当前节点的所有邻居（不走回头路）
        for v in adj[u]:              # 遍历u的所有邻居（比如u=2，邻居是1和3）
            if v == parent:           # 如果邻居是上一个节点（比如u=2，parent=1，邻居1就是回头路），跳过！
                continue
            dfs(v, u)                 # 去拜访邻居v，告诉v：你的上一个节点是u，别回头
        
        # 4. 离开当前节点时，计数器本“回退”（关键！）
        cnt[val] -= 1                 # 比如走完2的所有邻居（3），要离开2了，把val的计数减1（比如从2变回1），因为后面走其他路时，2不在那条路上了
    
    dfs(1, 0)  # 从根节点1开始串门，1没有上一个节点，parent设为0（随便一个不存在的节点就行）
    print(' '.join(map(str, res[1:n+1])))  # 把结果本里1~n的答案拿出来，用空格分开打印

if __name__ == "__main__":
    main()



