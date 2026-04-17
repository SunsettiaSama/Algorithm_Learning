
from typing import List
class Solution:
    def maxDistance(self, position: List[int], m: int) -> int:
        position.sort()
        left, right = 1, position[-1] - position[0]
        
        def check(min_force):
            count = 1
            last_pos = position[0]
            for i in range(1, len(position)):
                if position[i] - last_pos >= min_force:
                    count += 1
                    last_pos = position[i]
                    if count == m:
                        return True
            return False
        
        while left < right:
            mid = (left + right + 1) >> 1
            if check(mid):
                left = mid
            else:
                right = mid - 1
        return left
    

"""
V0 手搓

"""
from typing import List
class Solution:
    def maxDistance(self, position: List[int], m: int) -> int:
        position.sort()

        left = 1
        right = position[-1] - position[0]

        return self._binary_search_force(position, m, left, right)
    
    def _binary_search_force(self, position, m, left, right):

        while left < right:
            mid = (left + right + 1) // 2

            if self._can_place_balls(position, m, mid):
                left = mid
            else:
                right = mid - 1

        return left
    
    def _can_place_balls(self, position, m, min_force):
        count = 1
        last_pos = position[0]
        for i in range(1, len(position)):
            if position[i] - last_pos >= min_force:
                count += 1
                last_pos = position[i]

                if count == m:
                    return True
        
        return count >= m
    

