
from typing import List

class Solution:
    def reverseString(self, s: List[str]) -> None:
        """
        Do not return anything, modify s in-place instead.
        """

        left = 0
        right = len(s) - 1

        while left < right:

            s[left], s[right] = s[right], s[left] # 这一行需要记忆，这种用法还是少见

            left += 1
            right -= 1

        return s
