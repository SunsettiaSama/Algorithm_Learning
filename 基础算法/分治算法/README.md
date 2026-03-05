# 分治算法

- 分治是一种「拆分—求解—合并」的通用思维范式：将大问题拆为若干规模更小且相互独立的同构子问题，递归（或迭代）求解到足够小的基例，最后自底向上合并结果。是否适合分治，取决于子问题是否独立、规模能否尽量均衡、以及合并是否足够高效。

- 实践中要关注三个要点：

    - 明确且正确的递归基与边界，避免无穷递归与越界；
    - 尽量使子问题独立、规模均衡，必要时调整划分策略；
    - 评估合并代价，如果合并过重或子问题高度重叠，应考虑动态规划、记忆化或改用其他范式。



合理运用这些原则，分治能在排序、查找、几何与数值计算等领域提供简洁而高效的解法。

## 分治算法应用
### 归并排序
- 任意给定一个数列，如何对该数列元素进行升序（降序）排列？
    - 不借助任何内置函数实现；

```python 
from typing import List

class Solution:
    def merge(self, left_array, right_array):
        """
        所以你是第i个子问题的合并方法
        """
        # 最终结果
        array = []

        # 针对所有内部元素都进行插入
        while left_array and right_array:
            if left_array[0] <= right_array[0]:
                array.append(left_array.pop(0))
            else:
                array.append(right_array.pop(0))
        
        # 为什么这里不再进行检查呢？直接进行添加？
        # 不对，思考角度问题
        # 明白了，其实这里不重要，如果左侧有多余，那么右侧为空
        # 如果右侧有多余，则左侧为空
        # 又或者两个都为空

        # 反正的反正，总而言之，不可能都 同时 不为空 ！
        while left_array:
            array.append(left_array.pop(0))
        
        while right_array:
            array.append(right_array.pop(0))

        return array
    
    def mergeSort(self, array):
        # 实际上你这个是一个递归体
        # 终止条件
        if len(array) <= 1:
            return array
        
        # 递归内容
        # 简单分治算法的确很适合递归这种结构呢
        # 不对、其实复杂的也很适合
        
        mid = len(array) // 2

        # 递归体内容：左侧数组的分解和排序
        left_array = self.mergeSort(array[0: mid])

        # 递归体内容：右侧数组的分解和排序
        right_array = self.mergeSort(array[mid: ])

        # 分解排序后，再统一合并
        return self.merge(left_array, right_array)

    def sortArray(self, nums: List[int]) -> List[int]:
        return self.mergeSort(nums)
    


if __name__ == "__main__":
    s = Solution()
    print(s.sortArray([12, 2, 5, 7]))
```


