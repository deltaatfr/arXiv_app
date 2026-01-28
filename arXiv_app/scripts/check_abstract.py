#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
摘要检查脚本
"""

import os
import sys
import logging

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from arxiv_tracker.extractor import ArxivExtractor
from arxiv_tracker.utils.config import load_config

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_abstract_extraction():
    """测试摘要提取"""
    logger.info("开始测试摘要提取功能")
    
    # 加载配置
    config = load_config()
    
    # 创建提取器
    extractor = ArxivExtractor(config)
    
    # 测试论文数据
    test_papers = [
        {
            'arxiv_id': '2301.00001',
            'title': 'Test Paper Title',
            'authors': ['John Doe', 'Jane Smith'],
            'abstract': 'This is a test abstract for the paper.'
        }
    ]
    
    # 测试从PDF提取
    logger.info("测试从PDF提取功能")
    # 注意：这里需要实际的PDF文件才能测试
    # papers_from_pdf = extractor.extract_from_pdfs(test_papers)
    # logger.info(f"从PDF提取结果: {papers_from_pdf}")
    
    # 测试从网页提取
    logger.info("测试从网页提取功能")
    papers_from_web = extractor.extract_from_web(test_papers)
    logger.info(f"从网页提取结果: {papers_from_web}")
    
    logger.info("摘要提取测试完成")

def main():
    """主函数"""
    test_abstract_extraction()

if __name__ == "__main__":
    main()
