#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模块
"""

import os
import json
from typing import Dict, Any

DEFAULT_CONFIG = {
    "data_dir": "src/arxiv_tracker/data",
    "pdf_storage": "src/arxiv_tracker/data/papers",
    "report_storage": "src/arxiv_tracker/data/reports",
    "cache_storage": "src/arxiv_tracker/data/cache",
    "log_dir": "src/arxiv_tracker/data/logs",
    "categories": ["cs.AI", "cs.LG"],
    "max_workers": 4,
    "timeout": 30,
    "max_retries": 3,
    "cache_ttl": 86400,
    "default_paper_count": 10
}

def load_config(config_path=None) -> Dict[str, Any]:
    """加载配置文件
    
    Args:
        config_path: 配置文件路径
    
    Returns:
        配置字典
    """
    # 首先使用默认配置
    config = DEFAULT_CONFIG.copy()
    
    # 如果指定了配置文件路径
    if config_path and os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            user_config = json.load(f)
            config.update(user_config)
    else:
        # 尝试加载默认配置文件
        default_config_path = os.path.join(
            os.path.dirname(__file__),
            '..',
            '..',
            '..',
            'config',
            'system_config.json'
        )
        
        if os.path.exists(default_config_path):
            with open(default_config_path, 'r', encoding='utf-8') as f:
                system_config = json.load(f)
                config.update(system_config)
    
    # 确保路径是相对路径
    for key in ['data_dir', 'pdf_storage', 'report_storage', 'cache_storage', 'log_dir']:
        if config.get(key) and not config.get(key).startswith('src/'):
            # 如果是绝对路径，转换为相对路径
            config[key] = os.path.relpath(config[key], os.path.dirname(__file__))
    
    return config

def save_config(config: Dict[str, Any], config_path: str):
    """保存配置文件
    
    Args:
        config: 配置字典
        config_path: 保存路径
    """
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def get_config_path() -> str:
    """获取配置文件路径
    
    Returns:
        配置文件路径
    """
    return os.path.join(
        os.path.dirname(__file__),
        '..',
        '..',
        '..',
        'config',
        'system_config.json'
    )
