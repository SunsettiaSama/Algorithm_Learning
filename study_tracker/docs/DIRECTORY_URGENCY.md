# 目录紧急度映射功能说明

## 概述

为了更好地组织和管理学习进度，系统新增了**目录级别的紧急度映射**功能。该功能通过分析子文件的紧急复习需求，自动计算目录的紧急度等级，并用不同的橙色深度进行可视化展示。

## 功能特性

### 1. 目录紧急度权重计算

根据子文件的紧急状态进行权重计算：

- **紧急文件** (14-30天未更新或30+天): 权重 = **1.0**
- **警告文件** (7-14天未更新): 权重 = **0.5**
- **其他文件** (0-7天): 权重 = **0**

### 2. 紧急度分数计算公式

```
紧急度分数 = (紧急文件数 × 1.0 + 警告文件数 × 0.5) / 总文件数
```

### 3. 紧急度等级划分

| 分数范围 | 等级 | 颜色 | 含义 |
|---------|------|------|------|
| ≥ 0.7 | critical | #FF4500 (深橙) | 大量紧急文件需要复习 |
| 0.4-0.7 | warning | #FF8C00 (中深橙) | 有较多紧急文件 |
| 0.2-0.4 | normal | #FFD700 (中橙) | 有中等紧急文件 |
| 0.1-0.2 | early | #FFE4B5 (淡橙) | 有少量紧急文件 |
| < 0.1 | fresh | #FFF8DC (浅橙) | 没有紧急文件 |

### 4. 显示层次

- **目录节点**: 使用加粗字体，背景色为橙色系，深度反映子文件的紧急程度
- **文件节点**: 字体大小比目录小，背景色保持原有的红/黄系统
- **排序**: 目录和文件都按紧急程度倒序排列，紧急的在前面

## 配置管理

### 配置文件位置

`study_tracker/config/settings.json` 中的 `directory_color_mapping` 部分：

```json
{
  "directory_color_mapping": {
    "description": "目录级别的橙色连续映射 - 基于子文件的紧急度权重",
    "color_scheme": "orange_continuous",
    "min_color": "#FFF8DC",
    "max_color": "#FF4500",
    "fresh": {
      "background": "#FFF8DC",
      "foreground": "#000000"
    },
    "early": {
      "background": "#FFE4B5",
      "foreground": "#000000"
    },
    "normal": {
      "background": "#FFD700",
      "foreground": "#000000"
    },
    "warning": {
      "background": "#FF8C00",
      "foreground": "#FFFFFF"
    },
    "critical": {
      "background": "#FF4500",
      "foreground": "#FFFFFF"
    }
  }
}
```

### 字体配置

`settings.json` 中的 `font_config` 部分控制全局字体：

```json
{
  "font_config": {
    "family": "Microsoft YaHei, SimHei, Arial, Helvetica, sans-serif",
    "default_family": "Microsoft YaHei",
    "fallback_family": "Arial",
    "description": "全局字体配置"
  }
}
```

系统会自动尝试以下字体（按优先级）：
1. Microsoft YaHei (微软雅黑) - Windows 推荐
2. SimHei (黑体) - 备选中文字体
3. Arial / Helvetica - 英文备选
4. 系统默认 Arial

## API 使用

### 获取目录紧急度

```python
from study_tracker.tracker.file_tracker import FileTracker

tracker = FileTracker('.')

# 获取所有顶级目录的紧急度
dir_urgencies = tracker.get_directory_urgency()

# 返回格式
# {
#     "目录名": {
#         "urgency_score": 0.0-1.0,      # 归一化分数
#         "urgency_level": "critical",    # 等级
#         "critical_count": 1,            # 紧急文件数
#         "warning_count": 2,             # 警告文件数
#         "normal_count": 3,              # 普通文件数
#         "total_files": 6                # 总文件数
#     }
# }
```

### 单个目录的紧急度

```python
# 获取特定目录的紧急度
urgencies = tracker.get_directory_urgency("基础算法")
```

## 界面展示

### 目录树结构

```
┌─ [critical] 基础算法                    (深橙 #FF4500)
│  ├─ [critical] 快速排序.py             (深红 #DC143C)
│  ├─ [critical] 冒泡排序.py             (暗红 #8B0000)
│  └─ [normal] 递归算法.py               (橙色 #FFA500)
│
├─ [warning] 数据结构                     (中深橙 #FF8C00)
│  ├─ [critical] 栈和队列.py             (深红 #DC143C)
│  ├─ [normal] 二叉搜索树.py             (橙色 #FFA500)
│  └─ [early] 链表.py                    (浅黄 #FFFFE0)
│
└─ [fresh] 高级算法                       (浅橙 #FFF8DC)
   ├─ [normal] 图遍历.py                 (橙色 #FFA500)
   └─ [early] 动态规划.py                (浅黄 #FFFFE0)
```

## 实现细节

### 内部方法

#### `get_directory_urgency(dir_path="")`

获取目录的紧急度信息。

**参数：**
- `dir_path` (str): 目录路径，空字符串表示获取所有顶级目录

**返回：**
- Dict: 包含紧急度信息的字典

#### `_calculate_dir_urgency(files, intervals)`

根据文件列表计算目录的紧急度。

**参数：**
- `files` (List[Dict]): 文件信息列表
- `intervals` (Dict): 时间区间配置

**返回：**
- Dict: 包含紧急度分数、等级和文件统计的字典

### 时间区间配置

从 `settings.py` 自动读取以下配置：

- `fresh_days`: 0-1天（默认）
- `early_days`: 1-3天（默认）
- `normal_days`: 3-7天（默认）
- `warning_days`: 7-14天（默认）
- `critical_days`: 14-30天（默认）

## 使用场景

### 1. 快速定位需要复习的知识体系

当某个目录显示为深橙色或红色时，说明该知识点的多个文件需要复习。

### 2. 学习计划制定

通过目录的紧急度颜色，快速制定学习计划：
- 深橙 ➜ 立即复习
- 中深橙 ➜ 今日复习
- 中橙 ➜ 本周复习
- 淡橙 ➜ 下周复习
- 浅橙 ➜ 保持学习

### 3. 学习进度监控

定期查看各目录的颜色变化，了解整体学习进度。

## 注意事项

1. **文件与目录颜色系统不同**
   - 文件：使用红/黄系统（表示时间紧急程度）
   - 目录：使用橙色系统（表示权重紧急程度）

2. **权重计算**
   - 只考虑紧急和警告级别的文件
   - 其他级别的文件不计入权重

3. **字体一致性**
   - 所有文本使用统一的字体配置
   - 目录节点加粗，文件节点正常

4. **性能**
   - 紧急度计算在每次刷新时执行
   - 对于大量文件的目录，计算时间可能较长

## 故障排除

### 问题：目录颜色未变化

**解决方案：**
1. 检查数据库是否正确更新
2. 尝试点击"刷新数据"按钮
3. 检查 `settings.json` 中的 `directory_color_mapping` 配置

### 问题：字体显示不正确

**解决方案：**
1. 检查系统安装的字体
2. 修改 `font_config` 中的字体列表
3. 使用系统支持的字体

### 问题：紧急度分数不合理

**解决方案：**
1. 检查文件的 `age_days` 是否正确
2. 验证 `time_intervals` 配置
3. 手动运行 `test_directory_urgency.py` 进行调试

## 扩展建议

1. **连续颜色梯度**：使用 HSL 或 RGB 插值实现更平滑的颜色过渡
2. **自定义权重**：在设置中添加可配置的权重参数
3. **子目录支持**：支持计算嵌套子目录的紧急度
4. **导出报告**：生成目录紧急度的报告
