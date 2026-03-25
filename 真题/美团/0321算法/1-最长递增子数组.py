
import sys


def get_input():

    lines = sys.stdin.read().strip().split("\n")
    ptr = 0

    T = int(lines[0])
    ptr += 1

    arrays = []

    for i in range(T):
        
        n = lines[ptr]
        ptr += 1
        array = map(int, lines[ptr].split(" "))
        ptr += 1

        arrays.append((n, array))

    return T, arrays

def main():

    T, arrays = get_input()

    for n, array in arrays:
        # 统计结果
        # 这里不需要一个个统计，直接一个初始化全搞定
        res_set = set(array)
        print(len(res_set))



if __name__ == "__main__":
    main()