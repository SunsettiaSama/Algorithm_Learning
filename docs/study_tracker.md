# Study Tracker 学习进度追踪系统

> 路径：`study_tracker/`
> 入口：`run_study_tracker.py`

## 概述

Study Tracker 是一个面向算法学习者的**本地文件学习进度追踪工具**，核心功能：

- 自动扫描目录，记录所有算法文件的元数据
- 基于**艾宾浩斯遗忘曲线**计算每个文件的复习紧急度（权重分数）
- 图形界面展示复习推荐列表、文件详情、阶段完成情况
- 支持"温启动/冷启动"重置复习计划
- 提供 CLI 命令行接口

---

## 目录结构

```
study_tracker/
├── run_study_tracker.py        # 启动脚本
├── main.py                     # 主入口
├── config/
│   ├── settings.py             # 配置管理（颜色、阈值等）
│   └── settings.json           # 持久化配置（自动生成）
├── tracker/
│   └── file_tracker.py         # 核心追踪逻辑 + 艾宾浩斯算法
└── ui/
    ├── gui.py                  # Tkinter 图形界面
    ├── cli.py                  # 命令行接口
    └── settings_window.py      # 设置窗口
```

数据文件（自动生成，存于 `.study_tracker/`）：

```
.study_tracker/
├── database.json       # 所有文件的元数据 + 复习记录
├── .studyignore        # 忽略规则（类似 .gitignore）
└── report.txt          # 导出的文字报告
```

---

## 启动方式

### 图形界面（GUI）

```bash
python run_study_tracker.py
# 或
python -m study_tracker
```

### 命令行（CLI）

```bash
python -m study_tracker.ui.cli --root . scan         # 扫描目录
python -m study_tracker.ui.cli --root . status       # 查看统计
python -m study_tracker.ui.cli --root . list         # 列出所有文件
python -m study_tracker.ui.cli --root . urgent       # 列出需要复习的文件
python -m study_tracker.ui.cli --root . update "算法/solution.py"
python -m study_tracker.ui.cli --root . mark-studied "算法/solution.py"
python -m study_tracker.ui.cli --root . mark-mastered "算法/solution.py"
python -m study_tracker.ui.cli --root . ignore "*.tmp"
python -m study_tracker.ui.cli --root . export
```

---

## 艾宾浩斯遗忘曲线算法

### 阶段定义

从**首次学习时间**（`first_study_timestamp`）起，定义 5 个固定复习窗口：

| 阶段 | 时间窗口 | 紧急度分数 |
|------|---------|-----------|
| `1d` | 0 ~ 1 天 | 20 |
| `3d` | 1 ~ 3 天 | 40 |
| `7d` | 3 ~ 7 天 | 60 |
| `14d` | 7 ~ 14 天 | 80 |
| `30d` | 14 ~ 30 天 | 100 |

**核心原则**：阶段内任意时刻复习 = 该阶段完成，阶段等价。
只看"当前应完成阶段有没有做"，不计复习次数。

### 权重计算公式

```
1. 当前阶段已完成  →  权重 = 0（不需要复习）

2. 当前阶段未完成：
   base         = 阶段紧急度 × 重要程度系数
   missed_prior = 当前阶段之前，有几个历史阶段也未完成
   退化倍率     = 1.0 + 0.25 × missed_prior
   权重         = min(150, base × 退化倍率)
```

**重要程度系数**：

| 标记 | 系数 |
|------|------|
| 普通（☆） | × 1.0 |
| 重点（★） | × 1.5 |

**退化机制**：每跳过一个历史阶段，掌握度退化 25%。
最多 4 个历史阶段（退化倍率最高 × 2.0），权重上限 150 分。

### 权重示例

| 场景 | 距今天数 | 当前阶段 | 已完成情况 | 权重（普通） |
|------|---------|---------|-----------|------------|
| 第 2 天已复习 | 2 天 | 3d | 1d✓ 3d✓ | 0（阶段完成） |
| 第 5 天忘记复习 | 5 天 | 7d | 1d✓ 3d✓ 7d✗ | 60 |
| 第 10 天，从未复习 | 10 天 | 14d | 全✗ | 80 × (1+0.25×3) = 140 |
| 重点文件，第 20 天忘记 | 20 天 | 30d | 1d✓ 其余✗ | min(150, 100×1.5×(1+0.75)) = 150 |

### 阶段完成判定

文件每次被修改（磁盘 mtime 变化 或 手动点击"更新"），系统自动：

