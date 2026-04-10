class Solution:
    def eraseOverlapIntervals(self, intervals: list):
        if not intervals:
            return 0
        
        # 先进行排序
        intervals.sort(key = lambda item: item[1])

        # 迭代算法
        # 初始化第一个区间的状态
        eos_pos = intervals[0][1]
        count = 1
        for i in range(1, len(intervals)):
            if eos_pos <= intervals[i][0]:
                count += 1
                eos_pos = intervals[i][1]
        
        return len(intervals) - count
    