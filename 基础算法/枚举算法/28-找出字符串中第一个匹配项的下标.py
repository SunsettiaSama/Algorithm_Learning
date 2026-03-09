
class Solution:
    def strStr(self, haystack: str, needle: str) -> int:

        for haystack_index in range(len(haystack) - len(needle) + 1):
            res = 0

            for needle_index in range(len(needle)):
                if haystack[haystack_index] == needle[needle_index]:
                    res += 1
                    haystack_index += 1
            
            if res == len(needle):
                return haystack_index - len(needle)
        
        return -1
    


"""
V1

"""

class Solution:
    def strStr(self, haystack: str, needle: str) -> int:

        if len(haystack) == 0 or len(needle) == 0:
            return -1
        
        # 遍历，且维护一个大小为needle的窗口
        for slow_index in range(len(haystack) - len(needle) + 1):
            if haystack[slow_index: slow_index + len(needle)] == needle:
                return slow_index
        
        return -1
    

