#!/usr/bin/env python3
"""
学习追踪系统启动脚本
"""

import sys
from pathlib import Path

if __name__ == "__main__":
    current_dir = Path(__file__).parent
    parent_dir = current_dir.parent
    sys.path.insert(0, str(parent_dir))
    
    from study_tracker.main import main
    sys.exit(main())
