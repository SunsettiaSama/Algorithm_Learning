


# 我知道了，另类的dp区间，类似的东西
from typing import List

from typing import List  # 你漏了导入，不影响核心，但补一下
class Solution:
    def longestPath(self, parent: List[int], s: str) -> int:
        
        size = len(parent)

        adj = [[] for i in range(size)]
        # ==================== 错误1：索引越界！致命！ ====================
        # 根节点 parent[node] = -1，adj[-1] 是非法索引（数组不能有-1下标）
        for node in range(size):
            adj[parent[node]].append(node)

        ans = [0]
        # 定义节点的状态为：当前节点能向上延伸的最大合法路径长度
        def dfs(node):
            node_len = 0  # 存储当前节点的最大单链长度
            # ==================== 错误2：node_len 从未更新！全程都是0 ====================
            for neighbor in adj[node]:
                neighbor_len = dfs(neighbor)

                if s[node] != s[neighbor]:
                    # ==================== 错误3：ans更新逻辑错了 ====================
                    # node_len一直是0，算出来永远是 0+... 根本不对
                    ans[:] = max(ans[0], node_len + neighbor_len + 1)
                    # ==================== 错误4：赋值完全写反！逻辑混乱 ====================
                    # 你想更新当前节点长度，却改了邻居的返回值
                    neighbor_len = max(node_len, neighbor_len + 1)
                
            # ==================== 错误5：返回值固定为0！完全失效 ====================
            # 必须返回当前节点的最大单链长度，而不是初始的0
            return node_len

        dfs(0)
        # ==================== 错误6：返回值错了！ ====================
        # 1. ans是列表，要返回ans[0]；2. ans已经是边数，不需要+1
        return ans + 1

"""
V0 豆包修复版

"""

from typing import List
class Solution:
    def longestPath(self, parent: List[int], s: str) -> int:
        size = len(parent)
        adj = [[] for _ in range(size)]
        
        # 修复1：跳过根节点(parent=-1)，避免索引越界
        for node in range(1, size):  # 从1开始，根节点0不用处理
            p = parent[node]
            adj[p].append(node)

        ans = 0  # 直接用数字，不用列表

        def dfs(node):
            nonlocal ans
            max1 = 0  # 当前节点的 最长子链
            max2 = 0  # 当前节点的 次长子链

            for child in adj[node]:
                child_len = dfs(child)
                # 只有字母不同，才是合法路径
                if s[node] != s[child]:
                    # 更新当前节点的最长/次长子链
                    now = child_len + 1
                    if now > max1:
                        max2 = max1
                        max1 = now
                    elif now > max2:
                        max2 = now

            # 最长路径 = 最长子链 + 次长子链
            ans = max(ans, max1 + max2)
            # 修复2/5：返回当前节点能向上延伸的 最长单链
            return max1

        dfs(0)
        # 修复6：直接返回答案（ans就是最终长度）
        return ans




"""
V1 手搓

"""

from typing import List
class Solution:
    def longestPath(self, parent: List[int], s: str) -> int:
        size = len(parent)
        adj = [[] for _ in range(size)]
        
        # 修复1：跳过根节点(parent=-1)，避免索引越界
        for node in range(1, size):  # 从1开始，根节点0不用处理
            p = parent[node]
            adj[p].append(node)

        ans = 0  # 直接用数字，不用列表
        def dfs(node):
            nonlocal ans

            curr_max_len = 0
            for neighbor in adj[node]:
                neighbor_max_len = dfs(neighbor)
                # 判定是否合法
                if s[node] != s[neighbor]:
                    ans = max(ans, curr_max_len + neighbor_max_len + 1) # 更新最长子链
                    curr_max_len = max(curr_max_len, neighbor_max_len + 1)
            
            return curr_max_len


            # 传入了当前节点