1. 计算 `days = (当前时间 - first_study_timestamp) / 86400`
2. 映射到对应阶段窗口
3. 将该阶段 `stage_done[stage_name] = True`
4. 写入一条 `review_records` 复习记录

### 历史数据回溯

首次启动时，系统会对已有文件的 `update_timestamps` 做一次性回溯（`_migrated_stage_backfill`），
将历史更新时间点映射到对应阶段并标记完成，确保旧文件不会显示错误的权重。

---

## 颜色等级

| 权重分数 | 颜色 | 状态 |
|---------|------|------|
| < 1 | 白色 | 不需要复习 |
| 1 ~ 40 | 浅黄 | 需要复习 |
| 40 ~ 60 | 橙色 | 重点复习 |
| 60 ~ 80 | 番茄红 | 警告级 |
| 80 ~ 100 | 深红 | 紧急复习 |
| ≥ 100 | 暗红 | 已遗忘 |

颜色阈值可在"设置"窗口中调整（`score_thresholds`）。

---

## 图形界面（GUI）说明

### 布局

```
┌─────────────────────────────────────────────────────────────┐
│ [扫描目录] [刷新数据] [导出报告] [紧急复习] [设置]           │
├────────────────────────────────────┬────────────────────────┤
│ 文件列表（左侧）                    │ 复习推荐 Top 10（右上） │
│                                    ├────────────────────────┤
│ 重要 | 权重 | 更新次数 | 状态       │ 文件详情（右下）        │
│                                    │                        │
└────────────────────────────────────┴────────────────────────┘
```

### 文件列表列说明

| 列 | 说明 |
|----|------|
| 文件名 | 点击查看详情；双击直接用系统程序打开文件 |
| 重要（★/☆） | 点击直接切换重要程度；或右键菜单切换 |
| 权重 | 艾宾浩斯权重分数（0 = 无需复习） |
| 更新次数 | 文件被修改/手动更新的次数（即复习次数） |
| 状态 | 新建 / 已学习 / 已掌握 / 已删除 |

列表按**权重降序**排列（越高越紧急越靠前）。
目录节点颜色反映子文件的整体紧急度。

### 右侧面板

#### 复习推荐 Top 10（始终可见）

- 展示当前权重最高的 10 个文件
- 点击条目 → 在下方详情面板显示该文件元数据
- 双击条目 → 用系统程序直接打开文件

#### 文件详情（选中文件后显示）

显示内容：

```
路径 / 大小
创建时间 | 首次追踪时间（距今 X 天）
最后修改时间（距今 X 天）
复习次数 | 状态 | 重要程度
权重分数 | 颜色等级
艾宾浩斯当前阶段 | 各阶段完成情况（1d✓ 3d✗ …）
最近 8 条更新记录
```

操作按钮：**标记为已学 / 标记为已掌握 / 更新 / 切换重要程度 / 清除选择**

下方为**笔记区**（可编辑保存）。

### 右键菜单

在文件树中右键任意文件，弹出：

| 菜单项 | 功能 |
|--------|------|
| 标记为重点 ★ / 取消重点 ☆ | 切换重要程度 |
| 查看复习详情... | 弹出完整复习历史与权重计算过程 |
| 接续进度复习（温启动） | 从最后完成的阶段续接，调整时间线 |
| 从头重新开始（冷启动） | 完全重置复习计划 |
| 忽略此目录 | 添加到 `.studyignore` |

### 复习详情弹窗

右键 → "查看复习详情" 弹出独立窗口，包含三个区块：

1. **权重计算过程**：逐步展示阶段、已完成情况、退化倍率、最终权重
2. **阶段完成汇总**：5 个阶段的 ✓/✗ 状态
3. **复习历史**：每条记录含时间、类型（`file_modified` / `manual_update` / `warm_resume` / `cold_restart`）、距上次间隔天数、备注

---

## 复习计划重启

### 冷启动（从头重新开始）

适用场景：完全忘记，需要重新学习。

- `first_study_timestamp` 重置为现在
- 所有阶段清零
- 本次操作视为完成 `1d` 阶段（权重 = 0）
- 明天起进入 `3d` 阶段

### 温启动（接续进度）

适用场景：隔了较长时间，但之前有一定基础，不想从零开始。

算法：

