# 功能详细说明

这个文档详细介绍学习进度追踪系统的所有功能、项目结构和实现细节。

## 目录

1. [项目结构](#项目结构)
2. [核心功能](#核心功能)
3. [工作流程](#工作流程)
4. [使用示例](#使用示例)
5. [进阶功能](#进阶功能)

---

## 项目结构

### 完整项目布局

```
study_tracker/
├── tracker/                      # 核心追踪模块
│   ├── __init__.py
│   └── file_tracker.py          # FileTracker 类（核心）
│
├── ui/                           # 用户界面模块
│   ├── __init__.py
│   ├── gui.py                   # StudyTrackerGUI 类
│   ├── cli.py                   # CLIInterface 类
│   └── study_log_window.py      # StudyLogWindow 类
│
├── docs/                         # 文档目录
│   ├── README.md                # 简介（你在这里）
│   ├── QUICK_START.md           # 快速开始
│   ├── FEATURES.md              # 本文件
│   └── API.md                   # API 文档
│
├── main.py                       # 主入口脚本
│
└── .study_tracker/              # 数据存储目录（自动创建）
    ├── database.json            # 数据库
    ├── .studyignore             # 忽略配置
    └── report.txt               # 导出报告
```

### 模块说明

| 模块 | 位置 | 职责 |
|------|------|------|
| FileTracker | `tracker/file_tracker.py` | 文件扫描、追踪、状态管理 |
| GUI | `ui/gui.py` | 图形用户界面（Tkinter） |
| CLI | `ui/cli.py` | 命令行接口 |
| StudyLogWindow | `ui/study_log_window.py` | 学习日志子窗口 |

---

## 核心功能

### 1. 文件追踪系统 (FileTracker)

#### 功能概述

自动扫描和监控指定目录的所有文件，记录元数据和修改历史。

#### 主要方法

##### `scan_directory() -> Dict`

扫描目录，初始化或更新所有文件信息。

```python
result = tracker.scan_directory()
# 返回：
# {
#     "new_files": 5,              # 新发现的文件
#     "updated_files": 3,          # 已修改的文件
#     "total_files": 100,          # 总文件数
#     "scanned_at": "2026-03-03T10:30:00"
# }
```

**工作流程：**
1. 遍历目录树
2. 对于每个文件，检查是否在数据库中
3. 新文件：添加到数据库
4. 已修改文件：更新修改时间
5. 已删除文件：标记为"已删除"状态

##### `record_update(file_path: str, notes: str = "")`

记录对文件的手动更新（表示已复习）。

```python
tracker.record_update("算法/动态规划.py", "复习了状态转移方程")
```

**作用：**
- 更新文件的最后修改时间为当前时间
- 增加更新计数
- 记录更新备注
- 文件颜色将变为绿色

##### `update_file_status(file_path: str, status: str, notes: str = "")`

更新文件的学习状态。

```python
tracker.update_file_status("算法/排序.py", "已掌握", "掌握了所有排序算法")
tracker.update_file_status("算法/查找.py", "已学习", "学习了二分查找")
```

**状态类型：**
- `"新建"` - 新增的文件
- `"已学习"` - 初步学过
- `"已掌握"` - 充分掌握
- `"复习中"` - 正在复习
- 自定义状态 - 任意自定义字符串

##### `get_file_list() -> List[Dict]`

获取所有活跃文件的列表。

```python
files = tracker.get_file_list()
# 返回列表，每个元素包含：
# {
#     "path": "relative/path/file.py",
#     "age_days": 5.2,                # 距离上次修改的天数
#     "color": "red",                 # 标记颜色：green/yellow/red
#     "status": "已学习",              # 学习状态
#     "update_count": 3,              # 更新次数
#     "created_at": "ISO8601时间",
#     "last_modified": "ISO8601时间",
#     "file_size": 1024               # 文件大小
# }
```

##### `get_urgent_files() -> List[Dict]`

获取需要紧急复习的文件（3-30天内未更新）。

```python
urgent = tracker.get_urgent_files()
# 返回需要紧急复习的文件列表，按age_days倒序排列
```

##### `get_statistics() -> Dict`

获取统计信息。

```python
stats = tracker.get_statistics()
# 返回：
# {
#     "total_files": 100,
#     "active_files": 95,
#     "recent_updates": 5,            # 1天内更新的文件
#     "urgent_count": 15,             # 需要复习的文件
#     "by_age_range": {
#         "0_1days": 5,
#         "1_3days": 3,
#         "3_7days": 10,
#         "7_14days": 8,
#         "14_30days": 15,
#         "30+days": 54
#     }
# }
```

### 2. 智能颜色标记系统

#### 颜色规则

系统根据文件距离最后修改的天数自动标记：

| 天数 | 颜色 | 含义 | 操作 |
|------|------|------|------|
| < 1天 | 🟢 绿色 | 刚更新，不需要复习 | 继续学习 |
| 1-3天 | 🟡 黄色 | 逐渐需要复习 | 开始准备 |
| 3-7天 | 🔴 红色 | 需要紧急复习 | 立即复习 |
| 7-14天 | 🔴 红色 | 长时间未复习 | 必须复习 |
| 14-30天 | 🔴 红色 | 严重不足 | 优先复习 |
| > 30天 | 🟢 绿色 | 已基础稳定 | 偶尔复习 |

#### 实现原理

```python
def get_color_level(age_days: float) -> str:
    """根据天数返回颜色"""
    if age_days < 1 or age_days > 30:
        return "green"
    elif age_days < 3:
        return "yellow"
    else:
        return "red"
```

### 3. 学习日志功能

#### 功能概述

每日记录学习内容，形成学习日志库。

#### 主要方法

##### `add_study_log(content: str, date: str = None) -> bool`

添加学习日志。

```python
tracker.add_study_log("今天学习了动态规划的状态转移", "2026-03-03")
tracker.add_study_log("复习了排序算法的实现细节")  # 默认今天
```

##### `get_study_logs(date: str = None) -> List[Dict]`

获取学习日志。

```python
# 获取特定日期的日志
logs = tracker.get_study_logs("2026-03-03")

# 获取所有日志
all_logs = tracker.get_study_logs()
```

#### 日志数据结构

```json
{
  "study_logs": [
    {
      "date": "2026-03-03",
      "content": "学习了动态规划的状态转移方程",
      "timestamp": 1704067200
    }
  ]
}
```

### 4. 忽略模式配置 (.studyignore)

#### 功能概述

支持类似 `.gitignore` 的语法，忽略不需要追踪的文件和目录。

#### 配置方式

**方式1：编辑 .studyignore 文件**

在 `.study_tracker/.studyignore` 中添加：

```
# 注释行以 # 开头
node_modules/
dist/
build/
*.log
*.tmp
*.cache
__pycache__/
.venv/
```

**方式2：CLI 命令**

```bash
python main.py --cli ignore "*.tmp"
python main.py --cli ignore "node_modules/"
```

**方式3：GUI 右键菜单**

在文件树中右键点击目录 → "忽略此目录"

#### 默认忽略模式

以下内容默认被忽略：
- `.study_tracker` - 追踪系统自己的目录
- `.git` - Git版本控制目录
- `__pycache__` - Python缓存目录
- `*.pyc` - Python编译文件
- `.pytest_cache` - 测试缓存
- 所有以 `.` 开头的隐藏文件/目录

### 5. GUI 图形界面

#### 主要组件

##### 1. 控制栏
- **扫描目录** - 初始化文件信息
- **刷新数据** - 重新加载数据
- **导出报告** - 生成学习进度报告
- **学习日志** - 打开日志窗口
- **紧急复习** - 查看需要复习的文件

##### 2. 统计信息面板
显示：
- 总文件数
- 活跃文件数
- 最近更新的文件数
- 需要复习的文件数

##### 3. 文件列表（树形视图）
- 按目录分组组织
- 颜色标记（绿/黄/红）
- 显示天数、更新次数、状态
- 搜索和过滤功能

##### 4. 文件详情面板
显示选中文件的：
- 元数据（创建时间、大小、路径等）
- 更新历史（最近10次）
- 学习笔记编辑区

##### 5. 学习日志窗口
- 日期选择
- 内容输入和编辑
- 历史日志浏览
- 时间戳记录

#### 使用场景

**场景1：初始化**
```
启动 GUI → 点击"扫描目录" → 等待扫描完成 → 查看文件列表
```

**场景2：日常复习**
```
查看红色文件 → 双击打开 → 复习内容 → 点击"更新" → 颜色变绿
```

**场景3：记录学习**
```
点击"学习日志" → 输入内容 → 保存 → 可查询历史
```

### 6. CLI 命令行界面

#### 支持的命令

```bash
python main.py --cli <command> [arguments]
```

| 命令 | 功能 | 示例 |
|------|------|------|
| scan | 扫描目录 | `python main.py --cli scan` |
| status | 查看学习状态 | `python main.py --cli status` |
| list | 列出所有文件 | `python main.py --cli list` |
| urgent | 列出需要复习的文件 | `python main.py --cli urgent` |
| update | 更新文件时间戳 | `python main.py --cli update "file.py"` |
| mark-studied | 标记为已学习 | `python main.py --cli mark-studied "file.py"` |
| mark-mastered | 标记为已掌握 | `python main.py --cli mark-mastered "file.py"` |
| ignore | 添加忽略模式 | `python main.py --cli ignore "*.tmp"` |
| export | 导出报告 | `python main.py --cli export` |

### 7. 数据库和导出

#### 数据库格式

所有数据存储在 `.study_tracker/database.json`：

```json
{
  "version": "1.0",
  "created_at": "2026-03-01T10:00:00",
  "last_updated": "2026-03-03T15:30:00",
  "files": {
    "路径/文件.py": {
      "path": "路径/文件.py",
      "created_at": "2026-03-01T10:00:00",
      "last_modified": "2026-03-03T15:30:00",
      "update_count": 5,
      "update_timestamps": [1704067200, 1704153600],
      "file_size": 1024,
      "status": "已学习",
      "notes": "学习笔记内容"
    }
  },
  "study_logs": [
    {
      "date": "2026-03-03",
      "content": "今天学习了数据结构",
      "timestamp": 1704067200
    }
  ]
}
```

#### 导出报告

点击"导出报告"生成 `.study_tracker/report.txt`：
- 生成时间
- 统计信息汇总
- 时间分布统计
- 所有文件的详细列表

---

## 工作流程

### 初始化流程

```
启动应用
    ↓
扫描目录（或使用CLI: python main.py --cli scan）
    ↓
创建/更新 .study_tracker/database.json
    ↓
初始化所有文件信息
    ↓
显示在 GUI 文件列表中
```

### 日常学习流程

```
查看文件列表
    ↓
识别红色文件（需要复习）
    ↓
双击打开文件详情
    ↓
打开原始文件进行复习
    ↓
复习完成后点击"更新"刷新时间戳
    ↓
文件颜色变为绿色（恢复正常）
    ↓
打开学习日志记录学习内容
```

### 周期性管理流程

```
每周：查看统计信息
    ↓
对比上周的学习进度
    ↓
制定复习计划
    ↓
按计划更新文件状态

每月：导出报告
    ↓
分析学习效果
    ↓
调整学习策略
```

---

## 使用示例

### 示例1：快速复习工作流

```bash
# 1. 查看需要复习的文件
python main.py --cli urgent

# 2. 启动 GUI
python main.py

# 3. 选择红色文件并打开
# 4. 复习完成后点击"更新"

# 5. 记录学习日志
# 点击"学习日志"按钮 → 记录内容
```

### 示例2：编程集成

```python
from tracker.file_tracker import FileTracker

# 初始化追踪器
tracker = FileTracker("/path/to/study/files")

# 扫描目录
result = tracker.scan_directory()
print(f"发现 {result['new_files']} 个新文件")

# 获取统计信息
stats = tracker.get_statistics()
print(f"需要复习的文件：{stats['urgent_count']} 个")

# 获取需要复习的文件
urgent_files = tracker.get_urgent_files()
for file in urgent_files:
    print(f"{file['path']}: {file['age_days']:.1f} 天未更新")

# 记录复习
tracker.record_update("算法/动态规划.py", "复习了状态转移")

# 标记学习状态
tracker.update_file_status("算法/排序.py", "已掌握")

# 记录学习日志
tracker.add_study_log("今天学习了排序算法")

# 获取日志
logs = tracker.get_study_logs()
```

### 示例3：自定义忽略规则

```python
# 添加忽略模式
tracker.add_ignore_pattern("*.tmp")
tracker.add_ignore_pattern("__pycache__/")
tracker.add_ignore_pattern("test_*.py")

# 重新扫描应用忽略规则
tracker.scan_directory()
```

---

## 进阶功能

### 自定义文件状态

系统支持任意自定义状态，不仅限于"已学习"和"已掌握"：

```python
tracker.update_file_status("file.py", "深度掌握")
tracker.update_file_status("file.py", "做题中")
tracker.update_file_status("file.py", "待复习")
tracker.update_file_status("file.py", "困难")
```

### 批量操作

```python
# 获取所有文件
files = tracker.get_file_list()

# 批量更新某些文件
for file in files:
    if "算法" in file['path']:
        tracker.record_update(file['path'])
```

### 性能考虑

- **大目录扫描**：首次扫描大目录（>10000文件）可能需要几秒钟
- **数据库大小**：取决于文件数量，通常为KB到MB级别
- **搜索性能**：GUI搜索是实时的，查询速度很快
- **导出性能**：导出报告通常在几秒内完成

---

## 常见问题

### Q: 文件被删除后会发生什么？
A: 文件将标记为"已删除"状态，但历史记录会保留。如果文件重新出现，会自动恢复。

### Q: 如何修改颜色标记的时间阈值？
A: 编辑 `tracker/file_tracker.py` 中的 `get_color_level()` 方法。

### Q: 能否导出特定格式的报告？
A: 当前支持纯文本格式。数据库是JSON格式，可以自定义处理。

### Q: 支持网络驱动器或云同步吗？
A: 支持任何本地可访问的路径，包括映射的网络驱动器。

---

## 总结

学习进度追踪系统提供了完整的学习文件管理解决方案，包括：

✅ **自动化追踪** - 无需手动记录，自动追踪所有文件变化
✅ **智能提醒** - 通过颜色标记快速识别需要复习的内容
✅ **学习日志** - 记录学习过程，便于总结和反思
✅ **灵活配置** - 支持忽略规则、自定义状态等高级功能
✅ **多种界面** - 支持GUI和CLI两种操作方式

无论你是在学习算法、复习知识，还是管理长期学习项目，这个系统都能帮助你保持学习进度、避免遗忘。
