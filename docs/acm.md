# ACM 本地调试接口

> 路径：`ACM/__init__.py`

## 背景

ACM / 竞赛题目通常用 `sys.stdin.read()` 或 `input()` 读取控制台输入。本地调试时需要反复在终端粘贴样例，效率低且容易出错。

`ACM` 模块把**字符串注入为 stdin**，让本地调试与单元测试一样简洁，支持以下场景：

- 直接运行一个算法函数并捕获输出
- 运行完整的脚本文件（支持 `if __name__ == '__main__':` 块）
- 在代码块内部直接使用 `input()` / `sys.stdin.read()`
- 批量测试多组样例，自动比对期望输出

---

## 快速开始

```python
import sys
sys.path.insert(0, r"G:\AlgorithmLearning\BaseAlgorithmLearning")

from ACM import run, run_file, stdin_as, test, build_input
```

---

## API 参考

### `run(func, input_str, *, capture=True, print_output=False) -> str`

以 `input_str` 作为 stdin 运行无参函数 `func()`，返回其 stdout 字符串。

| 参数 | 类型 | 说明 |
|------|------|------|
| `func` | `Callable` | 算法入口函数（无参） |
| `input_str` | `str` | 注入的输入，行间用 `\n` 分隔 |
| `capture` | `bool` | `True`（默认）返回捕获的输出；`False` 直接打印到控制台 |
| `print_output` | `bool` | `True` 时捕获的同时额外打印到控制台 |

```python
def solution():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    print(sum(int(x) for x in data[1:n+1]))

output = run(solution, "5\n1 2 3 4 5")
print(output)   # "15\n"

# 捕获 + 直接看输出，两全其美
run(solution, "5\n1 2 3 4 5", print_output=True)
```

> **注意**：若算法脚本在**模块级**（函数外）绑定了 `input = sys.stdin.readline`，
> 该绑定在 `run()` 调用前已确定，不受重定向影响。
> 此时改用 `run_file()` 或将绑定语句移到函数内部。

---

### `run_file(filepath, input_str, *, capture=True, print_output=False) -> str`

以 `input_str` 作为 stdin 运行指定 Python 脚本文件，返回其 stdout。

使用 `runpy.run_path` 执行，脚本的 `__name__` 被设为 `'__main__'`，
因此 `if __name__ == '__main__':` 块会正常运行。

```python
# 运行同目录下的脚本
output = run_file("动态规划/53-最大子数组和.py", "8\n-2 1 -3 4 -1 2 1 -5")
print(output)   # "6\n"

# 绝对路径同样支持
output = run_file(r"G:\AlgorithmLearning\BaseAlgorithmLearning\动态规划\solution.py",
                  "5\n1 2 3 4 5")
```

---

### `stdin_as(input_str)` — 上下文管理器

在 `with` 块内把 `sys.stdin` 替换为 `input_str`，适合**直接写算法逻辑**而无需封装函数。

```python
from ACM import stdin_as

with stdin_as("3\n10 20 30"):
    n = int(input())
    nums = list(map(int, input().split()))
    print(sum(nums))   # 60
```

离开 `with` 块后 `sys.stdin` 自动恢复。

---

### `test(func_or_file, cases, *, strip=True, verbose=True, show_input=True, time_limit=None) -> bool`

批量测试函数或脚本文件，自动比对期望输出。

| 参数 | 类型 | 说明 |
|------|------|------|
| `func_or_file` | `Callable` 或路径 | 算法函数，或脚本文件路径 |
| `cases` | `list` | 测试用例列表（见下方格式说明） |
| `strip` | `bool` | 比较前去除首尾空白，默认 `True` |
| `verbose` | `bool` | 打印每个用例结果，默认 `True` |
| `show_input` | `bool` | 失败时显示输入内容，默认 `True` |
| `time_limit` | `float \| None` | 单个用例超时（秒），`None` 不限制 |

**用例格式：**

```python
cases = [
    ("5\n1 2 3 4 5", "15"),   # (input, expected)  →  比对输出
    ("0",            "0"),
    "10\n1 2 3 ...",           # 仅输入字符串       →  只运行，打印结果
]
```

**示例：**

```python
def solution():
    n = int(input())
    print(n * (n + 1) // 2)

test(solution, [
    ("5",  "15"),
    ("10", "55"),
    ("0",  "0"),
    ("100", "5050"),
])
```

输出示例：

```
Case 1/4  [PASS]  [0.1ms]
Case 2/4  [PASS]  [0.1ms]
Case 3/4  [PASS]  [0.0ms]
Case 4/4  [PASS]  [0.1ms]
----------------------------------------------------
Result: 4/4 passed
```

失败时显示输入 / 实际输出 / 期望输出三行对比。

返回值：所有有期望输出的用例全通过时返回 `True`，否则 `False`。

---

### `build_input(*lines) -> str`

把多行内容拼成换行分隔的输入字符串，每个元素可以是字符串、数字或可迭代对象（自动用空格连接）。

```python
s = build_input(
    5,
    [1, 2, 3, 4, 5],
    "query 1 3",
)
# 等价于 "5\n1 2 3 4 5\nquery 1 3\n"
```

---

## 常见模式速查

### `sys.stdin.read()` 一次性读取

```python
def solution():
    import sys
    data = sys.stdin.read().split()
    # ...

run(solution, "5\n1 2 3 4 5")
```

### `input()` 逐行读取

```python
def solution():
    n = int(input())
    for _ in range(n):
        a, b = map(int, input().split())
        print(a + b)

run(solution, "3\n1 2\n3 4\n5 6")
```

### 脚本文件内模块级绑定

```python
# solution.py
import sys
input = sys.stdin.readline   # 模块级绑定

def solve():
    n = int(input())
    ...

solve()
```

```python
# 正确做法：用 run_file 而非 run
output = run_file("solution.py", "5\n1 2 3 4 5")
```

### 多组输入压测

```python
import random
from ACM import run, build_input

def brute():
    n = int(input())
    print(sum(range(n + 1)))

def optimized():
    n = int(input())
    print(n * (n + 1) // 2)

for _ in range(1000):
    n = random.randint(0, 10000)
    inp = build_input(n)
    assert run(brute, inp) == run(optimized, inp)

print("随机对拍全部通过")
```

---

## 文件结构

```
ACM/
└── __init__.py    # 全部实现，直接 from ACM import ... 即可
```
