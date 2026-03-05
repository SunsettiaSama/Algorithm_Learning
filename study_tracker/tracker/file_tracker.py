"""
文件追踪系统 - 核心模块
记录和管理学习文件的修改时间、更新次数、学习状态
"""

import os
import json
import time
import fnmatch
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set


class FileTracker:
    """文件追踪器 - 记录文件的元数据和状态"""
    
    def __init__(self, root_dir: str, db_file: Optional[str] = None):
        """
        初始化文件追踪器
        
        Args:
            root_dir: 要追踪的根目录
            db_file: 数据库文件路径，默认在root_dir下
        """
        self.root_dir = Path(root_dir)
        self.tracker_dir = self.root_dir / ".study_tracker"
        self.tracker_dir.mkdir(parents=True, exist_ok=True)
        self.db_file = Path(db_file) if db_file else self.tracker_dir / "database.json"
        self.ignore_file = self.tracker_dir / ".studyignore"
        self.logs_dir = self.tracker_dir / "logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.data = self._load_database()
        self.ignored_patterns = self._load_ignore_patterns()
    
    def _load_ignore_patterns(self) -> List[str]:
        """
        加载忽略模式，优先级：
        1. 从 settings 中读取后缀和目录配置
        2. 从 .studyignore 文件中读取
        3. 使用内置的默认模式
        """
        patterns = []
        
        try:
            from ..config.settings import StudySettings
            settings = StudySettings()
            ignore_config = settings.get_ignore_settings()
            
            extensions = ignore_config.get("ignore_extensions", [])
            directories = ignore_config.get("ignore_directories", [])
            
            for ext in extensions:
                if ext.startswith('.'):
                    patterns.append(f"*{ext}")
                else:
                    patterns.append(f"*.{ext}")
            
            for directory in directories:
                patterns.append(f"{directory}/")
                patterns.append(directory)
        except:
            pass
        
        defaults = [
            '.study_tracker',
            '.git',
            '__pycache__',
            '*.pyc',
            '.pytest_cache'
        ]
        patterns.extend(defaults)
        
        if self.ignore_file.exists():
            with open(self.ignore_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        patterns.append(line)
        else:
            self._create_default_ignore_file()
        
        return patterns
    
    def _create_default_ignore_file(self):
        """创建默认的 .studyignore 文件"""
        default_patterns = """# .studyignore - 指定要忽略的文件和目录
# 语法类似于 .gitignore

# 不追踪某些目录
node_modules/
dist/
build/
.venv/
venv/

# 不追踪某些文件类型
*.log
*.tmp
*.cache
*.bak

# 不追踪隐藏文件夹中的内容（已默认忽略）
"""
        with open(self.ignore_file, 'w', encoding='utf-8') as f:
            f.write(default_patterns)
    
    def _should_ignore(self, file_path: Path) -> bool:
        """检查路径是否应该被忽略"""
        rel_path = file_path.relative_to(self.root_dir)
        path_str = str(rel_path).replace('\\', '/')
        
        for pattern in self.ignored_patterns:
            if fnmatch.fnmatch(path_str, pattern) or fnmatch.fnmatch(path_str, f"{pattern}/*"):
                return True
            if any(part == pattern for part in rel_path.parts):
                return True
        
        if any(part.startswith('.') for part in rel_path.parts):
            return True
        
        return False
    
    def add_ignore_pattern(self, pattern: str):
        """添加忽略模式到 .studyignore"""
        if pattern not in self.ignored_patterns:
            self.ignored_patterns.append(pattern)
            with open(self.ignore_file, 'a', encoding='utf-8') as f:
                f.write(f"\n{pattern}")
    
    def reload_ignore_patterns(self):
        """重新加载忽略模式（在设置更新后调用）"""
        self.ignored_patterns = self._load_ignore_patterns()
    
    def _load_database(self) -> Dict:
        """加载数据库"""
        if self.db_file.exists():
            with open(self.db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "files": {},
            "study_logs": [],
            "review_records": [],
            "ignored_dirs": []
        }
    
    def _save_database(self):
        """保存数据库"""
        self.data["last_updated"] = datetime.now().isoformat()
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def scan_directory(self) -> Dict:
        """
        扫描目录，更新文件信息（只更新新增和修改的文件，不清空旧数据）
        
        使用系统文件元数据：
        - 创建时间：优先使用 st_birthtime（macOS）或通过 Windows API 获取，
                   fallback 使用 st_mtime（修改时间）
        - 修改时间：使用 st_mtime（跨平台统一）
        
        Returns:
            扫描结果统计
        """
        self.ignored_patterns = self._load_ignore_patterns()
        new_files = 0
        updated_files = 0
        current_files = {}
        
        for file_path in self.root_dir.rglob("*"):
            if file_path.is_dir():
                continue
            
            if self._should_ignore(file_path):
                continue
            
            rel_path = str(file_path.relative_to(self.root_dir)).replace('\\', '/')
            
            stat = file_path.stat()
            mtime = stat.st_mtime
            ctime = self._get_file_creation_time(stat)
            size = stat.st_size
            
            current_files[rel_path] = mtime
            
            if rel_path not in self.data["files"]:
                self.data["files"][rel_path] = {
                    "path": rel_path,
                    "created_at": datetime.fromtimestamp(ctime).isoformat(),
                    "created_timestamp": int(ctime),
                    "last_modified": datetime.fromtimestamp(mtime).isoformat(),
                    "last_modified_timestamp": mtime,
                    "first_seen_timestamp": int(time.time()),
                    "update_count": 0,
                    "update_timestamps": [int(time.time())],
                    "file_size": size,
                    "status": "新建",
                    "notes": ""
                }
                new_files += 1
            else:
                old_mtime = self.data["files"][rel_path].get("last_modified_timestamp")
                if old_mtime is None or mtime > old_mtime:
                    self.data["files"][rel_path]["last_modified"] = datetime.fromtimestamp(mtime).isoformat()
                    self.data["files"][rel_path]["last_modified_timestamp"] = mtime
                    self.data["files"][rel_path]["update_count"] += 1
                    self.data["files"][rel_path]["update_timestamps"].append(int(time.time()))
                    self.data["files"][rel_path]["file_size"] = size
                    updated_files += 1
                if self.data["files"][rel_path]["status"] == "已删除":
                    self.data["files"][rel_path]["status"] = "新建"
        
        for rel_path in list(self.data["files"].keys()):
            if rel_path not in current_files and self.data["files"][rel_path]["status"] != "已删除":
                self.data["files"][rel_path]["status"] = "已删除"
        
        self._save_database()
        
        return {
            "new_files": new_files,
            "updated_files": updated_files,
            "total_files": len(current_files),
            "scanned_at": datetime.now().isoformat()
        }
    
    def _get_file_creation_time(self, stat_result) -> float:
        """
        获取文件的创建时间（跨平台）
        
        优先级：
        1. st_birthtime（macOS）
        2. st_ctime（Windows 上可能是创建时间，需要额外处理）
        3. st_mtime（fallback，修改时间）
        
        Args:
            stat_result: os.stat() 的返回结果
            
        Returns:
            float: 文件创建时间戳
        """
        import platform
        import sys
        
        try:
            if hasattr(stat_result, 'st_birthtime'):
                return stat_result.st_birthtime
        except AttributeError:
            pass
        
        if platform.system() == 'Windows':
            try:
                import ctypes
                from ctypes import wintypes
                
                kernel32 = ctypes.windll.kernel32
                GetFileTime = kernel32.GetFileTime
                FileTimeToSystemTime = kernel32.FileTimeToSystemTime
                
                ctime = stat_result.st_ctime
                return ctime
            except:
                pass
        
        return stat_result.st_mtime
    
    def record_update(self, file_path: str, notes: str = ""):
        """
        记录文件的手动更新
        
        Args:
            file_path: 文件的相对路径
            notes: 更新备注
        """
        if file_path in self.data["files"]:
            timestamp = int(time.time())
            self.data["files"][file_path]["update_count"] += 1
            self.data["files"][file_path]["update_timestamps"].append(timestamp)
            self.data["files"][file_path]["last_modified"] = datetime.now().isoformat()
            self.data["files"][file_path]["notes"] = notes
            
            self._record_review_detail(file_path, "manual_update", notes, timestamp)
            
            self._save_database()
            return True
        return False
    
    def _record_review_detail(self, file_path: str, review_type: str, notes: str = "", timestamp: int = None):
        """
        记录详细的复习信息
        
        Args:
            file_path: 文件路径
            review_type: 复习类型（manual_update, status_change, scan等）
            notes: 复习备注
            timestamp: 时间戳（默认为当前时间）
        """
        if "review_records" not in self.data:
            self.data["review_records"] = []
        
        if timestamp is None:
            timestamp = int(time.time())
        
        record = {
            "file_path": file_path,
            "review_type": review_type,
            "timestamp": timestamp,
            "datetime": datetime.fromtimestamp(timestamp).isoformat(),
            "notes": notes,
            "update_count": self.data["files"][file_path].get("update_count", 0)
        }
        
        self.data["review_records"].append(record)
    
    def update_file_status(self, file_path: str, status: str, notes: str = ""):
        """
        更新文件的学习状态
        
        Args:
            file_path: 文件的相对路径
            status: 状态（如"已学习"、"复习中"、"掌握"等）
            notes: 备注
        """
        if file_path in self.data["files"]:
            timestamp = int(time.time())
            self.data["files"][file_path]["status"] = status
            self.data["files"][file_path]["notes"] = notes
            
            self._record_review_detail(file_path, "status_change", f"状态变更为: {status}\n{notes}", timestamp)
            
            self._save_database()
            return True
        return False
    
    def get_review_records(self, file_path: str = None) -> List[Dict]:
        """
        获取复习记录
        
        Args:
            file_path: 特定文件路径，如果为None则返回所有记录
        
        Returns:
            复习记录列表
        """
        if "review_records" not in self.data:
            return []
        
        records = self.data["review_records"]
        if file_path:
            records = [r for r in records if r["file_path"] == file_path]
        
        return sorted(records, key=lambda x: x["timestamp"], reverse=True)
    
    def add_study_log(self, content: str, date: str = None) -> bool:
        """
        添加学习日志
        
        Args:
            content: 学习内容
            date: 日期（格式：YYYY-MM-DD），默认为今天
        
        Returns:
            是否成功添加
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        if "study_logs" not in self.data:
            self.data["study_logs"] = []
        
        log_entry = {
            "date": date,
            "content": content,
            "timestamp": int(time.time())
        }
        
        self.data["study_logs"].append(log_entry)
        
        self._save_database()
        self._save_log_to_file(log_entry)
        return True
    
    def _save_log_to_file(self, log_entry: Dict):
        """保存日志到文件"""
        date = log_entry["date"]
        log_file = self.logs_dir / f"{date}.md"
        
        timestamp = log_entry.get("timestamp", int(time.time()))
        time_str = datetime.fromtimestamp(timestamp).strftime("%H:%M:%S")
        content = log_entry["content"]
        
        log_line = f"\n### {time_str}\n{content}\n"
        
        if log_file.exists():
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(log_line)
        else:
            header = f"# 学习日志 - {date}\n"
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(header)
                f.write(log_line)
    
    def get_study_logs(self, date: str = None) -> List[Dict]:
        """
        获取学习日志
        
        Args:
            date: 特定日期，如果为None则返回所有日志
        
        Returns:
            学习日志列表
        """
        if "study_logs" not in self.data:
            return []
        
        logs = self.data["study_logs"]
        if date:
            logs = [log for log in logs if log["date"] == date]
        
        return sorted(logs, key=lambda x: x["timestamp"], reverse=True)
    
    def get_file_age_days(self, file_path: str) -> Optional[float]:
        """
        获取文件距离最后修改的天数
        
        优先使用系统文件的修改时间（st_mtime），
        fallback 到追踪系统记录的时间戳
        """
        if file_path not in self.data["files"]:
            return None
        
        try:
            full_path = self.root_dir / file_path
            if full_path.exists():
                stat = full_path.stat()
                mtime = stat.st_mtime
                current_timestamp = time.time()
                age_seconds = current_timestamp - mtime
                age_days = age_seconds / (24 * 3600)
                return age_days
        except (OSError, FileNotFoundError):
            pass
        
        timestamps = self.data["files"][file_path].get("update_timestamps", [])
        if not timestamps:
            return None
        
        last_timestamp = timestamps[-1]
        current_timestamp = time.time()
        age_seconds = current_timestamp - last_timestamp
        age_days = age_seconds / (24 * 3600)
        
        return age_days
    
    def get_color_level(self, age_days: float) -> str:
        """
        根据天数确定颜色等级
        
        Returns:
            'green', 'yellow', 'red'
        """
        if age_days < 1:
            return 'green'
        elif age_days <= 3:
            progress = (age_days - 1) / 2
            if progress < 0.5:
                return 'green'
            else:
                return 'yellow'
        elif age_days <= 7:
            return 'red'
        elif age_days <= 14:
            return 'red'
        elif age_days <= 30:
            return 'red'
        else:
            return 'green'
    
    def get_review_color(self, file_path: str) -> str:
        """
        根据复习次数和时间戳计算连续颜色映射
        
        颜色映射策略：
        - 基于复习次数（掌握度）：次数越多，颜色越深
        - 基于距今时间（紧急度）：时间越久，需要复习
        - 反色映射：深色表示掌握好、需要复习少；浅色表示需要复习
        
        Returns:
            十六进制颜色代码
        """
        if file_path not in self.data["files"]:
            return '#FFFFFF'
        
        file_info = self.data["files"][file_path]
        update_count = file_info.get('update_count', 0)
        age_days = self.get_file_age_days(file_path)
        
        if age_days is None:
            return '#FFFFFF'
        
        import colorsys
        
        base_hue = 240 / 360.0
        
        saturation = min(1.0, max(0.0, age_days / 30.0))
        
        lightness = max(0.3, 1.0 - (update_count / 20.0) * 0.5)
        
        rgb = colorsys.hls_to_rgb(base_hue, lightness, saturation)
        hex_color = '#{:02x}{:02x}{:02x}'.format(
            int(rgb[0] * 255),
            int(rgb[1] * 255),
            int(rgb[2] * 255)
        )
        
        return hex_color
    
    def get_color_segment(self, file_path: str) -> str:
        """
        获取颜色分段（用于UI显示）
        
        仅基于时间判定：
        - 'fresh': 白色 - 0-1天内（不需要复习）
        - 'early': 浅黄 - 1-3天内（需要复习）
        - 'normal': 橙色 - 3-7天内（重点复习）
        - 'warning': 番茄红 - 7-14天内（警告级）
        - 'critical': 深红 - 14-30天内（紧急复习）
        - 'overdue': 暗红 - 30+天未更新（已遗忘）
        """
        from ..config.settings import StudySettings
        settings = StudySettings()
        intervals = settings.get_time_intervals()
        
        if file_path not in self.data["files"]:
            return 'fresh'
        
        age_days = self.get_file_age_days(file_path)
        
        if age_days is None:
            return 'fresh'
        
        if age_days < intervals.get('fresh_days', 1):
            return 'fresh'
        elif age_days < intervals.get('early_days', 3):
            return 'early'
        elif age_days < intervals.get('normal_days', 7):
            return 'normal'
        elif age_days < intervals.get('warning_days', 14):
            return 'warning'
        elif age_days < intervals.get('critical_days', 30):
            return 'critical'
        else:
            return 'overdue'
    
    def get_file_list(self) -> List[Dict]:
        """获取所有文件的列表（按修改时间排序）"""
        files = []
        for rel_path, info in self.data["files"].items():
            if info["status"] != "已删除":
                age_days = self.get_file_age_days(rel_path)
                color = self.get_color_level(age_days) if age_days else 'gray'
                
                files.append({
                    "path": rel_path,
                    **info,
                    "age_days": age_days,
                    "color": color
                })
        
        files.sort(key=lambda x: x.get("update_timestamps", [0])[-1], reverse=True)
        return files
    
    def get_urgent_files(self) -> List[Dict]:
        """获取需要紧急复习的文件（3-30天内未更新）"""
        urgent = []
        for file_info in self.get_file_list():
            age_days = file_info.get("age_days")
            if age_days is not None and 3 <= age_days <= 30:
                urgent.append(file_info)
        
        return sorted(urgent, key=lambda x: x.get("age_days", 0), reverse=True)
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        all_files = list(self.data["files"].values())
        active_files = [f for f in all_files if f["status"] != "已删除"]
        
        if not active_files:
            return {
                "total_files": 0,
                "active_files": 0,
                "recent_updates": 0,
                "urgent_count": 0,
                "by_age_range": {}
            }
        
        age_ranges = {
            "0_1days": 0,
            "1_3days": 0,
            "3_7days": 0,
            "7_14days": 0,
            "14_30days": 0,
            "30+days": 0
        }
        
        recent_updates = 0
        urgent_count = 0
        now = time.time()
        
        for f in active_files:
            age_days = self.get_file_age_days(f["path"])
            if age_days is None:
                continue
            
            if age_days <= 1:
                age_ranges["0_1days"] += 1
                recent_updates += 1
            elif age_days <= 3:
                age_ranges["1_3days"] += 1
            elif age_days <= 7:
                age_ranges["3_7days"] += 1
                urgent_count += 1
            elif age_days <= 14:
                age_ranges["7_14days"] += 1
                urgent_count += 1
            elif age_days <= 30:
                age_ranges["14_30days"] += 1
                urgent_count += 1
            else:
                age_ranges["30+days"] += 1
        
        return {
            "total_files": len(all_files),
            "active_files": len(active_files),
            "recent_updates": recent_updates,
            "urgent_count": urgent_count,
            "by_age_range": age_ranges
        }
    
    def get_directory_urgency(self, dir_path: str = "") -> Dict[str, Dict]:
        """
        计算目录的紧急度指标（用于目录着色）
        
        返回格式：
        {
            "dir_path": {
                "urgency_score": 0.0-1.0,  # 归一化后的紧急度分数
                "urgency_level": "critical|warning|normal|early|fresh",  # 紧急级别
                "critical_count": 0,  # 紧急复习的文件数
                "warning_count": 0,   # 警告级的文件数
                "total_files": 0      # 总文件数
            }
        }
        """
        intervals = self._get_time_intervals()
        all_files = self.get_file_list()
        
        dir_urgencies = {}
        
        if not dir_path:
            dir_dict = {}
            for file_info in all_files:
                path_parts = Path(file_info['path']).parts
                if path_parts:
                    dir_name = path_parts[0]
                    if dir_name not in dir_dict:
                        dir_dict[dir_name] = []
                    dir_dict[dir_name].append(file_info)
            
            for dir_name, files in dir_dict.items():
                urgency_info = self._calculate_dir_urgency(files, intervals)
                dir_urgencies[dir_name] = urgency_info
        else:
            matching_files = [f for f in all_files if f['path'].startswith(dir_path)]
            if matching_files:
                urgency_info = self._calculate_dir_urgency(matching_files, intervals)
                dir_urgencies[dir_path] = urgency_info
        
        return dir_urgencies
    
    def get_nested_directory_urgency(self, dir_dict: Dict[str, any], dir_path: str = "") -> Dict[str, Dict]:
        """
        递归计算嵌套目录结构中的紧急度
        
        Args:
            dir_dict: 嵌套的目录字典结构
            dir_path: 当前目录路径前缀
        
        Returns:
            Dict: 包含所有目录紧急度的字典
        """
        intervals = self._get_time_intervals()
        urgencies = {}
        
        for key, subdict in dir_dict.items():
            if key == '__files__':
                continue
            
            full_path = f"{dir_path}/{key}" if dir_path else key
            
            files = subdict.get('__files__', [])
            
            if files:
                urgency_info = self._calculate_dir_urgency(files, intervals)
                urgencies[full_path] = urgency_info
            
            nested_urgencies = self.get_nested_directory_urgency(subdict, full_path)
            urgencies.update(nested_urgencies)
        
        return urgencies
    
    def _calculate_dir_urgency(self, files: List[Dict], intervals: Dict) -> Dict:
        """
        根据子文件的紧急度计算目录的紧急度
        
        权重计算：
        - 紧急复习（critical）: 权重=1.0
        - 警告级（warning）: 权重=0.5
        - 其他（normal/early/fresh）: 权重=0
        """
        if not files:
            return {
                "urgency_score": 0.0,
                "urgency_level": "fresh",
                "critical_count": 0,
                "warning_count": 0,
                "normal_count": 0,
                "total_files": 0
            }
        
        critical_count = 0
        warning_count = 0
        normal_count = 0
        
        for file_info in files:
            age_days = file_info.get('age_days')
            if age_days is None:
                continue
            
            if age_days >= intervals.get('warning_days', 14):
                critical_count += 1
            elif age_days >= intervals.get('normal_days', 7):
                warning_count += 1
            else:
                normal_count += 1
        
        total = len(files)
        if total == 0:
            return {
                "urgency_score": 0.0,
                "urgency_level": "fresh",
                "critical_count": 0,
                "warning_count": 0,
                "normal_count": 0,
                "total_files": 0
            }
        
        weighted_score = (critical_count * 1.0 + warning_count * 0.5) / total
        
        if weighted_score >= 0.7:
            urgency_level = "critical"
        elif weighted_score >= 0.4:
            urgency_level = "warning"
        elif weighted_score >= 0.2:
            urgency_level = "normal"
        elif weighted_score >= 0.1:
            urgency_level = "early"
        else:
            urgency_level = "fresh"
        
        return {
            "urgency_score": min(1.0, weighted_score),
            "urgency_level": urgency_level,
            "critical_count": critical_count,
            "warning_count": warning_count,
            "normal_count": normal_count,
            "total_files": total
        }
    
    def _get_time_intervals(self) -> Dict:
        """获取时间间隔配置，使用默认值如果未设置"""
        from ..config.settings import StudySettings
        try:
            settings = StudySettings()
            return settings.get_time_intervals()
        except:
            return {
                "fresh_days": 1,
                "early_days": 3,
                "normal_days": 7,
                "warning_days": 14,
                "critical_days": 30
            }
