class Solution:
    def findContentChildrenV0(self, g, s):
        """
        V0问题:没有对饼干进行排序,无法得到最优解
        
        """
        # 每个小孩都算是一个问题
        # 在这个问题中，需要取得最优的解
        # 那么，这个饼干应该比最小的大一点点就行
        # 也即满足s[j] > g[i]的最小饼干尺寸s[j]
        # 那也就有这种做法

        g.sort()
        visited = [False for i in range(len(s))]
        res = 0
        # 对于每一个问题，有全局最优搜索
        for index, gi in enumerate(g):
            # 条件为sj > gi
            # 若采用枚举算法
            for jindex, sj in enumerate(s):
                # 没有被分配过并且满足大小
                if sj >= gi and not visited[jindex]: 
                    visited[jindex] = True # 饼干已被分配
                    res += 1
                    break
        
        return res
    

    def findContentChildrenV1(self, g, s):
        # 每个小孩都算是一个问题
        # 在这个问题中，需要取得最优的解
        # 那么，这个饼干应该比最小的大一点点就行
        # 也即满足s[j] > g[i]的最小饼干尺寸s[j]
        # 那也就有这种做法

        g.sort()
        visited = [False for i in range(len(s))]
        res = 0
        # 对于每一个问题，有全局最优搜索
        for index, gi in enumerate(g):
            # 条件为sj > gi
            # 若采用枚举算法
            for jindex, sj in enumerate(s):
                # 没有被分配过并且满足大小
                if sj >= gi and not visited[jindex]: 
                    visited[jindex] = True # 饼干已被分配
                    res += 1
                    break
        
        return res
    