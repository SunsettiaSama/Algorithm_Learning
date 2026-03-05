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
from ..tracker.file_tracker import FileTracker
from .study_log_window import StudyLogWindow


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
        ttk.Button(control_frame, text="学习日志", command=self._open_study_log).pack(side=tk.LEFT, padx=5)
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
        intervals = settings.get_time_intervals()
        
        color_text = (
            f"白色: 0-{intervals['fresh_days']}天 不需要复习 | "
            f"浅黄: {intervals['fresh_days']}-{intervals['early_days']}天 需要复习 | "
            f"橙色: {intervals['early_days']}-{intervals['normal_days']}天 重点复习 | "
            f"红色: {intervals['normal_days']}-{intervals['warning_days']}天 警告级 | "
            f"深红: {intervals['warning_days']}-{intervals['critical_days']}天 紧急复习 | "
            f"暗红: {intervals['critical_days']}+天 已遗忘"
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
            columns=("age", "updates", "status"),
            height=20,
            yscrollcommand=tree_scroll.set
        )
        tree_scroll.config(command=self.tree.yview)
        
        self.tree.heading('#0', text='文件名')
        self.tree.heading('age', text='天数')
        self.tree.heading('updates', text='更新次数')
        self.tree.heading('status', text='状态')
        
        self.tree.column('#0', width=400)
        self.tree.column('age', width=80)
        self.tree.column('updates', width=80)
        self.tree.column('status', width=100)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<Double-1>', self._on_tree_double_click)
        self.tree.bind('<Button-1>', self._on_tree_click)
        self.tree.bind('<Button-3>', self._on_tree_right_click)
        
        right_main_frame = ttk.Frame(self.window)
        right_main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        activity_frame = ttk.LabelFrame(right_main_frame, text="学习动态")
        activity_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.activity_frame = activity_frame
        self.activity_text = tk.Text(activity_frame, width=35, wrap=tk.WORD)
        self.activity_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.activity_text.config(state=tk.DISABLED)
        
        detail_container = ttk.Frame(activity_frame)
        self.detail_container = detail_container
        
        detail_scroll = ttk.Scrollbar(detail_container)
        detail_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.detail_text = tk.Text(detail_container, width=35, wrap=tk.WORD, yscrollcommand=detail_scroll.set)
        self.detail_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5, side=tk.LEFT)
        self.detail_text.config(state=tk.DISABLED)
        detail_scroll.config(command=self.detail_text.yview)
        
        button_frame = ttk.Frame(activity_frame)
        self.button_frame = button_frame
        
        ttk.Button(button_frame, text="标记为已学", command=self._mark_studied).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="标记为已掌握", command=self._mark_mastered).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="更新", command=self._update_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="返回动态", command=self._show_activity_list).pack(side=tk.LEFT, padx=5)
        
        notes_frame = ttk.LabelFrame(activity_frame, text="笔记", padding=5)
        self.notes_frame = notes_frame
        
        self.notes_text = tk.Text(notes_frame, width=35, height=6, wrap=tk.WORD)
        self.notes_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        ttk.Button(notes_frame, text="保存笔记", command=self._save_notes).pack(side=tk.RIGHT, padx=5, pady=5)
        
        log_frame = ttk.LabelFrame(right_main_frame, text="学习日记")
        log_frame.pack(fill=tk.BOTH, expand=False, padx=0, pady=(10, 0))
        
        self.log_text = tk.Text(log_frame, width=35, height=8, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.log_text.config(state=tk.DISABLED)
        
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
        
        files = self.tracker.get_file_list()
        search_term = self.search_var.get().lower()
        
        # 构建嵌套的目录树结构
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
        
        # 获取所有嵌套目录的紧急度信息
        dir_urgencies = self.tracker.get_nested_directory_urgency(dir_tree)
        
        # 递归插入树形结构 - 按紧急度排序（所有层级）
        def insert_tree_items(parent_id, dir_dict, dir_path='', is_top_level=False):
            dirs_with_urgency = []
            
            for key in dir_dict.keys():
                if key == '__files__':
                    continue
                
                full_path = f"{dir_path}/{key}" if dir_path else key
                urgency_info = dir_urgencies.get(full_path, {
                    "urgency_score": 0.0,
                    "urgency_level": "fresh"
                })
                dirs_with_urgency.append((key, dir_dict[key], urgency_info, full_path))
            
            sorted_dirs = sorted(dirs_with_urgency, 
                               key=lambda x: x[2].get('urgency_score', 0.0), 
                               reverse=True)
            
            for key, subdir, urgency_info, full_path in sorted_dirs:
                dir_id = self.tree.insert(parent_id, 'end', text=key, open=False)
                
                urgency_level = urgency_info.get('urgency_level', 'fresh')
                tag_name = f"dir_urgency_{urgency_level}"
                self.tree.item(dir_id, tags=(tag_name,))
                
                insert_tree_items(dir_id, subdir, full_path, is_top_level=False)
            
            if '__files__' in dir_dict:
                sorted_files = sorted(dir_dict['__files__'], 
                                    key=lambda x: x.get('age_days', 0), 
                                    reverse=True)
                
                for file_info in sorted_files:
                    age_days = file_info.get('age_days')
                    age_text = f"{age_days:.1f}" if age_days is not None else "N/A"
                    
                    item_id = self.tree.insert(
                        parent_id, 'end',
                        text=Path(file_info['path']).name,
                        values=(
                            age_text,
                            file_info.get('update_count', 0),
                            file_info.get('status', '')
                        )
                    )
                    
                    segment = self.tracker.get_color_segment(file_info['path'])
                    tag_name = f"segment_{segment}"
                    self.tree.item(item_id, tags=(tag_name,))
        
        insert_tree_items('', dir_tree, '', is_top_level=True)
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
        
        self._show_activity_list()
    
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
        
        self._show_activity_list()
    
    def _on_search(self, *args):
        """搜索事件"""
        self._update_file_list()
    
    def _show_activity_list(self):
        """显示学习动态列表"""
        self.in_detail_view = False
        
        self.detail_container.pack_forget()
        self.button_frame.pack_forget()
        self.notes_frame.pack_forget()
        
        self.activity_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.activity_text.config(state=tk.NORMAL)
        self.activity_text.delete('1.0', tk.END)
        
        files = self.tracker.get_file_list()
        if not files:
            self.activity_text.insert(tk.END, "暂无文件更新")
            self.activity_text.config(state=tk.DISABLED)
            self._refresh_logs()
            return
        
        activity_text = "【最近更新】\n"
        activity_text += "=" * 40 + "\n\n"
        
        recent_files = files[:10]
        
        for file_info in recent_files:
            path = file_info['path']
            status = file_info.get('status', '新建')
            age_days = file_info.get('age_days', 0)
            update_count = file_info.get('update_count', 0)
            
            activity_text += f"📄 {Path(path).name}\n"
            activity_text += f"   路径: {path}\n"
            activity_text += f"   状态: {status}\n"
            activity_text += f"   更新: {update_count}次 | 距今: {age_days:.1f}天\n"
            activity_text += "-" * 40 + "\n\n"
        
        self.activity_text.insert(tk.END, activity_text)
        self.activity_text.config(state=tk.DISABLED)
        
        self._refresh_logs()
    
    def _on_tree_click(self, event):
        """树形项目单击事件 - 显示文件详情"""
        item = self.tree.selection()
        if not item:
            return
        
        selected_item = item[0]
        parent = self.tree.parent(selected_item)
        
        if not parent:
            return
        
        item_text = self.tree.item(selected_item, 'text')
        parent_text = self.tree.item(parent, 'text')
        
        for file_info in self.tracker.get_file_list():
            file_name = Path(file_info['path']).name
            if file_name == item_text:
                self._show_file_detail_view(file_info['path'])
                return
    
    def _show_file_detail_view(self, file_path: str):
        """显示文件详情视图"""
        if file_path not in self.tracker.data["files"]:
            return
        
        self.in_detail_view = True
        self.current_file = file_path
        
        self.activity_text.pack_forget()
        self.detail_container.pack(fill=tk.BOTH, expand=True)
        self.button_frame.pack(fill=tk.X, pady=5, padx=5)
        self.notes_frame.pack(fill=tk.BOTH, expand=False)
        
        file_info = self.tracker.data["files"][file_path]
        age_days = self.tracker.get_file_age_days(file_path)
        color_segment = self.tracker.get_color_segment(file_path)
        
        self.detail_text.config(state=tk.NORMAL)
        self.detail_text.delete('1.0', tk.END)
        self.notes_text.config(state=tk.NORMAL)
        self.notes_text.delete('1.0', tk.END)
        
        from ..config.settings import StudySettings
        settings = StudySettings()
        intervals = settings.get_time_intervals()
        
        segment_display = {
            'fresh': f'白色 - 0-{intervals["fresh_days"]}天 不需要复习',
            'early': f'浅黄 - {intervals["fresh_days"]}-{intervals["early_days"]}天 需要复习',
            'normal': f'橙色 - {intervals["early_days"]}-{intervals["normal_days"]}天 重点复习',
            'warning': f'番茄红 - {intervals["normal_days"]}-{intervals["warning_days"]}天 警告级',
            'critical': f'深红 - {intervals["warning_days"]}-{intervals["critical_days"]}天 紧急复习',
            'overdue': f'暗红 - {intervals["critical_days"]}+天 已遗忘'
        }
        
        detail_info = f"""文件: {file_path}

创建时间: {file_info.get('created_at', 'N/A')}
最后修改: {file_info.get('last_modified', 'N/A')}
更新次数: {file_info.get('update_count', 0)}
文件大小: {file_info.get('file_size', 0)} 字节
状态: {file_info.get('status', 'N/A')}

复习情况:
  距今: {age_days:.1f}天
  颜色分段: {segment_display.get(color_segment, '未知')}

更新历史（最近10次）:
"""
        self.detail_text.insert(tk.END, detail_info)
        
        timestamps = file_info.get('update_timestamps', [])
        for ts in timestamps[-10:]:
            dt = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            self.detail_text.insert(tk.END, f"  - {dt}\n")
        
        review_records = self.tracker.get_review_records(file_path)
        if review_records:
            self.detail_text.insert(tk.END, f"\n复习记录（最近5条）:\n")
            for record in review_records[:5]:
                record_time = record.get('datetime', 'N/A')
                record_type = record.get('review_type', 'N/A')
                record_notes = record.get('notes', '')
                notes_display = f" - {record_notes}" if record_notes else ""
                self.detail_text.insert(tk.END, f"  {record_time} [{record_type}]{notes_display}\n")
        
        self.detail_text.config(state=tk.DISABLED)
        
        notes = file_info.get('notes', '')
        self.notes_text.insert(tk.END, notes)
        self.notes_text.config(state=tk.NORMAL)
        
        self._refresh_logs()
    
    def _on_tree_double_click(self, event):
        """树形项目双击事件 - 直接打开文件"""
        if not self.tree.selection():
            return
        
        item = self.tree.selection()[0]
        values = self.tree.item(item)
        text = values['text']
        
        for file_info in self.tracker.get_file_list():
            if Path(file_info['path']).name == text:
                file_path = self.root_dir / file_info['path']
                
                if not file_path.exists():
                    messagebox.showerror("错误", "文件不存在")
                    return
                
                try:
                    if platform.system() == 'Windows':
                        os.startfile(str(file_path))
                    elif platform.system() == 'Darwin':
                        subprocess.Popen(['open', str(file_path)])
                    else:
                        subprocess.Popen(['xdg-open', str(file_path)])
                except Exception as e:
                    messagebox.showerror("错误", f"打开文件失败: {str(e)}")
                
                break
    
    def _refresh_logs(self):
        """刷新日记显示"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete('1.0', tk.END)
        
        logs = self.tracker.get_study_logs()
        if not logs:
            self.log_text.insert(tk.END, "暂无学习日记")
            self.log_text.config(state=tk.DISABLED)
            return
        
        grouped_logs = {}
        for log in logs:
            date = log.get('date', '未知日期')
            if date not in grouped_logs:
                grouped_logs[date] = []
            grouped_logs[date].append(log)
        
        for date in sorted(grouped_logs.keys(), reverse=True):
            self.log_text.insert(tk.END, f"\n{date}\n")
            self.log_text.insert(tk.END, "=" * 35 + "\n")
            
            for log in grouped_logs[date]:
                content = log.get('content', '')
                timestamp = log.get('timestamp', 0)
                if timestamp:
                    time_str = datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
                    self.log_text.insert(tk.END, f"[{time_str}] {content}\n\n")
                else:
                    self.log_text.insert(tk.END, f"{content}\n\n")
        
        self.log_text.config(state=tk.DISABLED)
    
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
    
    def _open_study_log(self):
        """打开学习日志窗口"""
        StudyLogWindow(self.window, self.tracker)
    
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
        
        report += "时间分布\n"
        report += "-" * 60 + "\n"
        for range_name, count in stats['by_age_range'].items():
            report += f"{range_name}: {count}\n"
        
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
        item = self.tree.selection()
        if not item:
            item = self.tree.identify('item', event.x, event.y)
            self.tree.selection_set(item)
        
        if not item:
            return
        
        menu = tk.Menu(self.window, tearoff=0)
        menu.add_command(label="忽略此目录", command=self._ignore_selected_directory)
        menu.post(event.x_root, event.y_root)
    
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
