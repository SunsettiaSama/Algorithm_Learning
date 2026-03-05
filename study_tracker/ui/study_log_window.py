"""
学习日志窗口 - 记录每日学习内容
提供子窗口界面用于管理学习日志
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from pathlib import Path
import os


class StudyLogWindow:
    """学习日志子窗口"""
    
    def __init__(self, parent, tracker):
        """
        初始化学习日志窗口
        
        Args:
            parent: 父窗口
            tracker: FileTracker 实例
        """
        self.tracker = tracker
        self.window = tk.Toplevel(parent)
        self.window.title("学习日志")
        self.window.geometry("900x700")
        self.window.resizable(True, True)
        
        self.colors = {
            'bg_main': '#f5f5f5',
            'bg_input': '#ffffff',
            'bg_header': '#2c3e50',
            'text_header': '#ffffff',
            'accent': '#3498db'
        }
        
        self._setup_ui()
        self._load_today_logs()
    
    def _setup_ui(self):
        """设置UI"""
        self.window.configure(bg=self.colors['bg_main'])
        
        header_frame = tk.Frame(self.window, bg=self.colors['bg_header'], height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame, 
            text="📔 学习日志",
            font=("Arial", 18, "bold"),
            bg=self.colors['bg_header'],
            fg=self.colors['text_header']
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=15)
        
        subtitle_label = tk.Label(
            header_frame,
            text="记录每日学习进度",
            font=("Arial", 10),
            bg=self.colors['bg_header'],
            fg=self.colors['text_header']
        )
        subtitle_label.pack(side=tk.LEFT, padx=5)
        
        main_frame = tk.Frame(self.window, bg=self.colors['bg_main'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        container = ttk.Frame(main_frame)
        container.pack(fill=tk.BOTH, expand=True)
        
        left_panel = ttk.Frame(container)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        input_label = tk.Label(
            left_panel,
            text="今天学习了什么?",
            font=("Arial", 12, "bold"),
            bg=self.colors['bg_main']
        )
        input_label.pack(anchor=tk.W, pady=(0, 8))
        
        input_bg_frame = tk.Frame(left_panel, bg='white', relief=tk.SUNKEN, bd=1)
        input_bg_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        scrollbar_input = ttk.Scrollbar(input_bg_frame)
        scrollbar_input.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.input_text = tk.Text(
            input_bg_frame,
            wrap=tk.WORD,
            yscrollcommand=scrollbar_input.set,
            height=12,
            font=("Arial", 10),
            bg=self.colors['bg_input'],
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=10
        )
        self.input_text.pack(fill=tk.BOTH, expand=True)
        scrollbar_input.config(command=self.input_text.yview)
        
        self.input_text.bind('<Control-Return>', lambda e: self._save_log())
        
        control_frame = tk.Frame(left_panel, bg=self.colors['bg_main'])
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        save_btn = tk.Button(
            control_frame,
            text="保存日志 (Ctrl+Enter)",
            command=self._save_log,
            bg=self.colors['accent'],
            fg='white',
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            relief=tk.FLAT,
            cursor='hand2'
        )
        save_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        clear_btn = tk.Button(
            control_frame,
            text="清空",
            command=self._clear_input,
            bg='#95a5a6',
            fg='white',
            font=("Arial", 10),
            padx=15,
            pady=8,
            relief=tk.FLAT,
            cursor='hand2'
        )
        clear_btn.pack(side=tk.LEFT)
        
        date_frame = tk.Frame(left_panel, bg=self.colors['bg_main'])
        date_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(date_frame, text="日期:", font=("Arial", 10), bg=self.colors['bg_main']).pack(side=tk.LEFT, padx=(0, 5))
        
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        date_entry = ttk.Entry(date_frame, textvariable=self.date_var, width=12)
        date_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        query_btn = tk.Button(
            date_frame,
            text="查看",
            command=self._load_logs_by_date,
            bg=self.colors['accent'],
            fg='white',
            font=("Arial", 9),
            padx=10,
            pady=5,
            relief=tk.FLAT,
            cursor='hand2'
        )
        query_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        today_btn = tk.Button(
            date_frame,
            text="今天",
            command=self._load_today_logs,
            bg='#27ae60',
            fg='white',
            font=("Arial", 9),
            padx=10,
            pady=5,
            relief=tk.FLAT,
            cursor='hand2'
        )
        today_btn.pack(side=tk.LEFT)
        
        right_panel = ttk.Frame(container, width=350)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        right_panel.pack_propagate(False)
        
        history_label = tk.Label(
            right_panel,
            text="📅 今日日志",
            font=("Arial", 12, "bold"),
            bg=self.colors['bg_main']
        )
        history_label.pack(anchor=tk.W, pady=(0, 8))
        
        history_bg_frame = tk.Frame(right_panel, bg='white', relief=tk.SUNKEN, bd=1)
        history_bg_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar_h = ttk.Scrollbar(history_bg_frame)
        scrollbar_h.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_text = tk.Text(
            history_bg_frame,
            wrap=tk.WORD,
            yscrollcommand=scrollbar_h.set,
            state=tk.DISABLED,
            font=("Arial", 9),
            bg=self.colors['bg_input'],
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=10
        )
        self.history_text.pack(fill=tk.BOTH, expand=True)
        scrollbar_h.config(command=self.history_text.yview)
    
    def _save_log(self):
        """保存日志"""
        content = self.input_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("提示", "请输入学习内容")
            return
        
        date = self.date_var.get()
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("错误", "日期格式不正确，请使用 YYYY-MM-DD 格式")
            return
        
        if self.tracker.add_study_log(content, date):
            messagebox.showinfo("成功", "学习日志已保存")
            self._clear_input()
            self._load_logs_by_date()
        else:
            messagebox.showerror("错误", "保存失败")
    
    def _clear_input(self):
        """清空输入框"""
        self.input_text.delete("1.0", tk.END)
    
    def _load_today_logs(self):
        """加载今天的日志"""
        today = datetime.now().strftime("%Y-%m-%d")
        self.date_var.set(today)
        self._load_logs_by_date()
    
    def _load_logs_by_date(self):
        """根据日期加载日志"""
        date = self.date_var.get()
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("错误", "日期格式不正确，请使用 YYYY-MM-DD 格式")
            return
        
        logs = self.tracker.get_study_logs(date)
        
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete("1.0", tk.END)
        
        if logs:
            for i, log in enumerate(logs, 1):
                timestamp = log.get("timestamp", 0)
                time_str = datetime.fromtimestamp(timestamp).strftime("%H:%M:%S")
                header = f"[{log['date']} {time_str}]\n"
                self.history_text.insert(tk.END, header)
                self.history_text.insert(tk.END, log["content"] + "\n")
                if i < len(logs):
                    self.history_text.insert(tk.END, "-" * 50 + "\n")
        else:
            self.history_text.insert(tk.END, "暂无日志记录")
        
        self.history_text.config(state=tk.DISABLED)
