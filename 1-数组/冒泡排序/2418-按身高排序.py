

import numpy as np

class Solution:
    def sortPeople(self, names: List[str], heights: List[int]) -> List[str]:

        sorted_indices = np.argsort(np.array(heights, dtype = int))[::-1]

        return [names[item] for item in sorted_indices]



# ==========================上述是numpy做这个题目================================


class Solution:
    def sortPeople(self, names: List[str], heights: List[int]) -> List[str]:

        # 关键是同步交换名字

        n = len(names)

        for i in range(n - 1):

            swapped = False

            for j in range(n - i - 1):

                if heights[j] < heights[j + 1]:

                    heights[j], heights[j + 1] = heights[j + 1], heights[j]
                    names[j], names[j + 1] = names[j + 1], names[j]
                    swapped = True

            if swapped == False:
                break

        return names
