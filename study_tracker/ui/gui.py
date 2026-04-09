"""
学习追踪系统 - GUI 界面
提供可视化的文件追踪和学习状态管理
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter import font as tkFont
from pathlib import Path
from typing import Dict
import webbrowser
import threading
import subprocess
import os
import platform
from datetime import datetime
from ..tracker.file_tracker import FileTracker, EBBINGHAUS_STAGES, IMPORTANCE_COEF


class StudyTrackerGUI:
    """学习追踪 GUI 应用"""
    
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.tracker = FileTracker(str(self.root_dir))
        
        from ..config.settings import StudySettings
        self.settings = StudySettings()
        
        self.window = tk.Tk()
        self.window.title("学习进度追踪系统")
        self.window.geometry("1200x700")
        
        self.colors = {
            'green': '#90EE90',
            'yellow': '#FFFFE0',
            'red': '#FFB6C6',
            'gray': '#D3D3D3',
            'white': '#FFFFFF',
            'deep_blue': '#00008B',
            'medium_blue': '#4169E1',
            'light_blue': '#ADD8E6'
        }
        
        self._setup_ui()
        self._ask_scan_on_startup()
        self._refresh_data()
    
    def _setup_ui(self):
        """设置 UI"""
        control_frame = ttk.Frame(self.window)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        ttk.Button(control_frame, text="扫描目录", command=self._scan_directory).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="刷新数据", command=self._refresh_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="导出报告", command=self._export_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="紧急复习", command=self._show_urgent_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="设置", command=self._open_settings).pack(side=tk.LEFT, padx=5)
        
        stats_frame = ttk.LabelFrame(self.window, text="统计信息")
        stats_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        self.stats_var = tk.StringVar()
        ttk.Label(stats_frame, textvariable=self.stats_var, font=("Arial", 10)).pack(anchor=tk.W, padx=10, pady=5)
        
        color_info_frame = ttk.LabelFrame(self.window, text="颜色说明")
        color_info_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        from ..config.settings import StudySettings
        settings = StudySettings()
        thresholds = settings.get_score_thresholds()

        color_text = (
            f"白色: 分数<{thresholds['fresh_max']} 不需要复习 | "
            f"浅黄: {thresholds['fresh_max']}-{thresholds['early_max']} 需要复习 | "
            f"橙色: {thresholds['early_max']}-{thresholds['normal_max']} 重点复习 | "
            f"红色: {thresholds['normal_max']}-{thresholds['warning_max']} 警告级 | "
            f"深红: {thresholds['warning_max']}-{thresholds['critical_max']} 紧急复习 | "
            f"暗红: >={thresholds['critical_max']} 已遗忘"
        )
        ttk.Label(color_info_frame, text=color_text, font=("Arial", 8)).pack(anchor=tk.W, padx=10, pady=5)
        
        list_frame = ttk.Frame(self.window)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(list_frame, text="文件列表", font=("Arial", 11, "bold")).pack(anchor=tk.W)
        
        search_frame = ttk.Frame(list_frame)
        search_frame.pack(fill=tk.X, pady=5)
        ttk.Label(search_frame, text="搜索:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self._on_search)
        ttk.Entry(search_frame, textvariable=self.search_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        tree_scroll = ttk.Scrollbar(list_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(
            list_frame,
            columns=("importance", "age", "updates", "status"),
            height=20,
            yscrollcommand=tree_scroll.set
        )
        tree_scroll.config(command=self.tree.yview)

        self.tree.heading('#0', text='文件名')
        self.tree.heading('importance', text='重要')
        self.tree.heading('age', text='权重')
        self.tree.heading('updates', text='更新次数')
        self.tree.heading('status', text='状态')

        self.tree.column('#0', width=340)
        self.tree.column('importance', width=46, anchor='center')
        self.tree.column('age', width=64)
        self.tree.column('updates', width=68)
        self.tree.column('status', width=80)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<Double-1>', self._on_tree_double_click)
        self.tree.bind('<Button-1>', self._on_tree_click)
        self.tree.bind('<Button-3>', self._on_tree_right_click)
        
        right_main_frame = ttk.Frame(self.window)
        right_main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # ── 上半区：推荐复习 Top 10（始终固定显示）──
        urgency_frame = ttk.LabelFrame(right_main_frame, text="复习推荐 Top 10")
        urgency_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))

        urgency_scroll = ttk.Scrollbar(urgency_frame)
        urgency_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.urgency_tree = ttk.Treeview(
            urgency_frame,
            columns=("score", "importance", "stage"),
            height=10,
            yscrollcommand=urgency_scroll.set,
            show="headings tree"
        )
        urgency_scroll.config(command=self.urgency_tree.yview)

        self.urgency_tree.heading('#0', text='文件')
        self.urgency_tree.heading('score', text='权重')
        self.urgency_tree.heading('importance', text='重要')
        self.urgency_tree.heading('stage', text='阶段')

        self.urgency_tree.column('#0', width=230)
        self.urgency_tree.column('score', width=55, anchor='center')
        self.urgency_tree.column('importance', width=46, anchor='center')
        self.urgency_tree.column('stage', width=46, anchor='center')

        self.urgency_tree.pack(fill=tk.X)
        self.urgency_tree.bind('<Button-1>', self._on_urgency_click)
        self.urgency_tree.bind('<Double-1>', self._on_urgency_double_click)

        # ── 下半区：文件元数据详情（始终可见，选中文件后更新内容）──
        detail_panel = ttk.LabelFrame(right_main_frame, text="文件详情")
        detail_panel.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.detail_panel = detail_panel

        self.detail_placeholder = ttk.Label(
            detail_panel,
            text="← 点击左侧文件或上方推荐列表查看详细信息",
            font=("Arial", 9), foreground="gray"
        )
        self.detail_placeholder.pack(expand=True)

        detail_content_frame = ttk.Frame(detail_panel)
        self.detail_content_frame = detail_content_frame

        detail_scroll = ttk.Scrollbar(detail_content_frame)
        detail_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.detail_text = tk.Text(
            detail_content_frame, width=40, wrap=tk.WORD,
            yscrollcommand=detail_scroll.set, state=tk.DISABLED
        )
        self.detail_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        detail_scroll.config(command=self.detail_text.yview)

        button_frame = ttk.Frame(detail_panel)
        self.button_frame = button_frame

        ttk.Button(button_frame, text="标记为已学", command=self._mark_studied).pack(side=tk.LEFT, padx=4)
        ttk.Button(button_frame, text="标记为已掌握", command=self._mark_mastered).pack(side=tk.LEFT, padx=4)
        ttk.Button(button_frame, text="更新", command=self._update_file).pack(side=tk.LEFT, padx=4)
        ttk.Button(button_frame, text="切换重要程度", command=self._toggle_importance).pack(side=tk.LEFT, padx=4)
        ttk.Button(button_frame, text="清除选择", command=self._clear_detail_view).pack(side=tk.LEFT, padx=4)

        notes_frame = ttk.LabelFrame(detail_panel, text="笔记", padding=5)
        self.notes_frame = notes_frame

        self.notes_text = tk.Text(notes_frame, width=40, height=4, wrap=tk.WORD)
        self.notes_text.pack(fill=tk.BOTH, expand=True, pady=5)

        ttk.Button(notes_frame, text="保存笔记", command=self._save_notes).pack(side=tk.RIGHT, padx=5, pady=5)

        self._urgency_file_map: Dict[str, str] = {}
        self._tree_file_map: Dict[str, str] = {}
        self.current_file = None
        self.in_detail_view = False
    
    def _ask_scan_on_startup(self):
        """启动时询问是否扫描文件"""
        if messagebox.askyesno("扫描", "启动时是否扫描文件目录以更新学习情况？"):
            self._scan_directory()
    
    def _open_settings(self):
        """打开设置窗口"""
        from .settings_window import SettingsWindow
        SettingsWindow(self.window, self.settings)
    
    def _scan_directory(self):
        """扫描目录"""
        result = self.tracker.scan_directory()
        messagebox.showinfo(
            "扫描完成",
            f"新文件: {result['new_files']}\n"
            f"更新文件: {result['updated_files']}\n"
            f"总文件数: {result['total_files']}"
        )
        self._refresh_data()
    
    def _refresh_data(self):
        """刷新数据显示"""
        stats = self.tracker.get_statistics()
        
        mastered_count = sum(1 for f in self.tracker.get_file_list() if f.get('status') == '已掌握')
        studied_count = sum(1 for f in self.tracker.get_file_list() if f.get('status') == '已学习')
        pending_count = stats['urgent_count']
        
        stats_text = (
            f"总文件: {stats['total_files']} | "
            f"活跃: {stats['active_files']} | "
            f"已掌握: {mastered_count} ({self._calc_percentage(mastered_count, stats['active_files'])}) | "
            f"已学习: {studied_count} ({self._calc_percentage(studied_count, stats['active_files'])}) | "
            f"待复习: {pending_count} ({self._calc_percentage(pending_count, stats['active_files'])})"
        )
        self.stats_var.set(stats_text)
        
        self._update_file_list()
        if not self.in_detail_view:
            self._update_urgency_list()
        self._check_reminders()
    
    def _calc_percentage(self, count: int, total: int) -> str:
        """计算百分比"""
        if total == 0:
            return "0%"
        return f"{int(count * 100 / total)}%"
    
    def _update_file_list(self):
        """更新文件列表显示"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        self._tree_file_map.clear()

        files = self.tracker.get_file_list()
        search_term = self.search_var.get().lower()

        dir_tree = {}
        for file_info in files:
            path = file_info['path']
            if search_term and search_term not in path.lower():
                continue

            parts = Path(path).parts
            if not parts:
                continue

            current_level = dir_tree
            for part in parts[:-1]:
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]

            if '__files__' not in current_level:
                current_level['__files__'] = []
            current_level['__files__'].append(file_info)

        dir_urgencies = self.tracker.get_nested_directory_urgency(dir_tree)

        def insert_tree_items(parent_id, dir_dict, dir_path=''):
            dirs_with_urgency = []
            for key in dir_dict.keys():
                if key == '__files__':
                    continue
                full_path = f"{dir_path}/{key}" if dir_path else key
                urgency_info = dir_urgencies.get(full_path, {
                    "urgency_score": 0.0, "urgency_level": "fresh"
                })
                dirs_with_urgency.append((key, dir_dict[key], urgency_info, full_path))

            for key, subdir, urgency_info, full_path in sorted(
                dirs_with_urgency, key=lambda x: x[2].get('urgency_score', 0.0), reverse=True
            ):
                dir_id = self.tree.insert(parent_id, 'end', text=key, open=False,
                                          values=('', '', '', ''))
                self.tree.item(dir_id, tags=(f"dir_urgency_{urgency_info.get('urgency_level', 'fresh')}",))
                insert_tree_items(dir_id, subdir, full_path)

            if '__files__' in dir_dict:
                # 按权重分数降序排列（越高越紧急，排在前面）
                sorted_files = sorted(
                    dir_dict['__files__'],
                    key=lambda x: x.get('weight_score') or 0,
                    reverse=True
                )
                for file_info in sorted_files:
                    path = file_info['path']
                    weight_score = file_info.get('weight_score')
                    score_text = f"{weight_score:.0f}" if weight_score is not None else "N/A"
                    importance = file_info.get('is_important', '普通')
                    importance_star = '★' if importance == '重点' else '☆'

                    item_id = self.tree.insert(
                        parent_id, 'end',
                        text=Path(path).name,
                        values=(importance_star, score_text,
                                file_info.get('update_count', 0),
                                file_info.get('status', ''))
                    )
                    self._tree_file_map[item_id] = path
                    segment = self.tracker.get_color_segment(path)
                    self.tree.item(item_id, tags=(f"segment_{segment}",))

        insert_tree_items('', dir_tree)
        self._configure_color_tags()
    
    def _configure_color_tags(self):
        """配置颜色标签 - 包括文件和目录"""
        from ..config.settings import StudySettings
        settings = StudySettings()
        color_mapping = settings.get_color_mapping()
        dir_color_mapping = settings.get_directory_color_mapping()
        font_config = settings.get_font_config()
        
        font_family = self._get_available_font(font_config)
        
        self.tree.tag_configure('segment_fresh', 
                               background=color_mapping['fresh']['background'], 
                               foreground=color_mapping['fresh']['foreground'],
                               font=(font_family, 9))
        self.tree.tag_configure('segment_early', 
                               background=color_mapping['early']['background'], 
                               foreground=color_mapping['early']['foreground'],
                               font=(font_family, 9))
        self.tree.tag_configure('segment_normal', 
                               background=color_mapping['normal']['background'], 
                               foreground=color_mapping['normal']['foreground'],
                               font=(font_family, 9))
        self.tree.tag_configure('segment_warning', 
                               background=color_mapping['warning']['background'], 
                               foreground=color_mapping['warning']['foreground'],
                               font=(font_family, 9))
        self.tree.tag_configure('segment_critical', 
                               background=color_mapping['critical']['background'], 
                               foreground=color_mapping['critical']['foreground'],
                               font=(font_family, 9))
        self.tree.tag_configure('segment_overdue', 
                               background=color_mapping['overdue']['background'], 
                               foreground=color_mapping['overdue']['foreground'],
                               font=(font_family, 9))
        
        self.tree.tag_configure('dir_urgency_fresh',
                               background=dir_color_mapping['fresh']['background'],
                               foreground=dir_color_mapping['fresh']['foreground'],
                               font=(font_family, 10, 'bold'))
        self.tree.tag_configure('dir_urgency_early',
                               background=dir_color_mapping['early']['background'],
                               foreground=dir_color_mapping['early']['foreground'],
                               font=(font_family, 10, 'bold'))
        self.tree.tag_configure('dir_urgency_normal',
                               background=dir_color_mapping['normal']['background'],
                               foreground=dir_color_mapping['normal']['foreground'],
                               font=(font_family, 10, 'bold'))
        self.tree.tag_configure('dir_urgency_warning',
                               background=dir_color_mapping['warning']['background'],
                               foreground=dir_color_mapping['warning']['foreground'],
                               font=(font_family, 10, 'bold'))
        self.tree.tag_configure('dir_urgency_critical',
                               background=dir_color_mapping['critical']['background'],
                               foreground=dir_color_mapping['critical']['foreground'],
                               font=(font_family, 10, 'bold'))

        for seg, cfg in color_mapping.items():
            self.urgency_tree.tag_configure(
                f"segment_{seg}",
                background=cfg['background'],
                foreground=cfg['foreground'],
                font=(font_family, 9)
            )

        self._update_urgency_list()
    
    def _get_available_font(self, font_config: Dict) -> str:
        """获取系统可用的字体"""
        from tkinter import font as tkFont
        
        available_fonts = tkFont.families()
        
        font_families = font_config.get('family', 'Arial').split(',')
        for font_name in font_families:
            font_name = font_name.strip()
            if font_name in available_fonts:
                return font_name
        
        return font_config.get('fallback_family', 'Arial')
    
    def _on_search(self, *args):
        """搜索事件"""
        self._update_file_list()
    
    def _show_urgency_list(self):
        """兼容旧调用 → 转发到 _clear_detail_view"""
        self._clear_detail_view()

    def _clear_detail_view(self):
        """清除文件选中状态，详情区恢复占位提示"""
        self.in_detail_view = False
        self.current_file = None
        self.detail_content_frame.pack_forget()
        self.button_frame.pack_forget()
        self.notes_frame.pack_forget()
        self.detail_placeholder.pack(expand=True)

    def _update_urgency_list(self):
        """刷新紧急复习推荐列表（Top 10，按权重分数降序）"""
        for item in self.urgency_tree.get_children():
            self.urgency_tree.delete(item)
        self._urgency_file_map.clear()

        import time as _time

        urgent_files = self.tracker.get_urgent_files()[:10]

        if not urgent_files:
            self.urgency_tree.insert('', 'end', text='🎉 暂无需要复习的文件', values=('', '', ''))
            return

        rank_icons = {1: '🥇', 2: '🥈', 3: '🥉'}
        for rank, file_info in enumerate(urgent_files, 1):
            path = file_info['path']
            file_name = Path(path).name
            score = file_info.get('weight_score') or 0
            importance = file_info.get('is_important', '普通')
            importance_star = '★' if importance == '重点' else '☆'

            db_info = self.tracker.data["files"].get(path, {})
            first_study_ts = db_info.get("first_study_timestamp") or db_info.get("first_seen_timestamp")
            if first_study_ts:
                days = (_time.time() - first_study_ts) / 86400.0
                stage_name = EBBINGHAUS_STAGES[-1][0]
                for s_name, s_max, _ in EBBINGHAUS_STAGES:
                    if days <= s_max:
                        stage_name = s_name
                        break
            else:
                stage_name = '?'

            icon = rank_icons.get(rank, f'{rank}.')
            item_id = self.urgency_tree.insert(
                '', 'end',
                text=f"{icon} {file_name}",
                values=(f"{score:.0f}", importance_star, stage_name)
            )
            self._urgency_file_map[item_id] = path
            segment = self.tracker.get_color_segment(path)
            self.urgency_tree.item(item_id, tags=(f"segment_{segment}",))

    def _on_urgency_click(self, event):
        """点击推荐列表 - 显示文件详情"""
        item = self.urgency_tree.identify_row(event.y)
        if not item or item not in self._urgency_file_map:
            return
        self._show_file_detail_view(self._urgency_file_map[item])

    def _on_urgency_double_click(self, event):
        """双击推荐列表 - 直接打开文件"""
        item = self.urgency_tree.identify_row(event.y)
        if not item or item not in self._urgency_file_map:
            return
        file_path = self._urgency_file_map[item]
        full_path = self.root_dir / file_path
        if not full_path.exists():
            messagebox.showerror("错误", "文件不存在")
            return
        if platform.system() == 'Windows':
            os.startfile(str(full_path))
        elif platform.system() == 'Darwin':
            subprocess.Popen(['open', str(full_path)])
        else:
            subprocess.Popen(['xdg-open', str(full_path)])
    
    def _on_tree_click(self, event):
        """树形项目单击事件：点击重要列 → 切换；点击其他列 → 显示详情"""
        col = self.tree.identify_column(event.x)
        item = self.tree.identify_row(event.y)
        if not item:
            return

        # 点击重要程度列（#1）直接切换
        if col == '#1':
            file_path = self._tree_file_map.get(item)
            if file_path:
                self._toggle_importance_for(file_path)
            return

        selected = self.tree.selection()
        if not selected:
            return
        selected_item = selected[0]
        file_path = self._tree_file_map.get(selected_item)
        if file_path:
            self._show_file_detail_view(file_path)
    
    def _show_file_detail_view(self, file_path: str):
        """在下半区详情面板中显示文件的完整元数据"""
        if file_path not in self.tracker.data["files"]:
            return

        self.current_file = file_path
        self.in_detail_view = True

        # 切换占位文字 → 详情内容
        self.detail_placeholder.pack_forget()
        self.detail_content_frame.pack(fill=tk.BOTH, expand=True)
        self.button_frame.pack(fill=tk.X, pady=3, padx=5)
        self.notes_frame.pack(fill=tk.BOTH, expand=False)

        file_info = self.tracker.data["files"][file_path]
        weight_score = self.tracker.compute_weight_score(file_path)
        color_segment = self.tracker.get_color_segment(file_path)

        self.detail_text.config(state=tk.NORMAL)
        self.detail_text.delete('1.0', tk.END)
        self.notes_text.config(state=tk.NORMAL)
        self.notes_text.delete('1.0', tk.END)

        import time as _time

        # ── 时间信息 ──
        first_study_ts = file_info.get("first_study_timestamp") or file_info.get("first_seen_timestamp")
        first_study_str = "N/A"
        days_since_first = None
        if first_study_ts:
            first_study_str = datetime.fromtimestamp(first_study_ts).strftime("%Y-%m-%d %H:%M:%S")
            days_since_first = (_time.time() - first_study_ts) / 86400.0

        last_mod_ts = file_info.get("last_modified_timestamp")
        last_mod_str = file_info.get("last_modified", "N/A")
        days_since_mod = None
        if last_mod_ts:
            days_since_mod = (_time.time() - last_mod_ts) / 86400.0

        created_str = file_info.get("created_at", "N/A")

        # ── 艾宾浩斯当前阶段 ──
        stage_done = file_info.get("stage_done", {})
        importance = file_info.get("is_important", "普通")
        importance_star = "★ 重点" if importance == "重点" else "☆ 普通"

        current_stage_name = EBBINGHAUS_STAGES[-1][0]
        current_stage_score = EBBINGHAUS_STAGES[-1][2]
        if days_since_first is not None:
            for s_name, s_max, s_score in EBBINGHAUS_STAGES:
                if days_since_first <= s_max:
                    current_stage_name = s_name
                    current_stage_score = s_score
                    break

        stage_row = "  ".join(
            f"{s}:{'✓' if stage_done.get(s, False) else '✗'}"
            for s in ["1d", "3d", "7d", "14d", "30d"]
        )

        # ── 颜色等级描述 ──
        seg_desc = {
            'fresh':    '白色  不需要复习',
            'early':    '浅黄  需要复习',
            'normal':   '橙色  重点复习',
            'warning':  '番茄红  警告级',
            'critical': '深红  紧急复习',
            'overdue':  '暗红  已遗忘',
        }

        # ── 文件大小 ──
        size_bytes = file_info.get("file_size", 0) or 0
        if size_bytes >= 1024 * 1024:
            size_str = f"{size_bytes / 1024 / 1024:.1f} MB"
        elif size_bytes >= 1024:
            size_str = f"{size_bytes / 1024:.1f} KB"
        else:
            size_str = f"{size_bytes} B"

        score_str = f"{weight_score:.1f}" if weight_score is not None else "N/A"
        days_first_str = f"（距今 {days_since_first:.1f} 天）" if days_since_first is not None else ""
        days_mod_str = f"（距今 {days_since_mod:.1f} 天）" if days_since_mod is not None else ""

        lines = [
            f"{'─'*36}",
            f"  {Path(file_path).name}",
            f"{'─'*36}",
            f"路径      {file_path}",
            f"大小      {size_str}",
            f"",
            f"── 时间信息 ──",
            f"创建时间  {created_str}",
            f"首次追踪  {first_study_str}{days_first_str}",
            f"最后修改  {last_mod_str}{days_mod_str}",
            f"",
            f"── 学习状态 ──",
            f"复习次数  {file_info.get('update_count', 0)} 次",
            f"状态      {file_info.get('status', 'N/A')}",
            f"重要程度  {importance_star}",
            f"",
            f"── 权重与颜色 ──",
            f"权重分数  {score_str} 分",
            f"颜色等级  {seg_desc.get(color_segment, color_segment)}",
            f"",
            f"── 艾宾浩斯进度 ──",
            f"当前阶段  {current_stage_name}（紧急度 {current_stage_score} 分）",
            f"阶段完成  {stage_row}",
            f"",
            f"── 最近更新记录 ──",
        ]
        self.detail_text.insert(tk.END, "\n".join(lines) + "\n")

        timestamps = file_info.get("update_timestamps", [])
        if timestamps:
            for ts in sorted(timestamps)[-8:]:
                dt = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
                self.detail_text.insert(tk.END, f"  {dt}\n")
        else:
            self.detail_text.insert(tk.END, "  暂无记录\n")

        self.detail_text.insert(tk.END, "\n右键文件可查看完整复习历史与权重计算过程\n")
        self.detail_text.config(state=tk.DISABLED)

        notes = file_info.get("notes", "")
        self.notes_text.insert(tk.END, notes)
        self.notes_text.config(state=tk.NORMAL)
    
    def _on_tree_double_click(self, event):
        """树形项目双击事件 - 直接打开文件"""
        if not self.tree.selection():
            return
        item = self.tree.selection()[0]
        rel_path = self._tree_file_map.get(item)
        if not rel_path:
            return
        full_path = self.root_dir / rel_path
        if not full_path.exists():
            messagebox.showerror("错误", "文件不存在")
            return
        if platform.system() == 'Windows':
            os.startfile(str(full_path))
        elif platform.system() == 'Darwin':
            subprocess.Popen(['open', str(full_path)])
        else:
            subprocess.Popen(['xdg-open', str(full_path)])
    
    
    def _mark_studied(self):
        """标记为已学"""
        if not hasattr(self, 'current_file') or not self.current_file:
            messagebox.showwarning("提示", "请先选择文件")
            return
        
        self.tracker.update_file_status(self.current_file, "已学习")
        messagebox.showinfo("成功", "已标记为已学习")
        self._refresh_data()
        self._show_file_detail_view(self.current_file)
    
    def _mark_mastered(self):
        """标记为已掌握"""
        if not hasattr(self, 'current_file') or not self.current_file:
            messagebox.showwarning("提示", "请先选择文件")
            return
        
        self.tracker.update_file_status(self.current_file, "已掌握")
        messagebox.showinfo("成功", "已标记为已掌握")
        self._refresh_data()
        self._show_file_detail_view(self.current_file)
    
    def _update_file(self):
        """更新文件（刷新时间戳）"""
        if not hasattr(self, 'current_file') or not self.current_file:
            messagebox.showwarning("提示", "请先选择文件")
            return
        
        notes = self.notes_text.get('1.0', tk.END).strip()
        self.tracker.record_update(self.current_file, notes)
        messagebox.showinfo("成功", "已更新文件时间戳")
        self._refresh_data()
        self._show_file_detail_view(self.current_file)
    
    def _save_notes(self):
        """保存笔记"""
        if not hasattr(self, 'current_file'):
            messagebox.showwarning("提示", "请先选择文件")
            return
        
        notes = self.notes_text.get('1.0', tk.END).strip()
        self.tracker.data["files"][self.current_file]["notes"] = notes
        self.tracker._save_database()
        messagebox.showinfo("成功", "笔记已保存")
    
    
    def _export_report(self):
        """导出报告"""
        from datetime import datetime
        
        report = "学习进度报告\n"
        report += "=" * 60 + "\n"
        report += f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        stats = self.tracker.get_statistics()
        report += "统计信息\n"
        report += "-" * 60 + "\n"
        report += f"总文件数: {stats['total_files']}\n"
        report += f"活跃文件: {stats['active_files']}\n"
        report += f"最近更新: {stats['recent_updates']}\n\n"
        
        report += "权重分数分布\n"
        report += "-" * 60 + "\n"
        for seg_name, count in stats.get('by_score_range', {}).items():
            report += f"{seg_name}: {count}\n"
        
        report += "\n\n文件详细列表\n"
        report += "-" * 60 + "\n"
        
        for file_info in self.tracker.get_file_list():
            report += f"\n文件: {file_info['path']}\n"
            report += f"  更新次数: {file_info.get('update_count', 0)}\n"
            report += f"  状态: {file_info.get('status', 'N/A')}\n"
            report += f"  最后修改: {file_info.get('last_modified', 'N/A')}\n"
        
        report_path = self.root_dir / ".study_tracker" / "report.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        messagebox.showinfo("成功", f"报告已导出到: {report_path}")
    
    def _on_tree_right_click(self, event):
        """树形项目右键点击事件"""
        item_id = self.tree.identify_row(event.y)
        if not item_id:
            return
        self.tree.selection_set(item_id)

        menu = tk.Menu(self.window, tearoff=0)
        file_path = self._tree_file_map.get(item_id)
        if file_path:
            file_info = self.tracker.data["files"].get(file_path, {})
            is_important = file_info.get("is_important", "普通") == "重点"
            label = "取消重点 ☆" if is_important else "标记为重点 ★"
            menu.add_command(label=label,
                             command=lambda fp=file_path: self._toggle_importance_for(fp))
            menu.add_command(label="查看复习详情...",
                             command=lambda fp=file_path: self._show_review_detail_popup(fp))
            menu.add_separator()
        menu.add_command(label="忽略此目录", command=self._ignore_selected_directory)
        menu.post(event.x_root, event.y_root)
    
    def _show_review_detail_popup(self, file_path: str):
        """弹窗展示该文件完整复习历史与逐步权重计算过程"""
        import time as _time

        file_info = self.tracker.data["files"].get(file_path)
        if not file_info:
            return

        popup = tk.Toplevel(self.window)
        popup.title(f"复习详情  {Path(file_path).name}")
        popup.geometry("700x560")
        popup.resizable(True, True)

        ttk.Label(popup, text=file_path, font=("Arial", 9), foreground="#555",
                  wraplength=680, justify=tk.LEFT).pack(padx=10, pady=(8, 2), anchor=tk.W)

        frame = ttk.Frame(popup)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        sb = ttk.Scrollbar(frame)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        text = tk.Text(frame, wrap=tk.WORD, yscrollcommand=sb.set, font=("Courier New", 9))
        text.pack(fill=tk.BOTH, expand=True)
        sb.config(command=text.yview)

        now = _time.time()
        first_study_ts = file_info.get("first_study_timestamp") or file_info.get("first_seen_timestamp")
        importance = file_info.get("is_important", "普通")
        stage_done = file_info.get("stage_done", {})

        # ══ 权重计算过程 ══
        text.insert(tk.END, "═" * 52 + "\n")
        text.insert(tk.END, "   权重计算过程\n")
        text.insert(tk.END, "═" * 52 + "\n\n")

        if first_study_ts:
            days_since = (now - first_study_ts) / 86400.0
            first_dt = datetime.fromtimestamp(first_study_ts).strftime("%Y-%m-%d %H:%M:%S")

            cur_stage_name = EBBINGHAUS_STAGES[-1][0]
            cur_stage_score = EBBINGHAUS_STAGES[-1][2]
            for s_name, s_max, s_score in EBBINGHAUS_STAGES:
                if days_since <= s_max:
                    cur_stage_name = s_name
                    cur_stage_score = s_score
                    break

            is_done = stage_done.get(cur_stage_name, False)
            coef = IMPORTANCE_COEF.get(importance, 1.0)
            weight = 0.0 if is_done else round(cur_stage_score * coef, 2)

            text.insert(tk.END, f"  首次学习时间   {first_dt}\n")
            text.insert(tk.END, f"  距今天数       {days_since:.2f} 天\n\n")
            text.insert(tk.END, f"  当前应完成阶段 {cur_stage_name}\n")
            text.insert(tk.END, f"    阶段紧急度   {cur_stage_score} 分\n")
            text.insert(tk.END, f"  该阶段是否完成 {'✓ 已完成' if is_done else '✗ 未完成'}\n\n")
            text.insert(tk.END, f"  重要程度       {importance}  (系数 ×{coef})\n\n")
            if is_done:
                text.insert(tk.END, f"  权重 = 0  （当前阶段已完成，暂不需要复习）\n")
            else:
                text.insert(tk.END, f"  权重 = {cur_stage_score} × {coef} = {weight} 分\n")

            seg = self.tracker.get_color_segment(file_path)
            seg_names = {
                'fresh':    '白色  不需要复习',
                'early':    '浅黄  需要复习',
                'normal':   '橙色  重点复习',
                'warning':  '番茄红  警告级',
                'critical': '深红  紧急复习',
                'overdue':  '暗红  已遗忘',
            }
            text.insert(tk.END, f"  颜色等级       {seg_names.get(seg, seg)}\n")
        else:
            text.insert(tk.END, "  首次学习时间尚未记录，无法计算权重\n")

        # ══ 艾宾浩斯阶段完成情况 ══
        text.insert(tk.END, "\n" + "─" * 52 + "\n")
        text.insert(tk.END, "   艾宾浩斯阶段完成情况\n")
        text.insert(tk.END, "─" * 52 + "\n\n")

        for s_name, s_max, s_score in EBBINGHAUS_STAGES:
            done = stage_done.get(s_name, False)
            mark = "✓" if done else "✗"
            text.insert(tk.END, f"  {mark} {s_name:4s}  ≤{s_max:2d} 天  紧急度 {s_score:3d} 分\n")

        # ══ 复习历史 ══
        records = self.tracker.get_review_records(file_path)
        text.insert(tk.END, "\n" + "─" * 52 + "\n")
        text.insert(tk.END, f"   复习历史  （共 {len(records)} 条记录）\n")
        text.insert(tk.END, "─" * 52 + "\n\n")

        if not records:
            text.insert(tk.END, "  暂无复习记录\n")
        else:
            sorted_records = sorted(records, key=lambda r: r.get("timestamp", 0))
            prev_ts = None
            for i, rec in enumerate(sorted_records, 1):
                rec_ts = rec.get("timestamp", 0)
                dt_str = rec.get("datetime", datetime.fromtimestamp(rec_ts).strftime("%Y-%m-%d %H:%M:%S") if rec_ts else "N/A")
                rec_type = rec.get("review_type", "N/A")
                notes = rec.get("notes", "")

                gap_str = ""
                if prev_ts and rec_ts:
                    gap_days = (rec_ts - prev_ts) / 86400.0
                    gap_str = f"  ← 距上次 {gap_days:.1f} 天"
                elif i == 1:
                    gap_str = "  ← 首次"

                text.insert(tk.END, f"  [{i:2d}]  {dt_str}  [{rec_type}]{gap_str}\n")
                if notes:
                    preview = notes[:70] + ("..." if len(notes) > 70 else "")
                    text.insert(tk.END, f"        备注: {preview}\n")
                prev_ts = rec_ts

        text.config(state=tk.DISABLED)
        ttk.Button(popup, text="关闭", command=popup.destroy).pack(pady=8)

    def _ignore_selected_directory(self):
        """忽略选中的目录"""
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("提示", "请先选择目录")
            return
        
        item_text = self.tree.item(item[0], 'text')
        if item_text in ['根目录'] or not self.root_dir / item_text:
            pattern = item_text
        else:
            pattern = item_text
        
        self.tracker.add_ignore_pattern(pattern)
        messagebox.showinfo("成功", f"已添加忽略模式: {pattern}")
        self._scan_directory()
    
    def _show_urgent_files(self):
        """显示需要紧急复习的文件"""
        urgent_files = self.tracker.get_urgent_files()
        
        if not urgent_files:
            messagebox.showinfo("提示", "没有需要紧急复习的文件")
            return
        
        urgent_window = tk.Toplevel(self.window)
        urgent_window.title("紧急复习列表")
        urgent_window.geometry("600x400")
        
        ttk.Label(urgent_window, text=f"共 {len(urgent_files)} 个文件需要复习", 
                  font=("Arial", 11, "bold")).pack(padx=10, pady=10)
        
        frame = ttk.Frame(urgent_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=text.yview)
        
        for file_info in urgent_files:
            age_days = file_info.get('age_days', 0)
            path = file_info['path']
            status = file_info.get('status', 'N/A')
            text.insert(tk.END, f"{path}\n")
            text.insert(tk.END, f"  天数: {age_days:.1f} | 状态: {status}\n\n")
        
        text.config(state=tk.DISABLED)
    
    def _toggle_importance_for(self, file_path: str):
        """切换指定文件的重要程度，并刷新列表和推荐栏"""
        file_info = self.tracker.data["files"].get(file_path, {})
        current = file_info.get("is_important", "普通")
        new_importance = "重点" if current == "普通" else "普通"
        self.tracker.mark_important(file_path, new_importance)
        self._update_file_list()
        self._update_urgency_list()
        if self.in_detail_view and self.current_file == file_path:
            self._show_file_detail_view(file_path)

    def _toggle_importance(self):
        """详情按钮：切换当前选中文件的重要程度"""
        if not hasattr(self, 'current_file') or not self.current_file:
            messagebox.showwarning("提示", "请先选择文件")
            return
        self._toggle_importance_for(self.current_file)

    def _check_reminders(self):
        """检查是否需要提醒"""
        stats = self.tracker.get_statistics()
        urgent_count = stats.get('urgent_count', 0)
        
        if urgent_count > 0:
            reminder_message = f"你有 {urgent_count} 个文件需要紧急复习！"
            self.window.after(3000, lambda: messagebox.showwarning("提醒", reminder_message))
    
    def run(self):
        """运行应用"""
        self.window.mainloop()


def main():
    import sys
    
    if len(sys.argv) > 1:
        root_dir = sys.argv[1]
    else:
        root_dir = str(Path(__file__).parent.parent.parent)
    
    app = StudyTrackerGUI(root_dir)
    app.run()


if __name__ == "__main__":
    main()
