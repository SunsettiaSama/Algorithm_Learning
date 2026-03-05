
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
