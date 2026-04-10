"""
ACM 算法本地调试接口

解决痛点：算法程序通常用 sys.stdin.read() / input() 读取控制台输入，
本地调试时需要反复手动粘贴样例。本模块把字符串作为 stdin 注入，
让调试像单元测试一样简洁。

用法速查
--------
from ACM import run, run_file, stdin_as, test

# 1. 运行函数
output = run(my_solution, "3\\n1 2 3")

# 2. 运行脚本文件
output = run_file("solution.py", "3\\n1 2 3")

# 3. 上下文管理器（直接写算法逻辑）
with stdin_as("3\\n1 2 3"):
    n = int(input())
    nums = list(map(int, input().split()))
    print(sum(nums))

# 4. 批量测试
test(my_solution, [
    ("3\\n1 2 3", "6"),
    ("5\\n1 2 3 4 5", "15"),
])
"""

import sys
import io
import runpy
import contextlib
import textwrap
import time
from pathlib import Path
from typing import Callable, Iterable, Optional, Sequence, Tuple, Union


# ── 核心工具 ────────────────────────────────────────────────────────────


def _make_stdin(input_str: str) -> io.StringIO:
    """把字符串包装为 stdin-compatible 对象"""
    buf = io.StringIO(input_str)
    # ACM 程序有时通过 sys.stdin.buffer 读取字节，提供一个简单的兼容层
    buf.buffer = io.BytesIO(input_str.encode())
    return buf


@contextlib.contextmanager
def stdin_as(input_str: str):
    """
    上下文管理器：在 with 块内将 sys.stdin 替换为 input_str。

    适合直接把算法逻辑写在 with 块里，无需封装成函数。

    示例
    ----
    with stdin_as("5\\n1 2 3 4 5"):
        n = int(input())
        nums = list(map(int, input().split()))
        print(sum(nums))
    """
    old_stdin = sys.stdin
    sys.stdin = _make_stdin(input_str)
    try:
        yield
    finally:
        sys.stdin = old_stdin


# ── 主 API ───────────────────────────────────────────────────────────────


def run(
    func: Callable,
    input_str: str = "",
    *,
    capture: bool = True,
    print_output: bool = False,
) -> str:
    """
    以 input_str 作为 stdin 运行 func()，返回捕获的 stdout 字符串。

    Parameters
    ----------
    func : Callable
        无参可调用对象（算法的入口函数）。
    input_str : str
        注入的输入字符串，行与行之间用 '\\n' 分隔。
    capture : bool
        True（默认）捕获 stdout 并返回；False 直接打印到控制台。
    print_output : bool
        True 时在捕获后额外打印到控制台，方便调试。

    Returns
    -------
    str
        函数运行期间写到 stdout 的全部内容。

    注意
    ----
    若算法在**模块级**绑定了 `input = sys.stdin.readline`（导入时执行），
    该绑定在 run() 之前已确定，不受本函数影响。
    此时请改用 run_file() 或将算法封装为函数后再绑定。

    示例
    ----
    def solution():
        import sys
        data = sys.stdin.read().split()
        n = int(data[0])
        print(sum(int(x) for x in data[1:n+1]))

    output = run(solution, "5\\n1 2 3 4 5")
    # output == "15\\n"
    """
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = _make_stdin(input_str)
    out_buf = io.StringIO() if capture else old_stdout
    sys.stdout = out_buf

    try:
        func()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

    result = out_buf.getvalue() if capture else ""
    if capture and print_output:
        print(result, end="")
    return result


