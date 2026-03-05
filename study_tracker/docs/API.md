# 学习进度追踪系统 - API 文档

## 模块结构

```
study_tracker/
├── tracker/
│   ├── __init__.py
│   └── file_tracker.py      # FileTracker 类
├── ui/
│   ├── __init__.py
│   ├── gui.py               # StudyTrackerGUI 类
│   ├── cli.py               # CLIInterface 类
│   └── study_log_window.py  # StudyLogWindow 类
└── main.py                  # 主入口
```

---

## tracker.file_tracker 模块

### FileTracker 类

文件追踪系统的核心类。

#### 初始化

```python
from tracker.file_tracker import FileTracker

tracker = FileTracker(root_dir, db_file=None)
```

参数：
- `root_dir` (str): 要追踪的根目录
- `db_file` (str, optional): 数据库文件路径，默认为 `root_dir/.study_tracker/database.json`

#### 方法

##### `scan_directory() -> Dict`

扫描目录并初始化所有文件的信息。

```python
result = tracker.scan_directory()
# {
#     "new_files": 10,
#     "updated_files": 5,
#     "total_files": 100,
#     "scanned_at": "2026-03-03T10:30:00"
# }
```

##### `record_update(file_path: str, notes: str = "") -> bool`

记录文件的手动更新（表示复习过该文件）。

```python
success = tracker.record_update("path/to/file.py", "复习了基本概念")
```

参数：
- `file_path`: 文件的相对路径
- `notes`: 可选的更新备注

返回值：`bool` - 操作是否成功

##### `update_file_status(file_path: str, status: str, notes: str = "") -> bool`

更新文件的学习状态。

```python
tracker.update_file_status("path/to/file.py", "已掌握", "完全理解了该部分")
```

参数：
- `file_path`: 文件的相对路径
- `status`: 状态字符串
- `notes`: 可选的备注

返回值：`bool` - 操作是否成功

##### `add_study_log(content: str, date: str = None) -> bool`

添加学习日志。

```python
tracker.add_study_log("今天学习了数据结构", "2026-03-03")
```

参数：
- `content`: 学习内容
- `date`: 日期（格式YYYY-MM-DD），默认为当前日期

返回值：`bool` - 操作是否成功

##### `get_study_logs(date: str = None) -> List[Dict]`

获取学习日志。

```python
logs = tracker.get_study_logs("2026-03-03")
# [
#     {
#         "date": "2026-03-03",
#         "content": "学习内容...",
#         "timestamp": 1704067200
#     }
# ]
```

参数：
- `date`: 特定日期（格式YYYY-MM-DD），为None时返回所有日志

返回值：日志列表

##### `get_file_age_days(file_path: str) -> Optional[float]`

获取文件距离最后修改的天数。

```python
age = tracker.get_file_age_days("path/to/file.py")
# 3.5
```

参数：
- `file_path`: 文件的相对路径

返回值：`float` 或 `None` - 天数或None（如果文件不存在）

##### `get_color_level(age_days: float) -> str`

根据天数确定颜色等级。

```python
color = tracker.get_color_level(5)
# 'red'
```

参数：
- `age_days`: 天数

返回值：`str` - 'green', 'yellow', 或 'red'

##### `get_file_list() -> List[Dict]`

获取所有活跃文件的列表（已按修改时间排序）。

```python
files = tracker.get_file_list()
# [
#     {
#         "path": "path/to/file1.py",
#         "age_days": 0.5,
#         "color": "green",
#         "status": "已学习",
#         "update_count": 3,
#         "created_at": "2026-03-01T10:00:00",
#         ...
#     }
# ]
```

返回值：文件信息字典列表

##### `get_statistics() -> Dict`

获取统计信息。

```python
stats = tracker.get_statistics()
# {
#     "total_files": 100,
#     "active_files": 98,
#     "recent_updates": 5,
#     "by_age_range": {
#         "0_1days": 5,
#         "1_3days": 3,
#         "3_7days": 10,
#         "7_14days": 8,
#         "14_30days": 15,
#         "30+days": 52
#     }
# }
```

返回值：统计信息字典

##### `_load_database() -> Dict`

加载数据库（内部方法）。

##### `_save_database()`

保存数据库（内部方法）。

#### 属性

- `root_dir` (Path): 根目录
- `db_file` (Path): 数据库文件路径
- `data` (Dict): 内存中的数据库

---

## ui.gui 模块

### StudyTrackerGUI 类

GUI 主窗口类。

#### 初始化

```python
from ui.gui import StudyTrackerGUI

app = StudyTrackerGUI(root_dir)
app.run()
```

参数：
- `root_dir`: 根目录路径

#### 主要方法

##### `run()`

启动 GUI 应用。

```python
app.run()
```

##### `_scan_directory()`

扫描目录（GUI 回调）。

##### `_refresh_data()`

刷新数据显示。

##### `_update_file_list()`

更新文件列表显示。

##### `_open_study_log()`

打开学习日志窗口。

##### `_export_report()`

导出学习进度报告。

#### 属性

