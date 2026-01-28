#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
状态重置脚本
"""

import os
import sys
import logging

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from arxiv_tracker.utils.state_manager import get_state_manager
from arxiv_tracker.utils.cache_manager import get_cache_manager

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def reset_all_states():
    """重置所有状态"""
    logger.info("开始重置所有状态")
    
    # 重置状态管理器
    state_manager = get_state_manager()
    state_manager.reset()
    logger.info("系统状态已重置")
    
    # 重置缓存管理器
    cache_manager = get_cache_manager()
    cache_manager.clear()
    logger.info("系统缓存已清空")
    
    # 清理日志文件
    log_dir = os.path.join(
        os.path.dirname(__file__),
        '..',
        'src',
        'arxiv_tracker',
        'data',
        'logs'
    )
    
    if os.path.exists(log_dir):
        for log_file in os.listdir(log_dir):
            if log_file.endswith('.log'):
                log_path = os.path.join(log_dir, log_file)
                try:
                    os.remove(log_path)
                    logger.info(f"日志文件已清理: {log_file}")
                except Exception as e:
                    logger.error(f"清理日志文件失败 {log_file}: {e}")
    
    logger.info("所有状态已重置完成")

def reset_specific_step(step):
    """重置指定步骤
    
    Args:
        step: 步骤名称
    """
    logger.info(f"开始重置步骤: {step}")
    
    state_manager = get_state_manager()
    state_manager.reset_step(step)
    
    logger.info(f"步骤 {step} 已重置")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="重置系统状态")
    parser.add_argument(
        '--step',
        type=str,
        default=None,
        help="指定要重置的步骤"
    )
    
    args = parser.parse_args()
    
    if args.step:
        reset_specific_step(args.step)
    else:
        reset_all_states()

if __name__ == "__main__":
    main()
