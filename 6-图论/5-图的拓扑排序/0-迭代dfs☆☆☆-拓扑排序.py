



def findOrder(numCourses: int, prerequisites):
    # 建图：DAG 邻接表
    g = [[] for _ in range(numCourses)]
    for a,b in prerequisites:
        g[b].append(a)
    
    vis = [False] * numCourses
    post = []   # 存后序遍历结果

    for i in range(numCourses):
        if not vis[i]:
            stk = [(i, False)]
            while stk:
                u, processed = stk.pop()
                if processed:
                    # 子节点全部走完，后序收录
                    post.append(u)
                    continue
                if vis[u]:
                    continue
                vis[u] = True
                # 先压自己(待处理)，再逆序压邻点，保证顺序一致
                stk.append((u, True))
                # 逆序入栈 = 保持和递归DFS一样的遍历顺序
                for v in reversed(g[u]):
                    if not vis[v]:
                        stk.append((v, False))
    # DFS拓扑：后序反转
    topo = post[::-1]
    return topo




def findOrder(numCourses, prerequisities):

    g = [[] for _ in range(numCourses)]

    for a, b in prerequisities:
        g[b].append(a) 
    
    vis = [False] * numCourses
    post = []


    for i in range(numCourses):
        if not vis[i]:
            stk = [(i, False)]
            while stk:
                u, processed = stk.pop()

                if processed:
                    # 第二次遇到，后序压入当前节点
                    post.append(u)
                
                if vis[u]:
                    continue

                vis[u] = True

                stk.append((u, True))

                for v in reversed(g[u]):
                    if not vis[v]:
                        stk.append((v, False))
        
    topo = post[::-1]
    return topo










