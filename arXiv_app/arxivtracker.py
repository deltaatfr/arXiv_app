#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
arXiv论文跟踪系统 - 命令行入口
"""

import sys
import os
import argparse

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from arxiv_tracker import main

if __name__ == "__main__":
    main()