1. 找到历史上最后一个已完成的阶段 k
2. 若无已完成阶段 或 `30d` 已完成 → 自动降级为冷启动
3. 否则：
   - 把 `first_study_timestamp` 调整到"现在处于第 k+1 阶段中间点"
   - 标记第 k+1 阶段完成（本次复习）
   - 保留 k 之前的阶段完成状态
   - 重置 k+1 之后的阶段为未完成

| 历史状态 | 续接点 | 本次完成 | 下次提醒 |
|---------|-------|---------|--------|
| 1d✓ 3d✗ … | 从 1d 续 | 3d | 3~7 天后（7d 窗口）|
| 1d✓ 3d✓ 7d✗ … | 从 3d 续 | 7d | 7~14 天后（14d 窗口）|
| 1d✓ 3d✓ 7d✓ 14d✗ … | 从 7d 续 | 14d | 14~30 天后（30d 窗口）|

---

## 文件元数据字段

`database.json` 中每个文件条目包含：

| 字段 | 说明 |
|------|------|
| `path` | 相对于追踪根目录的路径 |
| `created_at` | 磁盘文件创建时间（ISO 格式） |
| `created_timestamp` | 创建时间戳 |
| `first_study_timestamp` | 首次追踪时间（艾宾浩斯起点） |
| `last_modified` | 最后修改时间（ISO 格式） |
| `last_modified_timestamp` | 最后修改时间戳 |
| `update_count` | 修改次数（即复习次数） |
| `update_timestamps` | 每次修改的时间戳列表 |
| `file_size` | 文件大小（字节） |
| `status` | 新建 / 已学习 / 已掌握 / 已删除 |
| `notes` | 用户笔记 |
| `is_important` | 重要程度：`"普通"` 或 `"重点"` |
| `stage_done` | 各阶段完成情况：`{"1d": bool, "3d": bool, ...}` |

复习记录（`review_records`）：

| 字段 | 说明 |
|------|------|
| `file_path` | 文件路径 |
| `review_type` | `file_modified` / `manual_update` / `warm_resume` / `cold_restart` / `status_change` |
| `timestamp` | 时间戳 |
| `datetime` | ISO 格式时间 |
| `notes` | 备注 |
| `update_count` | 当时的累计更新次数 |

---

## 配置说明（settings.json）

位于 `study_tracker/config/settings.json`，支持通过 GUI 设置窗口修改。

### 权重分数阈值（`score_thresholds`）

| 键 | 默认值 | 说明 |
|----|--------|------|
| `fresh_max` | 1 | 低于此值 → 白色（无需复习） |
| `early_max` | 40 | 低于此值 → 浅黄（需要复习） |
| `normal_max` | 60 | 低于此值 → 橙色（重点复习） |
| `warning_max` | 80 | 低于此值 → 番茄红（警告） |
| `critical_max` | 100 | 低于此值 → 深红（紧急复习） |
| ≥ `critical_max` | — | 暗红（已遗忘） |

### 忽略规则（`.study_tracker/.studyignore`）

语法同 `.gitignore`，默认忽略：

```
node_modules/  dist/  build/  .venv/  venv/
*.log  *.tmp  *.cache  *.bak
*.pyc  __pycache__  .git  .study_tracker
```

---

## 核心模块接口（`FileTracker`）

```python
from study_tracker.tracker.file_tracker import FileTracker

tracker = FileTracker(root_dir)
```

| 方法 | 说明 |
|------|------|
| `scan_directory()` | 扫描目录，自动完成新文件的阶段标记 |
| `compute_weight_score(path)` | 计算权重分数（含退化机制） |
| `get_weight_breakdown(path)` | 返回权重计算详情字典，供 UI 展示 |
| `get_color_segment(path)` | 返回颜色等级字符串（fresh/early/normal/warning/critical/overdue） |
| `get_urgent_files()` | 返回权重 > 0 的文件列表，按分数降序 |
| `get_file_list()` | 返回所有活跃文件，含权重、颜色等信息 |
| `get_statistics()` | 返回统计信息（总数、各区间分布等） |
| `record_update(path, notes)` | 手动记录一次复习，自动标记当前阶段完成 |
| `mark_important(path, importance)` | 切换重要程度（`"普通"` / `"重点"`） |
| `cold_restart(path)` | 冷启动：完全重置艾宾浩斯计划 |
| `warm_resume(path)` | 温启动：从最后完成阶段续接 |
| `get_review_records(path)` | 获取该文件的复习记录列表 |
| `update_file_status(path, status)` | 更新文件状态 |
| `add_ignore_pattern(pattern)` | 添加忽略规则 |