def run_file(
    filepath: Union[str, Path],
    input_str: str = "",
    *,
    capture: bool = True,
    print_output: bool = False,
) -> str:
    """
    以 input_str 作为 stdin 运行指定 Python 脚本，返回其 stdout。

    使用 runpy.run_path 执行，脚本的 __name__ 被设为 '__main__'，
    因此 if __name__ == '__main__': 块会正常执行。

    Parameters
    ----------
    filepath : str | Path
        要运行的脚本路径（绝对或相对于当前工作目录）。
    input_str : str
        注入的输入字符串。
    capture : bool
        True 捕获并返回 stdout；False 直接打印。
    print_output : bool
        True 时捕获后额外打印到控制台。

    示例
    ----
    output = run_file("动态规划/solution.py", "5\\n1 2 3 4 5")
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"脚本不存在: {filepath}")

    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = _make_stdin(input_str)
    out_buf = io.StringIO() if capture else old_stdout
    sys.stdout = out_buf

    try:
        runpy.run_path(str(filepath), run_name="__main__")
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

    result = out_buf.getvalue() if capture else ""
    if capture and print_output:
        print(result, end="")
    return result


# ── 批量测试 ─────────────────────────────────────────────────────────────

# 单个测试用例：(输入, 期望输出) 或仅 输入（不校验）
Case = Union[
    Tuple[str, str],   # (input, expected)
    Tuple[str, None],  # (input,) 只运行不比较
    str,               # 仅输入
]


def test(
    func_or_file: Union[Callable, str, Path],
    cases: Sequence[Case],
    *,
    strip: bool = True,
    verbose: bool = True,
    show_input: bool = True,
    time_limit: Optional[float] = None,
) -> bool:
    """
    批量测试函数或脚本文件。

    Parameters
    ----------
    func_or_file : Callable | str | Path
        算法入口函数，或脚本文件路径。
    cases : list
        测试用例列表，每个元素为：
          - (input_str, expected_output)：运行并比较输出
          - input_str：仅运行并打印输出，不做比较
    strip : bool
        比较前去掉首尾空白（默认 True，容忍末尾换行差异）。
    verbose : bool
        True 时打印每个测试用例的详情。
    show_input : bool
        True 时失败时显示输入内容（方便大样例时关闭）。
    time_limit : float | None
        单个用例的超时时间（秒），None 表示不限制。

    Returns
    -------
    bool
        所有有期望输出的用例全部通过时返回 True。

    示例
    ----
    def solution():
        n = int(input())
        print(sum(range(n + 1)))

    test(solution, [
        ("5", "15"),
        ("10", "55"),
        ("0", "0"),
    ])
    """
    is_file = isinstance(func_or_file, (str, Path))
    runner = (lambda inp: run_file(func_or_file, inp)) if is_file else (
              lambda inp: run(func_or_file, inp))

    total = len(cases)
    passed = 0
    failed = 0
    no_expected = 0

    sep = "-" * 52

    for i, case in enumerate(cases, 1):
        if isinstance(case, str):
            input_str, expected = case, None
        elif isinstance(case, (tuple, list)):
            if len(case) == 1:
                input_str, expected = case[0], None
            else:
                input_str, expected = str(case[0]), case[1]
        else:
            input_str, expected = str(case), None

        t0 = time.perf_counter()
        actual = runner(input_str)
        elapsed = time.perf_counter() - t0

        time_str = f"{elapsed * 1000:.1f}ms"
        tl_warn = (time_limit is not None and elapsed > time_limit)

        if expected is None:
            no_expected += 1
            if verbose:
                print(f"Case {i}/{total}  [{time_str}]{'  [TLE]' if tl_warn else ''}")
                _show_io(input_str, actual, show_input)
            continue

        actual_cmp = actual.strip() if strip else actual
        expected_cmp = str(expected).strip() if strip else str(expected)
        ok = (actual_cmp == expected_cmp) and not tl_warn

        if ok:
            passed += 1
            if verbose:
                print(f"Case {i}/{total}  [PASS]  [{time_str}]")
        else:
            failed += 1
            if verbose:
                tag = "TLE" if tl_warn else "FAIL"
                print(f"Case {i}/{total}  [{tag}]  [{time_str}]")
                if show_input:
                    _show_io(input_str, actual, True)
                    print(f"  expected: {repr(expected_cmp)}")
                else:
                    print(f"  actual  : {repr(actual_cmp)}")
                    print(f"  expected: {repr(expected_cmp)}")

    if verbose:
        print(sep)
        checkable = total - no_expected
        summary = f"Result: {passed}/{checkable} passed"
        if failed:
            summary += f"  {failed} failed"
        if no_expected:
            summary += f"  {no_expected} run-only"
        print(summary)

    return failed == 0


def _show_io(input_str: str, actual: str, show_input: bool):
    if show_input:
        lines = input_str.splitlines()
        preview = "\n    ".join(lines[:6])
        if len(lines) > 6:
            preview += f"\n    ... ({len(lines)} lines total)"
        print(f"  input :\n    {preview}")
    print(f"  output: {repr(actual.rstrip())}")


# ── 便捷工具 ─────────────────────────────────────────────────────────────


def build_input(*lines: Union[str, Iterable]) -> str:
    """
    把多行内容拼成换行分隔的输入字符串，方便构造大样例。

    每个元素可以是字符串或可迭代对象（自动用空格连接）。

    示例
    ----
    s = build_input(
        5,
        [1, 2, 3, 4, 5],
        "query",
    )
    # "5\\n1 2 3 4 5\\nquery\\n"
    """
    parts = []
    for line in lines:
        if isinstance(line, (list, tuple)):
            parts.append(" ".join(str(x) for x in line))
        else:
            parts.append(str(line))
    return "\n".join(parts) + "\n"
