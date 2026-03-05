"""
学习追踪系统 - 主入口
支持 GUI 和 CLI 两种模式
"""

import sys
import argparse
from pathlib import Path

try:
    from .ui.gui import StudyTrackerGUI
    from .ui.cli import CLIInterface
except ImportError:
    from ui.gui import StudyTrackerGUI
    from ui.cli import CLIInterface


def main():
    parser = argparse.ArgumentParser(
        description="学习进度追踪系统",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--root', default=None, help='追踪的根目录，默认为脚本父目录')
    parser.add_argument('--gui', action='store_true', help='启动 GUI 界面（默认）')
    parser.add_argument('--cli', action='store_true', help='使用 CLI 接口')
    parser.add_argument('command', nargs='?', help='CLI 命令')
    parser.add_argument('arg', nargs='?', help='命令参数')
    
    args = parser.parse_args()
    
    if args.root:
        root_dir = args.root
    else:
        root_dir = str(Path(__file__).parent.parent)
    
    print(f"追踪目录: {root_dir}")
    
    if args.cli or args.command:
        cli = CLIInterface(root_dir)
        
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
            print("未知命令，使用 'python main.py --help' 查看帮助")
    else:
        app = StudyTrackerGUI(root_dir)
        app.run()


if __name__ == "__main__":
    main()
