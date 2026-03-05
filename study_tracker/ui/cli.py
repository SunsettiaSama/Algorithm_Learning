"""
学习追踪系统 - CLI 接口
提供命令行操作
"""

import argparse
import sys
from pathlib import Path
from ..tracker.file_tracker import FileTracker
from datetime import datetime


class CLIInterface:
    """CLI 接口"""
    
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.tracker = FileTracker(str(self.root_dir))
    
    def scan(self):
        """扫描目录并初始化"""
        print("正在扫描目录...")
        result = self.tracker.scan_directory()
        print(f"\n扫描完成!")
        print(f"新文件: {result['new_files']}")
        print(f"更新文件: {result['updated_files']}")
        print(f"总文件数: {result['total_files']}")
        print(f"扫描时间: {result['scanned_at']}")
    
    def status(self):
        """显示学习状态"""
        stats = self.tracker.get_statistics()
        
        print("\n学习进度统计")
        print("=" * 60)
        print(f"总文件数: {stats['total_files']}")
        print(f"活跃文件: {stats['active_files']}")
        print(f"最近更新（1天内）: {stats['recent_updates']}")
        
        print("\n时间分布:")
        print(f"  0-1天: {stats['by_age_range']['0_1days']}")
        print(f"  1-3天: {stats['by_age_range']['1_3days']}")
        print(f"  3-7天: {stats['by_age_range']['3_7days']}")
        print(f"  7-14天: {stats['by_age_range']['7_14days']}")
        print(f"  14-30天: {stats['by_age_range']['14_30days']}")
        print(f"  30天+: {stats['by_age_range']['30+days']}")
    
    def list_files(self, filter_status: str = None, limit: int = 50):
        """列出文件"""
        files = self.tracker.get_file_list()
        
        if filter_status:
            files = [f for f in files if f['status'] == filter_status]
        
        print(f"\n文件列表 (显示前{limit}个)")
        print("=" * 100)
        print(f"{'文件':<50} {'天数':>8} {'次数':>6} {'状态':<10}")
        print("-" * 100)
        
        for file_info in files[:limit]:
            age = file_info.get('age_days')
            age_str = f"{age:.1f}" if age else "N/A"
            status = file_info.get('status', 'N/A')
            
            print(f"{file_info['path']:<50} {age_str:>8} {file_info['update_count']:>6} {status:<10}")
    
    def list_urgent(self):
        """列出需要复习的文件（3-30天内未更新）"""
        urgent = self.tracker.get_urgent_files()
        
        print(f"\n需要紧急复习的文件 (共{len(urgent)}个)")
        print("=" * 100)
        print(f"{'文件':<50} {'天数':>8} {'最后修改':>20}")
        print("-" * 100)
        
        for file_info in urgent:
            age = file_info.get('age_days')
            age_str = f"{age:.1f}" if age else "N/A"
            last_mod = file_info.get('last_modified', 'N/A')
            
            print(f"{file_info['path']:<50} {age_str:>8} {last_mod:>20}")
    
    def update(self, file_path: str):
        """更新文件时间戳"""
        if self.tracker.record_update(file_path):
            print(f"已更新文件: {file_path}")
        else:
            print(f"文件不存在: {file_path}")
    
    def mark_studied(self, file_path: str):
        """标记为已学习"""
        if self.tracker.update_file_status(file_path, "已学习"):
            print(f"已标记为已学习: {file_path}")
        else:
            print(f"文件不存在: {file_path}")
    
    def mark_mastered(self, file_path: str):
        """标记为已掌握"""
        if self.tracker.update_file_status(file_path, "已掌握"):
            print(f"已标记为已掌握: {file_path}")
        else:
            print(f"文件不存在: {file_path}")
    
    def add_ignore(self, pattern: str):
        """添加忽略模式"""
        self.tracker.add_ignore_pattern(pattern)
        print(f"已添加忽略模式: {pattern}")
    
    def export_report(self):
        """导出报告"""
        stats = self.tracker.get_statistics()
        
        report = "学习进度报告\n"
        report += "=" * 60 + "\n"
        report += f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        report += "统计信息\n"
        report += "-" * 60 + "\n"
        report += f"总文件数: {stats['total_files']}\n"
        report += f"活跃文件: {stats['active_files']}\n"
        report += f"最近更新: {stats['recent_updates']}\n"
        report += f"紧急复习: {stats['urgent_count']}\n\n"
        
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
        
        print(f"报告已导出到: {report_path}")


def main():
    parser = argparse.ArgumentParser(
        description="学习进度追踪系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python cli.py --root . scan                  # 扫描目录
  python cli.py --root . status                # 显示状态
  python cli.py --root . list                  # 列出所有文件
  python cli.py --root . urgent                # 列出需要复习的文件
  python cli.py --root . update "file/path.py" # 更新文件时间戳
  python cli.py --root . mark-studied "file/path.py" # 标记为已学习
  python cli.py --root . mark-mastered "file/path.py" # 标记为已掌握
  python cli.py --root . ignore "*.tmp"        # 添加忽略模式
  python cli.py --root . export                # 导出报告
        """
    )
    
    parser.add_argument('--root', default='.', help='追踪的根目录')
    parser.add_argument('command', nargs='?', help='命令')
    parser.add_argument('arg', nargs='?', help='命令参数')
    
    args = parser.parse_args()
    
    cli = CLIInterface(args.root)
    
    if args.command == 'scan':
        cli.scan()
    elif args.command == 'status':
        cli.status()
    elif args.command == 'list':
        cli.list_files()
    elif args.command == 'urgent':
        cli.list_urgent()
    elif args.command == 'update':
        if args.arg:
            cli.update(args.arg)
        else:
            print("需要指定文件路径")
    elif args.command == 'mark-studied':
        if args.arg:
            cli.mark_studied(args.arg)
        else:
            print("需要指定文件路径")
    elif args.command == 'mark-mastered':
        if args.arg:
            cli.mark_mastered(args.arg)
        else:
            print("需要指定文件路径")
    elif args.command == 'ignore':
        if args.arg:
            cli.add_ignore(args.arg)
        else:
            print("需要指定忽略模式")
    elif args.command == 'export':
        cli.export_report()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
