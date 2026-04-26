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


# 艾宾浩斯复习阶段：(阶段名, 天数上限, 阶段紧急度分数)
EBBINGHAUS_STAGES = [
    ("1d",  1,  20),
    ("3d",  3,  40),
    ("7d",  7,  60),
    ("14d", 14, 80),
    ("30d", 30, 100),
]

# 重要程度系数
IMPORTANCE_COEF = {
    "普通": 1.0,
    "重点": 1.5,
}


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
        self._migrate_file_data()
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
            "rename_history": [],
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
        renamed_files = 0
        current_files = {}

        # 构建 file_id → stored_path 反向索引，用于重命名检测
        id_to_stored_path: Dict[str, str] = {}
        for rel_path, info in self.data["files"].items():
            fid = info.get("file_id")
            if fid:
                id_to_stored_path[fid] = rel_path

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
            file_id = self._get_file_id(stat, file_path)

            current_files[rel_path] = mtime

            if rel_path not in self.data["files"]:
                now_ts = int(time.time())
                old_path = id_to_stored_path.get(file_id)

                if old_path and old_path != rel_path and old_path in self.data["files"]:
                    # 同一 file_id 出现在新路径 → 重命名/移动
                    self._migrate_renamed_file(old_path, rel_path, file_id, now_ts)
                    id_to_stored_path[file_id] = rel_path
                    # 同步更新 mtime（如果文件在移动过程中也被修改）
                    entry = self.data["files"][rel_path]
                    if mtime > entry.get("last_modified_timestamp", 0):
                        entry["last_modified"] = datetime.fromtimestamp(mtime).isoformat()
                        entry["last_modified_timestamp"] = mtime
                        entry["file_size"] = size
                    renamed_files += 1
                else:
                    self.data["files"][rel_path] = {
                        "path": rel_path,
                        "file_id": file_id,
                        "created_at": datetime.fromtimestamp(ctime).isoformat(),
                        "created_timestamp": int(ctime),
                        "last_modified": datetime.fromtimestamp(mtime).isoformat(),
                        "last_modified_timestamp": mtime,
                        "first_seen_timestamp": now_ts,
                        "first_study_timestamp": now_ts,
                        "update_count": 0,
                        "update_timestamps": [now_ts],
                        "file_size": size,
                        "status": "新建",
                        "notes": "",
                        "rename_history": [],
                        "stage_done": {s[0]: False for s in EBBINGHAUS_STAGES},
                        "is_important": "普通",
                    }
                    id_to_stored_path[file_id] = rel_path
                    new_files += 1
            else:
                entry = self.data["files"][rel_path]
                # 补填 file_id（旧记录可能没有）
                if not entry.get("file_id"):
                    entry["file_id"] = file_id
                    id_to_stored_path[file_id] = rel_path

                old_mtime = entry.get("last_modified_timestamp")
                if old_mtime is None or mtime > old_mtime:
                    now_ts = int(time.time())
                    entry["last_modified"] = datetime.fromtimestamp(mtime).isoformat()
                    entry["last_modified_timestamp"] = mtime
                    entry["update_count"] += 1
                    entry["update_timestamps"].append(now_ts)
                    entry["file_size"] = size
                    self._mark_current_stage_done(rel_path, now_ts)
                    self._record_review_detail(rel_path, "file_modified", "", now_ts)
                    updated_files += 1
                if entry["status"] == "已删除":
                    entry["status"] = "新建"

        for rel_path in list(self.data["files"].keys()):
            if rel_path not in current_files and self.data["files"][rel_path]["status"] != "已删除":
                self.data["files"][rel_path]["status"] = "已删除"

        self._save_database()

        return {
            "new_files": new_files,
            "updated_files": updated_files,
            "renamed_files": renamed_files,
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
    
    def _get_file_id(self, stat_result, file_path: Path) -> str:
        """
        获取文件的稳定唯一标识符（跨重命名/移动保持不变）。

        优先级：
        1. st_ino（NTFS/ext4 等现代文件系统均可靠）
        2. 回退：创建时间纳秒级时间戳 + 文件大小组成的指纹
        """
        ino = getattr(stat_result, 'st_ino', 0)
        if ino:
            return f"ino:{ino}"
        ctime = self._get_file_creation_time(stat_result)
        ctime_ns = int(ctime * 1_000_000_000)
        return f"fp:{ctime_ns}_{stat_result.st_size}"

    def _migrate_renamed_file(self, old_path: str, new_path: str,
                               file_id: str, timestamp: int):
        """
        将 old_path 的所有记录迁移到 new_path，保留完整历史。

        同步更新：
        - data["files"] 的键和 path 字段
        - 文件记录内的 rename_history
        - 全局 data["rename_history"]
        - data["review_records"] 中对旧路径的引用
        """
        record = self.data["files"].pop(old_path)
        record["path"] = new_path
        record["file_id"] = file_id
        record.setdefault("rename_history", []).append({
            "old_path": old_path,
            "new_path": new_path,
            "timestamp": timestamp,
            "datetime": datetime.fromtimestamp(timestamp).isoformat(),
        })
        self.data["files"][new_path] = record

        self.data.setdefault("rename_history", []).append({
            "old_path": old_path,
            "new_path": new_path,
            "file_id": file_id,
            "timestamp": timestamp,
            "datetime": datetime.fromtimestamp(timestamp).isoformat(),
        })

        for entry in self.data.get("review_records", []):
            if entry.get("file_path") == old_path:
                entry["file_path"] = new_path

    def record_update(self, file_path: str, notes: str = ""):
        """
        记录文件的手动更新（等价于一次复习），自动完成当前艾宾浩斯阶段。

        Args:
            file_path: 文件的相对路径
            notes: 更新备注
        """
        if file_path not in self.data["files"]:
            return False
        timestamp = int(time.time())
        self.data["files"][file_path]["update_count"] += 1
        self.data["files"][file_path]["update_timestamps"].append(timestamp)
        self.data["files"][file_path]["last_modified"] = datetime.now().isoformat()
        self.data["files"][file_path]["notes"] = notes
        self._mark_current_stage_done(file_path, timestamp)
        self._record_review_detail(file_path, "manual_update", notes, timestamp)
        self._save_database()
        return True
    
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
    
    def _get_current_stage(self, days: float) -> tuple:
        """根据距首次学习的天数返回 (当前阶段名, 阶段紧急度分数)"""
        for stage_name, max_day, score in EBBINGHAUS_STAGES:
            if days <= max_day:
                return stage_name, score
        return EBBINGHAUS_STAGES[-1][0], EBBINGHAUS_STAGES[-1][2]

    def _mark_current_stage_done(self, file_path: str, timestamp: int = None) -> Optional[str]:
        """
        将文件当前艾宾浩斯阶段标记为已完成。

        Returns:
            被标记的阶段名；文件不存在或缺少首次学习时间时返回 None
        """
        if timestamp is None:
            timestamp = int(time.time())
        file_entry = self.data["files"].get(file_path)
        if file_entry is None:
            return None
        first_study_ts = (
            file_entry.get("first_study_timestamp") or
            file_entry.get("first_seen_timestamp")
        )
        if first_study_ts is None:
            return None
        days = (timestamp - first_study_ts) / 86400.0
        stage_name, _ = self._get_current_stage(days)
        if "stage_done" not in file_entry:
            file_entry["stage_done"] = {s[0]: False for s in EBBINGHAUS_STAGES}
        file_entry["stage_done"][stage_name] = True
        return stage_name

    def _migrate_file_data(self):
        """
        为旧格式文件补充艾宾浩斯相关字段，并一次性回溯历史更新时间戳，
        将已存在的文件修改记录对应的艾宾浩斯阶段标记为已完成。
        """
        changed = False
        default_stage_done = {s[0]: False for s in EBBINGHAUS_STAGES}

        for info in self.data["files"].values():
            if "stage_done" not in info:
                info["stage_done"] = dict(default_stage_done)
                changed = True
            if "is_important" not in info:
                info["is_important"] = "普通"
                changed = True
            if "first_study_timestamp" not in info:
                info["first_study_timestamp"] = (
                    info.get("first_seen_timestamp") or
                    info.get("created_timestamp") or
                    int(time.time())
                )
                changed = True

        # 一次性回溯：根据历史 update_timestamps 补填 stage_done
        # 用数据库级标记确保只执行一次，避免每次启动重复扫描
        if not self.data.get("_migrated_stage_backfill"):
            for info in self.data["files"].values():
                first_study_ts = (
                    info.get("first_study_timestamp") or
                    info.get("first_seen_timestamp")
                )
                if not first_study_ts:
                    continue
                for ts in info.get("update_timestamps", []):
                    days = (ts - first_study_ts) / 86400.0
                    if days < 0:
                        continue
                    stage_name, _ = self._get_current_stage(days)
                    if not info["stage_done"].get(stage_name, False):
                        info["stage_done"][stage_name] = True
                        changed = True
            self.data["_migrated_stage_backfill"] = True
            changed = True

        # 为旧记录补填 file_id（仅在文件仍存在时）
        for rel_path, info in self.data["files"].items():
            if "file_id" not in info:
                full_path = self.root_dir / rel_path
                if full_path.exists():
                    stat = full_path.stat()
                    info["file_id"] = self._get_file_id(stat, full_path)
                else:
                    info["file_id"] = None
                changed = True

        # 确保全局 rename_history 存在
        if "rename_history" not in self.data:
            self.data["rename_history"] = []
            changed = True

        if changed:
            self._save_database()

    def cold_restart(self, file_path: str, notes: str = "") -> bool:
        """
        完全重置艾宾浩斯复习计划，从第一阶段重新开始。

        - first_study_timestamp 重置为当前时间
        - 所有 stage_done 清零
        - 本次复习视为完成 1d 阶段（当前时刻处于 0~1 天窗口内）
        """
        if file_path not in self.data["files"]:
            return False
        now_ts = int(time.time())
        entry = self.data["files"][file_path]
        entry["first_study_timestamp"] = now_ts
        entry["first_seen_timestamp"] = now_ts
        entry["stage_done"] = {s[0]: False for s in EBBINGHAUS_STAGES}
        entry["stage_done"]["1d"] = True
        entry["update_count"] = entry.get("update_count", 0) + 1
        entry["update_timestamps"] = entry.get("update_timestamps", []) + [now_ts]
        note_text = f"冷启动（完全重置）{notes}".strip()
        self._record_review_detail(file_path, "cold_restart", note_text, now_ts)
        self._save_database()
        return True

    def warm_resume(self, file_path: str, notes: str = "") -> Dict:
        """
        智能续接复习计划。

        算法：
          1. 找到历史上最后一个已完成的阶段 k（index）
          2. 若无已完成阶段 或 30d 已完成 → 降级为 cold_restart
          3. 否则：下一个阶段 = EBBINGHAUS_STAGES[k+1]
             - 把 first_study_timestamp 调整到"当前时刻处于 k+1 阶段中间点"
               即 first_study_ts = now - midpoint_day × 86400
               midpoint_day = (k 阶段最大天数 + k+1 阶段最大天数) / 2
             - 保留 0..k 阶段为完成状态
             - 标记 k+1 阶段为完成（本次复习）
             - 重置 k+2 以后的阶段为 False

        Returns:
            dict: mode='warm'/'cold', resume_from=阶段名, completed_stage=阶段名
        """
        if file_path not in self.data["files"]:
            return {"mode": "error"}

        entry = self.data["files"][file_path]
        stage_done = entry.get("stage_done", {})

        last_done_idx = -1
        for i, (s_name, _, _) in enumerate(EBBINGHAUS_STAGES):
            if stage_done.get(s_name, False):
                last_done_idx = i

        # 无历史完成阶段 或 最后阶段（30d）已完成 → 冷启动
        if last_done_idx == -1 or last_done_idx >= len(EBBINGHAUS_STAGES) - 1:
            self.cold_restart(file_path, notes)
            return {"mode": "cold"}

        next_idx = last_done_idx + 1
        last_max_day = EBBINGHAUS_STAGES[last_done_idx][1]
        next_name, next_max_day, _ = EBBINGHAUS_STAGES[next_idx]

        # 把"现在"对齐到下一阶段的中间点
        midpoint_day = (last_max_day + next_max_day) / 2.0
        now_ts = int(time.time())
        new_first_study_ts = int(now_ts - midpoint_day * 86400)

        entry["first_study_timestamp"] = new_first_study_ts
        entry["first_seen_timestamp"] = new_first_study_ts

        for i, (s_name, _, _) in enumerate(EBBINGHAUS_STAGES):
            if i <= last_done_idx:
                entry["stage_done"][s_name] = True
            elif i == next_idx:
                entry["stage_done"][s_name] = True   # 本次复习完成此阶段
            else:
                entry["stage_done"][s_name] = False  # 后续阶段等待复习

        entry["update_count"] = entry.get("update_count", 0) + 1
        entry["update_timestamps"] = entry.get("update_timestamps", []) + [now_ts]

        resume_from = EBBINGHAUS_STAGES[last_done_idx][0]
        note_text = f"温启动（从 {resume_from} 续接，完成 {next_name} 阶段）{notes}".strip()
        self._record_review_detail(file_path, "warm_resume", note_text, now_ts)
        self._save_database()
        return {"mode": "warm", "resume_from": resume_from, "completed_stage": next_name}

    def mark_important(self, file_path: str, importance: str) -> bool:
        """切换文件的重要程度标记（'普通' 或 '重点'）"""
        if file_path not in self.data["files"]:
            return False
        if importance not in IMPORTANCE_COEF:
            return False
        self.data["files"][file_path]["is_important"] = importance
        self._save_database()
        return True

    def compute_weight_score(self, file_path: str) -> Optional[float]:
        """
        基于艾宾浩斯遗忘曲线计算文件的复习权重分数（0-150）

        阶段时间窗口（从首次学习起）：
          1d:  0~1  天  紧急度 20
          3d:  1~3  天  紧急度 40
          7d:  3~7  天  紧急度 60
          14d: 7~14 天  紧急度 80
          30d: 14~30天  紧急度 100

        计算步骤：
          1. 当前阶段已完成 → 权重 = 0
          2. 当前阶段未完成：
               base = 阶段紧急度 × 重点系数
               missed_prior = 当前阶段之前未完成的阶段数
               退化倍率 = 1.0 + 0.25 × missed_prior（每跳过一个过去阶段掌握度退化 25%）
               weight = min(150, base × 退化倍率)

        重点系数：普通=1.0, 重点=1.5
        退化倍率上限：missed_prior 最多 4 → 倍率最高 2.0
        """
        if file_path not in self.data["files"]:
            return None

        file_info = self.data["files"][file_path]
        first_study_ts = (
            file_info.get("first_study_timestamp") or
            file_info.get("first_seen_timestamp")
        )
        if first_study_ts is None:
            return None

        days = (time.time() - first_study_ts) / 86400.0
        stage_name, stage_score = self._get_current_stage(days)
        stage_done = file_info.get("stage_done", {})

        if stage_done.get(stage_name, False):
            return 0.0

        importance = file_info.get("is_important", "普通")
        coef = IMPORTANCE_COEF.get(importance, 1.0)
        base_weight = stage_score * coef

        # 退化机制：当前阶段未完成时，检查有多少"应已完成"的过去阶段也未完成
        stage_index = [s[0] for s in EBBINGHAUS_STAGES].index(stage_name)
        missed_prior = sum(
            1 for i, (s_name, _, _) in enumerate(EBBINGHAUS_STAGES)
            if i < stage_index and not stage_done.get(s_name, False)
        )
        degradation = 1.0 + 0.25 * missed_prior
        return round(min(150.0, base_weight * degradation), 2)

    def get_weight_breakdown(self, file_path: str) -> Optional[Dict]:
        """
        返回权重计算的详细分解，供 UI 展示。

        Returns:
            dict 包含 days_since, stage_name, stage_score, stage_done_flag,
            importance, coef, missed_prior, degradation, base_weight, final_weight
        """
        if file_path not in self.data["files"]:
            return None
        file_info = self.data["files"][file_path]
        first_study_ts = (
            file_info.get("first_study_timestamp") or
            file_info.get("first_seen_timestamp")
        )
        if first_study_ts is None:
            return None

        days = (time.time() - first_study_ts) / 86400.0
        stage_name, stage_score = self._get_current_stage(days)
        stage_done = file_info.get("stage_done", {})
        is_done = stage_done.get(stage_name, False)
        importance = file_info.get("is_important", "普通")
        coef = IMPORTANCE_COEF.get(importance, 1.0)
        base_weight = stage_score * coef

        stage_index = [s[0] for s in EBBINGHAUS_STAGES].index(stage_name)
        missed_prior = sum(
            1 for i, (s_name, _, _) in enumerate(EBBINGHAUS_STAGES)
            if i < stage_index and not stage_done.get(s_name, False)
        )
        degradation = 1.0 + 0.25 * missed_prior
        final_weight = 0.0 if is_done else round(min(150.0, base_weight * degradation), 2)

        return {
            "days_since": days,
            "stage_name": stage_name,
            "stage_score": stage_score,
            "stage_is_done": is_done,
            "importance": importance,
            "coef": coef,
            "base_weight": base_weight,
            "missed_prior": missed_prior,
            "degradation": degradation,
            "final_weight": final_weight,
            "stage_done": stage_done,
        }

    def get_color_level(self, weight_score: float) -> str:
        """
        根据权重分数确定颜色等级

        Returns:
            'green', 'yellow', 'red'
        """
        thresholds = self._get_score_thresholds()
        if weight_score < thresholds.get('fresh_max', 1):
            return 'green'
        elif weight_score < thresholds.get('normal_max', 60):
            return 'yellow'
        else:
            return 'red'
    
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
        根据权重分数获取颜色分段（用于UI显示）

        - 'fresh':    白色 - 分数 < fresh_max（不需要复习）
        - 'early':    浅黄 - 分数 < early_max（需要复习）
        - 'normal':   橙色 - 分数 < normal_max（重点复习）
        - 'warning':  番茄红 - 分数 < warning_max（警告级）
        - 'critical': 深红 - 分数 < critical_max（紧急复习）
        - 'overdue':  暗红 - 分数 >= critical_max（已遗忘）
        """
        if file_path not in self.data["files"]:
            return 'fresh'

        score = self.compute_weight_score(file_path)
        if score is None:
            return 'fresh'

        thresholds = self._get_score_thresholds()
        if score < thresholds.get('fresh_max', 1):
            return 'fresh'
        elif score < thresholds.get('early_max', 40):
            return 'early'
        elif score < thresholds.get('normal_max', 60):
            return 'normal'
        elif score < thresholds.get('warning_max', 80):
            return 'warning'
        elif score < thresholds.get('critical_max', 100):
            return 'critical'
        else:
            return 'overdue'
    
    def get_file_list(self) -> List[Dict]:
        """获取所有文件的列表（按修改时间排序）"""
        files = []
        for rel_path, info in self.data["files"].items():
            if info["status"] != "已删除":
                age_days = self.get_file_age_days(rel_path)
                weight_score = self.compute_weight_score(rel_path)
                color = self.get_color_level(weight_score) if weight_score is not None else 'gray'

                files.append({
                    "path": rel_path,
                    **info,
                    "age_days": age_days,
                    "weight_score": weight_score,
                    "color": color
                })

        files.sort(key=lambda x: x.get("update_timestamps", [0])[-1], reverse=True)
        return files
    
    def _get_random_sampling_settings(self) -> Dict:
        """获取随机抽样配置，不可用时返回默认值"""
        from ..config.settings import StudySettings
        try:
            settings = StudySettings()
            return settings.get_random_sampling_settings()
        except:
            return {"enabled": False, "sample_size_per_tier": 10}

    def get_urgent_files(self) -> List[Dict]:
        """
        获取需要复习的文件（权重分数 > 0），按分数升序排列。

        排列规则：权重小（近期已学）的放前面，权重大（长期未复习）的放后面。
        若启用随机抽样，先按权重层次（tier）分组，每组内随机抽取至多
        sample_size_per_tier 个文件，再统一升序排列。
        """
        import random

        all_urgent = [
            f for f in self.get_file_list()
            if f.get("weight_score") is not None and f.get("weight_score") > 0
        ]

        sampling_cfg = self._get_random_sampling_settings()
        reverse = sampling_cfg.get("sort_order", "asc") == "desc"

        if sampling_cfg.get("enabled", False):
            sample_size = max(1, int(sampling_cfg.get("sample_size_per_tier", 10)))
            tiers: Dict[str, List] = {}
            for file_info in all_urgent:
                tier = self.get_color_segment(file_info["path"])
                tiers.setdefault(tier, []).append(file_info)

            sampled: List[Dict] = []
            for files in tiers.values():
                if len(files) > sample_size:
                    sampled.extend(random.sample(files, sample_size))
                else:
                    sampled.extend(files)
            return sorted(sampled, key=lambda x: x.get("weight_score", 0), reverse=reverse)

        return sorted(all_urgent, key=lambda x: x.get("weight_score", 0), reverse=reverse)
    
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
                "by_score_range": {}
            }

        thresholds = self._get_score_thresholds()
        fresh_max = thresholds.get('fresh_max', 0.2)
        early_max = thresholds.get('early_max', 0.4)
        normal_max = thresholds.get('normal_max', 0.6)
        warning_max = thresholds.get('warning_max', 0.8)
        critical_max = thresholds.get('critical_max', 1.0)

        score_ranges = {
            "fresh": 0,
            "early": 0,
            "normal": 0,
            "warning": 0,
            "critical": 0,
            "overdue": 0
        }

        recent_updates = 0
        urgent_count = 0

        for f in active_files:
            score = self.compute_weight_score(f["path"])
            if score is None:
                continue

            if score < fresh_max:
                score_ranges["fresh"] += 1
                recent_updates += 1
            elif score < early_max:
                score_ranges["early"] += 1
            elif score < normal_max:
                score_ranges["normal"] += 1
                urgent_count += 1
            elif score < warning_max:
                score_ranges["warning"] += 1
                urgent_count += 1
            elif score < critical_max:
                score_ranges["critical"] += 1
                urgent_count += 1
            else:
                score_ranges["overdue"] += 1

        return {
            "total_files": len(all_files),
            "active_files": len(active_files),
            "recent_updates": recent_updates,
            "urgent_count": urgent_count,
            "by_score_range": score_ranges
        }
    
    def get_directory_urgency(self, dir_path: str = "") -> Dict[str, Dict]:
        """
        计算目录的紧急度指标（用于目录着色）

        返回格式：
        {
            "dir_path": {
                "urgency_score": 0.0-1.0,
                "urgency_level": "critical|warning|normal|early|fresh",
                "critical_count": 0,
                "warning_count": 0,
                "total_files": 0
            }
        }
        """
        thresholds = self._get_score_thresholds()
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
                urgency_info = self._calculate_dir_urgency(files, thresholds)
                dir_urgencies[dir_name] = urgency_info
        else:
            matching_files = [f for f in all_files if f['path'].startswith(dir_path)]
            if matching_files:
                urgency_info = self._calculate_dir_urgency(matching_files, thresholds)
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
        thresholds = self._get_score_thresholds()
        urgencies = {}

        for key, subdict in dir_dict.items():
            if key == '__files__':
                continue

            full_path = f"{dir_path}/{key}" if dir_path else key

            files = subdict.get('__files__', [])

            if files:
                urgency_info = self._calculate_dir_urgency(files, thresholds)
                urgencies[full_path] = urgency_info

            nested_urgencies = self.get_nested_directory_urgency(subdict, full_path)
            urgencies.update(nested_urgencies)

        return urgencies

    def _calculate_dir_urgency(self, files: List[Dict], thresholds: Dict) -> Dict:
        """
        根据子文件的权重分数计算目录的紧急度

        权重计算：
        - 分数 >= warning_max（critical 级）: 权重=1.0
        - 分数 >= normal_max（warning 级）: 权重=0.5
        - 其他: 权重=0
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

        warning_max = thresholds.get('warning_max', 80)
        normal_max = thresholds.get('normal_max', 60)

        critical_count = 0
        warning_count = 0
        normal_count = 0

        for file_info in files:
            score = file_info.get('weight_score')
            if score is None:
                continue

            if score >= warning_max:
                critical_count += 1
            elif score >= normal_max:
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

    def _get_score_thresholds(self) -> Dict:
        """获取权重分数区间配置（艾宾浩斯模式，0-150 量程），不可用时返回默认值"""
        from ..config.settings import StudySettings
        try:
            settings = StudySettings()
            return settings.get_score_thresholds()
        except:
            return {
                "fresh_max": 1,
                "early_max": 40,
                "normal_max": 60,
                "warning_max": 80,
                "critical_max": 100,
            }
