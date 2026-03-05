


def condition1(x, y, z):
    return 5 * x + 3 * y + 1/3 * z == 100

def condition2(x, y, z):
    return x + y + z == 100

# 我们的解，也是正确的
class Solution:
    def buyChicken(self):
        for x in range(100):
            for y in range(100):
                for z in range(100):
                    if condition1(x, y, z) and condition2(x, y, z):
                        print("公鸡{}只，母鸡{}只，小鸡{}只".format(x, y, z))
        
# 正解
class Solution:
    def buyChicken(self):
        for x in range(101):
            for y in range(101):
                for z in range(101):
                    if z % 3 == 0 and 5 * x + 3 * y + z // 3 == 100 and x + y + z == 100:
                        print("公鸡 %s 只，母鸡 %s 只，小鸡 %s 只" % (x, y, z))


"""
V0

"""

class Solution:
    def buyChicken(self):
        
        for x in range(101):
            for y in range(101):
                for z in range(101):
                    if condition1(x, y, z) and condition2(x, y, z):
                        print((x, y, z))


def condition1(x, y, z):
    return 5 * x + 3 * y + 1/3 * z == 100

def condition2(x, y, z):
    return x + y + z == 100


if __name__ == "__main__":
    solu = Solution()
    solu.buyChicken()







