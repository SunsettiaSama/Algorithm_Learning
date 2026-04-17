


import sys

def get_input(input_string = None):

    if not input_string:
        strings = sys.stdin.read()
    else:
        strings = input_string

    ptr = 0
    strings = strings.strip().split()

    n, m = int(strings[ptr]), int(strings[ptr + 1])
    ptr += 2

    datas = []

    for i in range(n):
        lis = []
        for j in range(m):
            lis.append(int(strings[ptr]))
            ptr += 1

        datas.append(lis)

    
    return n, m, datas

def main(input_string = None):

    n, m, datas = get_input(input_string)

    sum_row = [sum(line) for line in datas]
    sum_col = []

    # 先完成行列相加，再予以判定
    for i in range(m):
        curr_col = [datas[row_index][i] for row_index in range(n)]
        sum_col.append(sum(curr_col))


    # 最后，进行查找，查找二者相等的值
    ans = 0
    for row_index in range(n):
        for col_index in range(m):
            if sum_row[row_index] == sum_col[col_index]:
                ans += 1

    return ans


if __name__ == "__main__":
    print(main())