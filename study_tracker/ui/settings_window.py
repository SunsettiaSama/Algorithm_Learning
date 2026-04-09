"""
学习追踪系统 - 设置窗口
提供设置界面用于配置学习参数
"""

import tkinter as tk
from tkinter import ttk, messagebox
from ..config.settings import StudySettings


class SettingsWindow:
    """设置窗口"""
    
    def __init__(self, parent, settings: StudySettings):
        """
        初始化设置窗口
        
        Args:
            parent: 父窗口
            settings: 设置管理器实例
        """
        self.settings = settings
        self.window = tk.Toplevel(parent)
        self.window.title("学习设置")
        self.window.geometry("500x600")
        self.window.resizable(False, False)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """设置UI"""
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        intervals_frame = ttk.Frame(notebook)
        notebook.add(intervals_frame, text="权重分数阈值")
        self._setup_intervals_tab(intervals_frame)
        
        review_frame = ttk.Frame(notebook)
        notebook.add(review_frame, text="复习周期")
        self._setup_review_tab(review_frame)
        
        mastery_frame = ttk.Frame(notebook)
        notebook.add(mastery_frame, text="掌握度")
        self._setup_mastery_tab(mastery_frame)
        
        ignore_frame = ttk.Frame(notebook)
        notebook.add(ignore_frame, text="忽略设置")
        self._setup_ignore_tab(ignore_frame)
        
        advanced_frame = ttk.Frame(notebook)
        notebook.add(advanced_frame, text="高级设置")
        self._setup_advanced_tab(advanced_frame)
        
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="保存设置", command=self._save_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="重置默认", command=self._reset_defaults).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="关闭", command=self.window.destroy).pack(side=tk.RIGHT, padx=5)
    
    def _setup_intervals_tab(self, parent):
        """设置权重分数阈值标签"""
        settings_data = self.settings.get_score_thresholds()

        frame = ttk.LabelFrame(parent, text="权重分数区间配置（0.0-1.0）", padding=10)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(frame, text="不需要复习（分数上限）:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.fresh_var = tk.StringVar(value=str(settings_data.get('fresh_max', 0.2)))
        ttk.Entry(frame, textvariable=self.fresh_var, width=20).grid(row=0, column=1, padx=10, pady=5)
        ttk.Label(frame, text="白色 | 分数 < fresh_max", foreground="gray", font=("Arial", 8)).grid(row=0, column=2, padx=5)

        ttk.Label(frame, text="需要复习（分数上限）:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.early_var = tk.StringVar(value=str(settings_data.get('early_max', 0.4)))
        ttk.Entry(frame, textvariable=self.early_var, width=20).grid(row=1, column=1, padx=10, pady=5)
        ttk.Label(frame, text="浅黄 | fresh_max ~ early_max", foreground="gray", font=("Arial", 8)).grid(row=1, column=2, padx=5)

        ttk.Label(frame, text="重点复习（分数上限）:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.normal_var = tk.StringVar(value=str(settings_data.get('normal_max', 0.6)))
        ttk.Entry(frame, textvariable=self.normal_var, width=20).grid(row=2, column=1, padx=10, pady=5)
        ttk.Label(frame, text="橙色 | early_max ~ normal_max", foreground="gray", font=("Arial", 8)).grid(row=2, column=2, padx=5)

        ttk.Label(frame, text="警告级（分数上限）:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.warning_var = tk.StringVar(value=str(settings_data.get('warning_max', 0.8)))
        ttk.Entry(frame, textvariable=self.warning_var, width=20).grid(row=3, column=1, padx=10, pady=5)
        ttk.Label(frame, text="番茄红 | normal_max ~ warning_max", foreground="gray", font=("Arial", 8)).grid(row=3, column=2, padx=5)

        ttk.Label(frame, text="紧急复习（分数上限）:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.critical_var = tk.StringVar(value=str(settings_data.get('critical_max', 1.0)))
        ttk.Entry(frame, textvariable=self.critical_var, width=20).grid(row=4, column=1, padx=10, pady=5)
        ttk.Label(frame, text="深红 | warning_max ~ critical_max", foreground="gray", font=("Arial", 8)).grid(row=4, column=2, padx=5)

        ttk.Label(frame, text="暗红 | 分数 >= critical_max → 已遗忘",
                  foreground="gray", font=("Arial", 8)).grid(row=5, column=0, columnspan=3, pady=10)
    
    def _setup_review_tab(self, parent):
        """设置复习周期标签"""
        settings_data = self.settings.get_review_schedule()
        
        frame = ttk.LabelFrame(parent, text="设置复习周期", padding=10)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(frame, text="第一次复习（小时）:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.first_var = tk.StringVar(value=str(settings_data.get('first_review_hours', 1)))
        ttk.Entry(frame, textvariable=self.first_var, width=20).grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(frame, text="第二次复习（小时）:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.second_var = tk.StringVar(value=str(settings_data.get('second_review_hours', 24)))
        ttk.Entry(frame, textvariable=self.second_var, width=20).grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(frame, text="第三次复习（小时）:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.third_var = tk.StringVar(value=str(settings_data.get('third_review_hours', 72)))
        ttk.Entry(frame, textvariable=self.third_var, width=20).grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(frame, text="这些设置用于计算建议的复习时间", font=("Arial", 9, "italic")).grid(row=3, column=0, columnspan=2, pady=10)
    
    def _setup_mastery_tab(self, parent):
        """设置掌握度标签"""
        settings_data = self.settings.get_mastery_weights()
        
        frame = ttk.LabelFrame(parent, text="掌握度计算权重", padding=10)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(frame, text="复习次数权重 (0.0-1.0):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.update_count_var = tk.StringVar(value=str(settings_data.get('update_count_weight', 0.6)))
        ttk.Entry(frame, textvariable=self.update_count_var, width=20).grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(frame, text="时间权重 (0.0-1.0):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.time_weight_var = tk.StringVar(value=str(settings_data.get('time_weight', 0.4)))
        ttk.Entry(frame, textvariable=self.time_weight_var, width=20).grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(frame, text="权重越高，对颜色影响越大", font=("Arial", 9, "italic")).grid(row=2, column=0, columnspan=2, pady=10)
        
        info_text = """
掌握度 = 复习次数权重 × 更新次数 + 时间权重 × 距今天数

例如：
- 权重都为0.5，则掌握度等于两者的平均值
- 权重0.6和0.4，则更重视复习次数
        """.strip()
        ttk.Label(frame, text=info_text, justify=tk.LEFT, font=("Arial", 9)).grid(row=3, column=0, columnspan=2, pady=10)
    
    def _setup_advanced_tab(self, parent):
        """设置高级选项标签"""
        frame = ttk.LabelFrame(parent, text="高级设置（开发中）", padding=10)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(frame, text="⏳ 艾宾浩斯遗忘曲线", foreground="gray").pack(anchor=tk.W, pady=5)
        ttk.Label(frame, text="   根据遗忘曲线自动调整复习周期", foreground="gray", font=("Arial", 9)).pack(anchor=tk.W, pady=5)
        
        ttk.Label(frame, text="⏳ 自适应调度", foreground="gray").pack(anchor=tk.W, pady=10)
        ttk.Label(frame, text="   根据学习速率动态调整复习计划", foreground="gray", font=("Arial", 9)).pack(anchor=tk.W, pady=5)
        
        ttk.Label(frame, text="⏳ 机器学习预测", foreground="gray").pack(anchor=tk.W, pady=10)
        ttk.Label(frame, text="   使用ML模型预测最优复习时间", foreground="gray", font=("Arial", 9)).pack(anchor=tk.W, pady=5)
        
        ttk.Label(frame, text="\n这些功能正在开发中，敬请期待", font=("Arial", 10, "italic")).pack(pady=20)
    
    def _save_settings(self):
        """保存设置"""
        try:
            first_hours = int(self.first_var.get())
            second_hours = int(self.second_var.get())
            third_hours = int(self.third_var.get())

            fresh_max = float(self.fresh_var.get())
            early_max = float(self.early_var.get())
            normal_max = float(self.normal_var.get())
            warning_max = float(self.warning_var.get())
            critical_max = float(self.critical_var.get())

            update_count_weight = float(self.update_count_var.get())
            time_weight = float(self.time_weight_var.get())

            if not (0 <= update_count_weight <= 1) or not (0 <= time_weight <= 1):
                messagebox.showerror("错误", "权重必须在 0.0 到 1.0 之间")
                return

            if first_hours <= 0 or second_hours <= 0 or third_hours <= 0:
                messagebox.showerror("错误", "复习时间必须为正数")
                return

            if not (0 <= fresh_max < early_max < normal_max < warning_max < critical_max <= 150):
                messagebox.showerror("错误", "分数阈值必须在 0-150 之间且依次递增（艾宾浩斯量程）")
                return

            self.settings.set_review_schedule(first_hours, second_hours, third_hours)
            self.settings.set_score_thresholds(fresh_max, early_max, normal_max, warning_max, critical_max)
            self.settings.set_mastery_weights(update_count_weight, time_weight)

            extensions = [line.strip() for line in self.ignore_extensions_text.get("1.0", tk.END).split("\n") if line.strip()]
            directories = [line.strip() for line in self.ignore_directories_text.get("1.0", tk.END).split("\n") if line.strip()]

            self.settings.set_ignore_extensions(extensions)
            self.settings.set_ignore_directories(directories)

            messagebox.showinfo("成功", "设置已保存")
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数值")
    
    def _reset_defaults(self):
        """重置为默认设置"""
        if messagebox.askyesno("确认", "确定要重置为默认设置吗？"):
            self.settings.reset_to_default()
            self.window.destroy()
            messagebox.showinfo("成功", "已重置为默认设置")
    
    def _setup_ignore_tab(self, parent):
        """设置忽略配置标签"""
        ignore_config = self.settings.get_ignore_settings()
        
        frame = ttk.LabelFrame(parent, text="文件后缀忽略", padding=10)
        frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
        
        ttk.Label(frame, text="要忽略的文件后缀 (每行一个，含点号)", font=("Arial", 9)).pack(anchor=tk.W, pady=5)
        
        extensions = ignore_config.get("ignore_extensions", [])
        self.ignore_extensions_var = tk.StringVar(value="\n".join(extensions))
        
        ext_text = tk.Text(frame, width=40, height=6, wrap=tk.WORD)
        ext_text.pack(fill=tk.BOTH, expand=True, pady=5)
        ext_text.insert("1.0", self.ignore_extensions_var.get())
        self.ignore_extensions_text = ext_text
        
        dir_frame = ttk.LabelFrame(parent, text="目录忽略", padding=10)
        dir_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
        
        ttk.Label(dir_frame, text="要忽略的目录名 (每行一个)", font=("Arial", 9)).pack(anchor=tk.W, pady=5)
        
        directories = ignore_config.get("ignore_directories", [])
        self.ignore_directories_var = tk.StringVar(value="\n".join(directories))
        
        dir_text = tk.Text(dir_frame, width=40, height=6, wrap=tk.WORD)
        dir_text.pack(fill=tk.BOTH, expand=True, pady=5)
        dir_text.insert("1.0", self.ignore_directories_var.get())
        self.ignore_directories_text = dir_text
