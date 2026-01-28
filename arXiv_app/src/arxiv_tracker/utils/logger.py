#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志管理模块
"""

import os
import logging
import json
from logging.config import dictConfig


def setup_logger(debug=False):
    """设置日志配置
    
    Args:
        debug: 是否启用调试模式
    """
    # 尝试加载日志配置文件
    log_config_path = os.path.join(
        os.path.dirname(__file__),
        '..',
        '..',
        '..',
        'config',
        'logging_config.json'
    )
    
    if os.path.exists(log_config_path):
        with open(log_config_path, 'r', encoding='utf-8') as f:
            log_config = json.load(f)
        
        # 确保日志目录存在
        log_dir = log_config['handlers']['file']['filename']
        log_dir = os.path.dirname(log_dir)
        os.makedirs(log_dir, exist_ok=True)
        
        # 应用配置
        dictConfig(log_config)
    else:
        # 使用默认配置
        default_config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                }
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'level': 'DEBUG' if debug else 'INFO',
                    'formatter': 'standard',
                    'stream': 'ext://sys.stdout'
                },
                'file': {
                    'class': 'logging.FileHandler',
                    'level': 'INFO',
                    'formatter': 'standard',
                    'filename': os.path.join(
                        os.path.dirname(__file__),
                        '..',
                        'data',
                        'logs',
                        'tracker.log'
                    ),
                    'encoding': 'utf-8'
                }
            },
            'loggers': {
                '': {
                    'handlers': ['console', 'file'],
                    'level': 'DEBUG' if debug else 'INFO',
                    'propagate': True
                }
            }
        }
        
        # 确保日志目录存在
        log_file = default_config['handlers']['file']['filename']
        log_dir = os.path.dirname(log_file)
        os.makedirs(log_dir, exist_ok=True)
        
        # 应用默认配置
        dictConfig(default_config)
    
    # 测试日志
    logger = logging.getLogger(__name__)
    logger.info("日志系统初始化完成")
    if debug:
        logger.debug("调试模式已启用")


def get_logger(name=None):
    """获取日志记录器
    
    Args:
        name: 日志名称
    
    Returns:
        日志记录器
    """
    return logging.getLogger(name)
