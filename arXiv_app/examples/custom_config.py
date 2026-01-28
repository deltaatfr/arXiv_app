#!/usr/bin/env python3
"""
自定义配置示例

这个脚本展示了如何使用自定义配置运行arXiv论文跟踪系统，包括：
1. 加载自定义配置文件
2. 运行特定类别的论文分析
3. 自定义输出目录
4. 调整系统参数

用法：
    python examples/custom_config.py
"""

import os
import sys
import json

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from arxiv_tracker import ArxivTracker
from arxiv_tracker.utils.config import load_config, save_config
from arxiv_tracker.utils.logger import setup_logger

# 设置日志
logger = setup_logger('custom_config')


def create_custom_config():
    """创建自定义配置"""
    # 基础配置
    config = {
        "system": {
            "data_dir": "custom_data",  # 自定义数据目录
            "pdf_storage": "custom_data/papers",
            "report_storage": "custom_data/reports",
            "cache_storage": "custom_data/cache",
            "log_dir": "custom_data/logs",
            "categories": ["cs.CV", "cs.CL"],  # 计算机视觉和计算语言学
            "max_workers": 2,  # 减少并发数，适合低配置机器
            "timeout": 45,  # 增加超时时间
            "max_retries": 3,
            "cache_ttl": 86400,
            "default_paper_count": 5
        },
        "api": {
            "dashscope_api_key": "YOUR_API_KEY_HERE",
            "api_endpoint": "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
            "max_retries": 3,
            "timeout": 90,  # 增加API超时时间
            "model": "qwen-plus",
            "temperature": 0.2,  # 降低随机性，提高稳定性
            "top_p": 0.7
        }
    }
    
    # 创建配置文件目录
    config_dir = os.path.join(os.path.dirname(__file__), '..', 'config', 'custom')
    os.makedirs(config_dir, exist_ok=True)
    
    # 保存系统配置
    system_config_path = os.path.join(config_dir, 'system_config.json')
    with open(system_config_path, 'w', encoding='utf-8') as f:
        json.dump(config['system'], f, ensure_ascii=False, indent=2)
    
    # 保存API配置
    api_config_path = os.path.join(config_dir, 'api_config.json')
    with open(api_config_path, 'w', encoding='utf-8') as f:
        json.dump(config['api'], f, ensure_ascii=False, indent=2)
    
    logger.info(f"自定义配置已保存到: {config_dir}")
    return config_dir


def run_custom_config():
    """运行自定义配置示例"""
    logger.info("开始自定义配置示例")
    
    try:
        # 1. 创建自定义配置
        logger.info("1. 创建自定义配置")
        custom_config_dir = create_custom_config()
        
        # 2. 检查API密钥
        api_config_path = os.path.join(custom_config_dir, 'api_config.json')
        with open(api_config_path, 'r', encoding='utf-8') as f:
            api_config = json.load(f)
        
        if api_config.get('dashscope_api_key') == 'YOUR_API_KEY_HERE':
            logger.warning("API密钥尚未配置，请在运行前修改 config/custom/api_config.json 文件")
            logger.warning("将使用默认配置继续...")
            # 使用默认配置
            custom_config_dir = None
        
        # 3. 创建跟踪器实例（使用自定义配置）
        logger.info("2. 创建跟踪器实例")
        tracker = ArxivTracker(config_dir=custom_config_dir)
        
        # 4. 运行系统
        logger.info("3. 运行系统")
        results = tracker.run(
            count=3,  # 只处理3篇论文
            categories=['cs.CV', 'cs.CL'],  # 只处理计算机视觉和计算语言学
            use_pdf=True,  # 从PDF提取信息
            date=None  # 使用当前日期
        )
        
        logger.info(f"处理完成，共分析了 {len(results)} 篇论文")
        
        # 5. 查看结果
        logger.info("\n4. 查看结果")
        for i, paper in enumerate(results, 1):
            logger.info(f"\n=== 论文 {i} ===")
            logger.info(f"标题: {paper.get('title', 'N/A')}")
            logger.info(f"类别: {paper.get('category', 'N/A')}")
            logger.info(f"评分: {paper.get('score', 'N/A')}")
            logger.info(f"PDF路径: {paper.get('pdf_path', 'N/A')}")
        
        # 6. 查看自定义数据目录
        logger.info("\n5. 查看自定义数据目录")
        if custom_config_dir:
            data_dir = tracker.config.get('data_dir', 'custom_data')
            logger.info(f"自定义数据目录: {data_dir}")
            
            # 检查目录是否创建
            if os.path.exists(data_dir):
                logger.info("自定义数据目录已创建")
                
                # 检查子目录
                subdirs = ['papers', 'reports', 'cache', 'logs']
                for subdir in subdirs:
                    dir_path = os.path.join(data_dir, subdir)
                    if os.path.exists(dir_path):
                        logger.info(f"  - {subdir}: 已创建")
                    else:
                        logger.warning(f"  - {subdir}: 未创建")
        
        logger.info("自定义配置示例完成")
        
    except Exception as e:
        logger.error(f"运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_custom_config()
