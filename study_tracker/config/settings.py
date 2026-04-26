"""
学习追踪系统 - 配置管理
管理学习曲线、颜色映射、复习周期等设置
"""

import json
from pathlib import Path
from typing import Dict, List, Optional


class StudySettings:
    """学习设置管理器"""
    
    def __init__(self, settings_file: Optional[str] = None):
        """
        初始化设置管理器
        
        Args:
            settings_file: 设置文件路径
        """
        if settings_file:
            self.settings_file = Path(settings_file)
        else:
            config_dir = Path(__file__).parent
            self.settings_file = config_dir / "settings.json"
        
        self.data = self._load_settings()
    
    def _load_settings(self) -> Dict:
        """加载设置文件"""
        if self.settings_file.exists():
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return self._get_default_settings()
    
    def _get_default_settings(self) -> Dict:
        """获取默认设置"""
        return {
            "version": "1.0",
            "review_schedule": {
                "first_review_hours": 1,
                "second_review_hours": 24,
                "third_review_hours": 72,
                "description": "复习周期（小时）"
            },
            "time_intervals": {
                "fresh_days": 1,
                "early_days": 3,
                "normal_days": 7,
                "warning_days": 14,
                "critical_days": 30,
                "description": "复习时间区间配置（天数）—— 已由 score_thresholds 接管底层逻辑，此项仅作参考保留"
            },
            "score_thresholds": {
                "fresh_max": 1,
                "early_max": 40,
                "normal_max": 60,
                "warning_max": 80,
                "critical_max": 100,
                "description": "艾宾浩斯权重分数区间（0-150）：0=当前阶段已完成，>0 表示需复习"
            },
            "color_mapping": {
                "fresh": {
                    "background": "#FFFFFF",
                    "foreground": "#000000",
                    "description": "0-1天内 - 不需要复习（白色）"
                },
                "early": {
                    "background": "#FFFFE0",
                    "foreground": "#000000",
                    "description": "1-3天内 - 需要复习（浅黄）"
                },
                "normal": {
                    "background": "#FFA500",
                    "foreground": "#FFFFFF",
                    "description": "3-7天内 - 重点复习（橙色）"
                },
                "warning": {
                    "background": "#FF6347",
                    "foreground": "#FFFFFF",
                    "description": "7-14天内 - 警告级（番茄红）"
                },
                "critical": {
                    "background": "#DC143C",
                    "foreground": "#FFFFFF",
                    "description": "14-30天内 - 紧急复习（深红）"
                },
                "overdue": {
                    "background": "#8B0000",
                    "foreground": "#FFFFFF",
                    "description": "30+天未更新 - 已遗忘（暗红）"
                }
            },
            "directory_color_mapping": {
                "description": "目录级别的颜色连续映射 - 基于子文件的紧急度权重",
                "color_scheme": "orange_continuous",
                "min_color": "#FFFFFF",
                "max_color": "#FF4500",
                "fresh": {
                    "background": "#FFFFFF",
                    "foreground": "#000000",
                    "description": "没有紧急文件 - 白色（不需要急着复习）"
                },
                "early": {
                    "background": "#FFE4B5",
                    "foreground": "#000000",
                    "description": "有少量紧急文件 - 淡橙色"
                },
                "normal": {
                    "background": "#FFD700",
                    "foreground": "#000000",
                    "description": "有中等紧急文件 - 中橙色"
                },
                "warning": {
                    "background": "#FF8C00",
                    "foreground": "#FFFFFF",
                    "description": "有较多紧急文件 - 深橙色"
                },
                "critical": {
                    "background": "#FF4500",
                    "foreground": "#FFFFFF",
                    "description": "有大量紧急文件 - 超深橙色"
                }
            },
            "font_config": {
                "family": "Microsoft YaHei, SimHei, Arial, Helvetica, sans-serif",
                "default_family": "Microsoft YaHei",
                "fallback_family": "Arial",
                "description": "全局字体配置"
            },
            "ignore_settings": {
                "ignore_extensions": [
                    ".log",
                    ".tmp",
                    ".cache",
                    ".bak",
                    ".pyc"
                ],
                "ignore_directories": [
                    "node_modules",
                    "dist",
                    "build",
                    ".venv",
                    "venv",
                    "__pycache__",
                    ".pytest_cache"
                ],
                "description": "文件和目录忽略配置"
            },
            "mastery_weights": {
                "update_count_weight": 0.6,
                "time_weight": 0.4,
                "description": "掌握度计算权重"
            },
            "random_sampling": {
                "enabled": False,
                "sample_size_per_tier": 10,
                "sort_order": "asc",
                "description": "同权重层次内随机抽样，避免复习列表顺序固定；sort_order: asc=升序(近期学的在前), desc=降序(最紧急在前)"
            },
            "advanced_settings": {
                "forgetting_curve": "PLACEHOLDER_ebbinghaus_curve_not_implemented",
                "adaptive_schedule": "PLACEHOLDER_adaptive_scheduling_not_implemented",
                "ml_prediction": "PLACEHOLDER_ml_based_prediction_not_implemented",
                "description": "高级设置（待实现）"
            }
        }
    
    def _save_settings(self):
        """保存设置到文件"""
        self.settings_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.settings_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def get_review_schedule(self) -> Dict[str, int]:
        """获取复习周期设置"""
        return self.data.get("review_schedule", {})
    
    def set_review_schedule(self, first_hours: int, second_hours: int, third_hours: int) -> bool:
        """
        设置复习周期
        
        Args:
            first_hours: 第一次复习的时间（小时）
            second_hours: 第二次复习的时间（小时）
            third_hours: 第三次复习的时间（小时）
        
        Returns:
            是否成功
        """
        self.data["review_schedule"]["first_review_hours"] = first_hours
        self.data["review_schedule"]["second_review_hours"] = second_hours
        self.data["review_schedule"]["third_review_hours"] = third_hours
        self._save_settings()
        return True
    
    def get_mastery_weights(self) -> Dict[str, float]:
        """获取掌握度权重"""
        return self.data.get("mastery_weights", {})
    
    def set_mastery_weights(self, update_count_weight: float, time_weight: float) -> bool:
        """
        设置掌握度权重
        
        Args:
            update_count_weight: 复习次数权重
            time_weight: 时间权重
        
        Returns:
            是否成功
        """
        self.data["mastery_weights"]["update_count_weight"] = update_count_weight
        self.data["mastery_weights"]["time_weight"] = time_weight
        self._save_settings()
        return True
    
    def get_ignore_settings(self) -> Dict:
        """获取忽略配置"""
        return self.data.get("ignore_settings", {
            "ignore_extensions": [".log", ".tmp", ".cache", ".bak", ".pyc"],
            "ignore_directories": ["node_modules", "dist", "build", ".venv", "venv", "__pycache__", ".pytest_cache"]
        })
    
    def set_ignore_extensions(self, extensions: List[str]) -> bool:
        """
        设置要忽略的文件后缀列表
        
        Args:
            extensions: 后缀列表，如 ['.log', '.tmp']
        
        Returns:
            是否成功
        """
        if "ignore_settings" not in self.data:
            self.data["ignore_settings"] = {
                "ignore_extensions": [],
                "ignore_directories": []
            }
        
        self.data["ignore_settings"]["ignore_extensions"] = extensions
        self._save_settings()
        return True
    
    def set_ignore_directories(self, directories: List[str]) -> bool:
        """
        设置要忽略的目录列表
        
        Args:
            directories: 目录名列表，如 ['node_modules', 'dist']
        
        Returns:
            是否成功
        """
        if "ignore_settings" not in self.data:
            self.data["ignore_settings"] = {
                "ignore_extensions": [],
                "ignore_directories": []
            }
        
        self.data["ignore_settings"]["ignore_directories"] = directories
        self._save_settings()
        return True
    
    def get_color_mapping(self) -> Dict:
        """获取颜色映射设置"""
        return self.data.get("color_mapping", {})
    
    def get_directory_color_mapping(self) -> Dict:
        """获取目录颜色映射设置"""
        return self.data.get("directory_color_mapping", {})
    
    def get_font_config(self) -> Dict:
        """获取字体配置"""
        return self.data.get("font_config", {
            "family": "Microsoft YaHei, SimHei, Arial, Helvetica, sans-serif",
            "default_family": "Microsoft YaHei",
            "fallback_family": "Arial"
        })
    
    def get_score_thresholds(self) -> Dict[str, float]:
        """获取权重分数区间配置（艾宾浩斯模式，0-150 量程）"""
        defaults = {
            "fresh_max": 1,
            "early_max": 40,
            "normal_max": 60,
            "warning_max": 80,
            "critical_max": 100,
        }
        thresholds = self.data.get("score_thresholds", defaults)
        # 兼容旧版 0.0-1.0 量程：自动返回新默认值
        if thresholds.get("fresh_max", 0) < 2:
            return defaults
        return thresholds

    def set_score_thresholds(self, fresh_max: float, early_max: float, normal_max: float,
                             warning_max: float, critical_max: float) -> bool:
        """
        设置权重分数区间配置

        Args:
            fresh_max: 不需要复习的分数上限
            early_max: 早期复习的分数上限
            normal_max: 重点复习的分数上限
            warning_max: 警告级的分数上限
            critical_max: 紧急复习的分数上限（超过此值视为 overdue）
        """
        if "score_thresholds" not in self.data:
            self.data["score_thresholds"] = {}
        self.data["score_thresholds"]["fresh_max"] = fresh_max
        self.data["score_thresholds"]["early_max"] = early_max
        self.data["score_thresholds"]["normal_max"] = normal_max
        self.data["score_thresholds"]["warning_max"] = warning_max
        self.data["score_thresholds"]["critical_max"] = critical_max
        self._save_settings()
        return True

    def get_time_intervals(self) -> Dict[str, int]:
        """获取时间区间配置"""
        return self.data.get("time_intervals", {
            "fresh_days": 1,
            "early_days": 3,
            "normal_days": 7,
            "warning_days": 14,
            "critical_days": 30
        })
    
    def set_time_intervals(self, fresh_days: int, early_days: int, normal_days: int, 
                          warning_days: int, critical_days: int) -> bool:
        """
        设置时间区间配置
        
        Args:
            fresh_days: 不需要复习的天数阈值
            early_days: 早期复习的天数阈值
            normal_days: 正常复习的天数阈值
            warning_days: 警告级别的天数阈值
            critical_days: 紧急复习的天数阈值
        
        Returns:
            是否成功
        """
        self.data["time_intervals"]["fresh_days"] = fresh_days
        self.data["time_intervals"]["early_days"] = early_days
        self.data["time_intervals"]["normal_days"] = normal_days
        self.data["time_intervals"]["warning_days"] = warning_days
        self.data["time_intervals"]["critical_days"] = critical_days
        self._save_settings()
        return True
    
    def get_random_sampling_settings(self) -> Dict:
        """获取随机抽样配置"""
        return self.data.get("random_sampling", {
            "enabled": False,
            "sample_size_per_tier": 10,
            "sort_order": "asc",
        })

    def set_random_sampling_settings(self, enabled: bool, sample_size_per_tier: int,
                                     sort_order: str = "asc") -> bool:
        """
        设置随机抽样配置

        Args:
            enabled: 是否启用随机抽样
            sample_size_per_tier: 每个权重层次最多抽取的文件数
            sort_order: 排序方向，'asc' 升序（近期学的在前）或 'desc' 降序（最紧急在前）
        """
        if sort_order not in ("asc", "desc"):
            sort_order = "asc"
        if "random_sampling" not in self.data:
            self.data["random_sampling"] = {}
        self.data["random_sampling"]["enabled"] = enabled
        self.data["random_sampling"]["sample_size_per_tier"] = sample_size_per_tier
        self.data["random_sampling"]["sort_order"] = sort_order
        self._save_settings()
        return True

    def reset_to_default(self) -> bool:
        """重置为默认设置"""
        self.data = self._get_default_settings()
        self._save_settings()
        return True
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return self.data.copy()
