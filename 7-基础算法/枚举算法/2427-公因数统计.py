class Solution:
    def commonFactors(self, a: int, b: int) -> int:
        if a == 1 and b == 1:
            return 1
        
        num = 0
        for x in range(1, a * b):
            if a % x == 0 and b % x == 0:
                num += 1
        return num

class Solution:
    def commonFactors(self, num1, num2):

        if num1 == 1 and num2 == 1:
            return 1
        
        res = 0

        for factor in range(1, min(num1, num2) + 1): # 注意迭代边界，老规矩，如果要迭代到它自身，记得加一
            if num1 % factor == 0 and num2 % factor == 0:
                res += 1

        return res


"""
V0
"""
# 最大公因数求取

class Solution:
    def commonFactors(self, num1, num2):

        if num1 == 1 or num2 == 1:
            return 1
        
        counts = 0

        for index in range(1, min(num1, num2) + 1):

            if num1 % index == 0 and num2 % index == 0:
                # 记录公因数，反向遍历
                counts += 1
        
        return counts









if __name__ == "__main__":
    s = Solution()
    print(s.commonFactors(1, 1))