- `window` (tk.Tk): 主窗口
- `tracker` (FileTracker): 追踪器实例
- `tree` (ttk.Treeview): 文件树形视图
- `colors` (Dict): 颜色定义

---

## ui.study_log_window 模块

### StudyLogWindow 类

学习日志子窗口类。

#### 初始化

```python
from ui.study_log_window import StudyLogWindow

log_window = StudyLogWindow(parent_window, tracker)
```

参数：
- `parent`: 父窗口
- `tracker`: FileTracker 实例

#### 主要方法

##### `_save_log()`

保存当前输入的日志。

##### `_load_logs_by_date()`

按日期加载日志。

##### `_load_today_logs()`

加载今天的日志。

#### 属性

- `window` (tk.Toplevel): 子窗口
- `tracker` (FileTracker): 追踪器实例
- `input_text` (tk.Text): 日志输入框
- `history_text` (tk.Text): 日志历史显示

---

## ui.cli 模块

### CLIInterface 类

命令行接口类。

#### 初始化

```python
from ui.cli import CLIInterface

cli = CLIInterface(root_dir)
```

参数：
- `root_dir`: 根目录路径

#### 方法

##### `scan()`

扫描目录。

```python
cli.scan()
```

##### `status()`

显示学习状态统计。

```python
cli.status()
```

##### `list_files(filter_status=None, limit=50)`

列出文件。

```python
cli.list_files()
cli.list_files(filter_status="已学习", limit=20)
```

##### `list_urgent()`

列出需要复习的文件。

```python
cli.list_urgent()
```

##### `update(file_path)`

更新文件时间戳。

```python
cli.update("path/to/file.py")
```

##### `mark_studied(file_path)`

标记为已学习。

```python
cli.mark_studied("path/to/file.py")
```

##### `mark_mastered(file_path)`

标记为已掌握。

```python
cli.mark_mastered("path/to/file.py")
```

##### `export_report()`

导出学习进度报告。

```python
cli.export_report()
```

---

## 使用示例

### 完整工作流示例

```python
from tracker.file_tracker import FileTracker
from pathlib import Path

# 初始化追踪器
root_dir = r"G:\AlgorithmLearning\系统性算法知识"
tracker = FileTracker(root_dir)

# 第一次使用：扫描目录
result = tracker.scan_directory()
print(f"新文件: {result['new_files']}, 总文件: {result['total_files']}")

# 获取统计信息
stats = tracker.get_statistics()
print(f"需要复习的: {stats['by_age_range']['3_7days'] + stats['by_age_range']['7_14days'] + stats['by_age_range']['14_30days']}")

# 获取文件列表
files = tracker.get_file_list()
for f in files[:5]:
    print(f"{f['path']}: {f['age_days']:.1f} 天, 状态: {f['status']}")

# 手动更新文件
tracker.record_update("path/to/file.py", "复习了基本概念")

# 标记为已掌握
tracker.update_file_status("path/to/file.py", "已掌握")

# 添加学习日志
tracker.add_study_log("今天完成了数据结构的学习", "2026-03-03")

# 查看日志
logs = tracker.get_study_logs("2026-03-03")
for log in logs:
    print(f"{log['date']}: {log['content']}")
```

### 获取需要复习的文件

```python
files = tracker.get_file_list()
urgent_files = [f for f in files if f['color'] == 'red']

for f in urgent_files:
    print(f"{f['path']} - {f['age_days']:.1f} 天未复习")
```

### 批量更新文件状态

```python
file_paths = [
    "基础算法/枚举算法/两数之和.py",
    "基础算法/枚举算法/三数之和.py"
]

for path in file_paths:
    tracker.record_update(path, "集中复习")
```

---

## 数据格式规范

### 时间格式

- **ISO8601**: `2026-03-03T10:30:45.123456`
- **日期**: `YYYY-MM-DD` 格式（如 `2026-03-03`）
- **Unix 时间戳**: 秒数整数

### 路径格式

- 使用相对路径（相对于根目录）
- 使用正斜杠 `/` 作为路径分隔符（系统会自动处理）

### 状态字符串

预定义状态：
- `"新建"` - 新文件
- `"已学习"` - 初步学过
- `"已掌握"` - 充分掌握
- `"已删除"` - 文件已删除

自定义状态：任意字符串

---

## 常见问题

### Q: 如何访问原始数据？
A: 通过 `tracker.data` 属性访问内存中的数据库：

```python
all_files = tracker.data["files"]
all_logs = tracker.data.get("study_logs", [])
```

### Q: 如何批量操作？
A: 获取文件列表后循环处理：

```python
for f in tracker.get_file_list():
    if f['age_days'] > 7:
        tracker.record_update(f['path'])
```

### Q: 如何导出数据？
A: 复制数据库文件或使用 JSON 序列化：

```python
import json
with open('.study_tracker/database.json', 'w') as f:
    json.dump(tracker.data, f, ensure_ascii=False, indent=2)
```

### Q: 如何恢复数据？
A: 替换数据库文件后重新初始化：

```python
# 用备份文件替换 .study_tracker/database.json
tracker = FileTracker(root_dir)
```
