#!/usr/bin/env python3
"""
基础用法示例

这个脚本展示了如何使用arXiv论文跟踪系统的基本功能，包括：
1. 爬取最新论文
2. 下载PDF文件
3. 分析论文
4. 生成报告

用法：
    python examples/basic_usage.py
"""

import os
import sys

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from arxiv_tracker import ArxivTracker
from arxiv_tracker.utils.logger import setup_logger

# 设置日志
logger = setup_logger('basic_usage')


def run_basic_usage():
    """运行基础用法示例"""
    logger.info("开始基础用法示例")
    
    try:
        # 创建跟踪器实例
        tracker = ArxivTracker()
        
        # 1. 运行完整流程
        logger.info("1. 运行完整流程")
        results = tracker.run(
            count=5,  # 处理5篇论文
            categories=['cs.AI', 'cs.LG'],  # 只处理AI和机器学习类别
            use_pdf=True,  # 从PDF提取信息
            date=None  # 使用当前日期
        )
        
        logger.info(f"处理完成，共分析了 {len(results)} 篇论文")
        
        # 2. 查看结果
        logger.info("\n2. 查看结果")
        for i, paper in enumerate(results[:3], 1):  # 只显示前3篇
            logger.info(f"\n=== 论文 {i} ===")
            logger.info(f"标题: {paper.get('title', 'N/A')}")
            logger.info(f"作者: {', '.join(paper.get('authors', ['N/A']))}")
            logger.info(f"论文ID: {paper.get('arxiv_id', 'N/A')}")
            logger.info(f"评分: {paper.get('score', 'N/A')}")
            logger.info(f"PDF路径: {paper.get('pdf_path', 'N/A')}")
        
        # 3. 查看生成的文件
        logger.info("\n3. 查看生成的文件")
        
        # 获取数据目录
        data_dir = tracker.config.get('data_dir', 'src/arxiv_tracker/data')
        papers_dir = os.path.join(data_dir, 'papers')
        reports_dir = os.path.join(data_dir, 'reports')
        logs_dir = os.path.join(data_dir, 'logs')
        
        logger.info(f"PDF文件存储在: {papers_dir}")
        logger.info(f"报告存储在: {reports_dir}")
        logger.info(f"日志存储在: {logs_dir}")
        
        # 检查是否生成了文件
        if os.path.exists(papers_dir):
            paper_count = sum(1 for _ in os.walk(papers_dir) if _.endswith('.pdf'))
            logger.info(f"已下载的PDF文件数量: {paper_count}")
        
        if os.path.exists(reports_dir):
            report_count = sum(1 for _ in os.walk(reports_dir) if _.endswith(('.md', '.json')))
            logger.info(f"已生成的报告数量: {report_count}")
        
        logger.info("基础用法示例完成")
        
    except Exception as e:
        logger.error(f"运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_basic_usage()
