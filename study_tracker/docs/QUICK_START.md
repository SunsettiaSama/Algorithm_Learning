# 快速开始指南

## 5分钟快速上手

### 安装与启动

#### 1. 进入项目目录

```bash
cd g:\AlgorithmLearning\BaseAlgorithmLearning\study_tracker
```

#### 2. 启动应用

**GUI 模式（推荐）**
```bash
python main.py
```

**CLI 模式**
```bash
python main.py --cli <command>
```

---

## 常用操作

### 操作1：初始化扫描（第一次使用）

1. 启动 GUI：`python main.py`
2. 点击 **"扫描目录"** 按钮
3. 等待扫描完成，系统会显示找到的文件数量
4. 刷新后即可看到文件列表

### 操作2：查看学习进度

在 GUI 主窗口查看：
- **统计信息** - 顶部显示总文件数、活跃文件数、需要复习的文件数
- **文件颜色** - 根据颜色快速判断需要复习的内容
  - 🟢 绿色：不需要复习
  - 🟡 黄色：逐渐需要复习
  - 🔴 红色：需要紧急复习

### 操作3：复习文件后更新状态

1. 看到红色文件（需要复习）
2. 双击打开文件详情
3. 复习完成后点击 **"更新"** 刷新时间戳
4. 文件颜色变回绿色

### 操作4：记录学习日志

1. 点击 **"学习日志"** 按钮
2. 输入今天学习的内容
3. 点击 **"保存"** 或按 `Ctrl+Enter`
4. 日志自动保存到系统数据库

### 操作5：标记学习状态

在文件详情窗口可以标记：
- **"标记为已学习"** - 表示初步学过了
- **"标记为已掌握"** - 表示充分掌握了

---

## 文件颜色说明

| 颜色 | 含义 | 天数 | 操作建议 |
|------|------|------|--------|
| 🟢 绿色 | 不需要复习 | < 1天或 > 30天 | 保持学习进度 |
| 🟡 黄色 | 逐渐需要复习 | 1-3天 | 开始准备复习 |
| 🔴 红色 | 需要紧急复习 | 3-30天 | 立即复习 |

---

## 日常工作流程

### 早上：检查学习进度

```bash
# 方式1：GUI 界面
python main.py
# 查看统计信息面板的"待复习"数量

# 方式2：CLI 命令
python main.py --cli status      # 查看状态
python main.py --cli urgent      # 查看需要复习的文件
```

### 学习中：记录日志

```bash
# 启动 GUI
python main.py

# 在主窗口点击"学习日志" → 输入内容 → Ctrl+Enter 保存
```

### 复习后：更新文件

在 GUI 中：
1. 双击打开文件详情
2. 点击 **"更新"** 刷新时间戳

在 CLI 中：
```bash
python main.py --cli update "path/to/file.py"
```

### 周期性：导出报告

```bash
# GUI 方式
python main.py
点击"导出报告"按钮

# CLI 方式
python main.py --cli export
# 报告保存到 .study_tracker/report.txt
```

---

## CLI 命令参考

```bash
# 扫描目录初始化
python main.py --cli scan

# 查看学习状态统计
python main.py --cli status

# 列出所有文件
python main.py --cli list

# 列出需要复习的文件
python main.py --cli urgent

# 更新文件时间戳（表示已复习）
python main.py --cli update "path/to/file.py"

# 标记为已学习
python main.py --cli mark-studied "path/to/file.py"

# 标记为已掌握
python main.py --cli mark-mastered "path/to/file.py"

# 添加忽略模式（类似.gitignore）
python main.py --cli ignore "*.tmp"
python main.py --cli ignore "__pycache__/"

# 导出学习进度报告
python main.py --cli export
```

---

## 忽略文件和目录

系统支持通过 `.studyignore` 文件忽略某些文件，类似于 `.gitignore`。

### 方式1：编辑配置文件

在 `.study_tracker/.studyignore` 中添加：
```
# Python 缓存
__pycache__/
*.pyc

# 临时文件
*.tmp
*.log

# 特定目录
test_files/
temp/
```

### 方式2：使用 CLI 命令

```bash
python main.py --cli ignore "*.tmp"
python main.py --cli ignore "test_*.py"
```

### 方式3：GUI 右键菜单

在文件列表中右键点击目录 → 选择"忽略此目录"

---

## 数据存储位置

所有追踪数据都存储在 `.study_tracker/` 目录：

```
.study_tracker/
├── database.json      # 核心数据库（自动生成）
├── .studyignore       # 忽略配置（自动生成）
└── report.txt         # 导出报告（手动导出）
```

### 备份和恢复

```bash
# Windows - 备份
robocopy .study_tracker .\.study_tracker_backup /S /E

# Linux/macOS - 备份
cp -r .study_tracker .study_tracker_backup
```

---

## 常见问题

### Q: 启动时速度很慢？
**A:** 首次扫描大目录（>10000文件）会较慢，之后会加快。可以通过 `.studyignore` 忽略不必要的目录。

### Q: 日志保存在哪里？
**A:** 所有数据都存储在 `.study_tracker/database.json` 中（JSON格式）

### Q: 如何重置所有数据？
**A:** 删除 `.study_tracker` 目录，然后重新运行"扫描目录"

### Q: 能在不同项目中使用？
**A:** 可以，为每个项目分别运行，各自维护独立的数据库

### Q: 支持导入导出吗？
**A:** 支持导出报告。数据库是 JSON 格式，可以直接复制和迁移

---

## 快捷操作

| 操作 | 快捷键 |
|------|--------|
| 保存日志 | Ctrl+Enter |
| 刷新数据 | 点击"刷新数据"按钮 |
| 查看详情 | 双击文件 |
| 右键菜单 | 右键点击文件树 |

---

## 更多帮助

- 📖 详细功能说明：[FEATURES.md](FEATURES.md)
- 🔌 编程接口文档：[API.md](API.md)
- 📚 项目说明：[README.md](README.md)

**祝你学习进度追踪愉快！** 📚✨
