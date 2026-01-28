#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
arXiv论文跟踪系统 - 命令行接口
"""

import argparse
import logging
import sys
import os

from .utils.config import load_config
from .utils.logger import setup_logger
from .crawler import ArxivCrawler
from .downloader import ArxivDownloader
from .extractor import ArxivExtractor
from .analyzer import ArxivAnalyzer
from .reporter import ArxivReporter

def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description="arXiv论文跟踪和分析系统",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="论文数量"
    )
    
    parser.add_argument(
        "--date",
        type=str,
        default=None,
        help="日期 (YYYYMMDD)"
    )
    
    parser.add_argument(
        "--categories",
        type=str,
        default=None,
        help="论文类别，逗号分隔"
    )
    
    parser.add_argument(
        "--use-pdf",
        action="store_true",
        default=False,
        help="从PDF文件提取信息"
    )
    
    parser.add_argument(
        "--no-download",
        action="store_true",
        default=False,
        help="不下载PDF文件"
    )
    
    parser.add_argument(
        "--no-analysis",
        action="store_true",
        default=False,
        help="不分析论文"
    )
    
    parser.add_argument(
        "--no-report",
        action="store_true",
        default=False,
        help="不生成报告"
    )
    
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="配置文件路径"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="调试模式"
    )
    
    args = parser.parse_args()
    
    # 加载配置
    config = load_config(args.config)
    
    # 覆盖配置
    if args.categories:
        config['categories'] = args.categories.split(',')
    
    # 设置日志
    setup_logger(debug=args.debug)
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("arXiv论文跟踪系统启动")
        logger.info(f"配置: {config}")
        
        # 1. 爬取论文信息
        logger.info("步骤1: 爬取论文信息")
        crawler = ArxivCrawler(config)
        papers = crawler.crawl(date=args.date)
        logger.info(f"成功爬取 {len(papers)} 篇论文")
        
        if not args.no_download:
            # 2. 下载PDF文件
            logger.info("步骤2: 下载PDF文件")
            downloader = ArxivDownloader(config)
            papers = downloader.download(papers, date=args.date)
            logger.info("PDF文件下载完成")
        
        # 3. 提取信息
        logger.info("步骤3: 提取论文信息")
        extractor = ArxivExtractor(config)
        if args.use_pdf:
            papers = extractor.extract_from_pdfs(papers, date=args.date)
        else:
            papers = extractor.extract_from_web(papers)
        logger.info("论文信息提取完成")
        
        if not args.no_analysis:
            # 4. 分析论文
            logger.info("步骤4: 分析论文")
            analyzer = ArxivAnalyzer(config)
            papers = analyzer.analyze(papers)
            logger.info("论文分析完成")
        
        if not args.no_report:
            # 5. 生成报告
            logger.info("步骤5: 生成报告")
            reporter = ArxivReporter(config)
            reporter.generate(papers, date=args.date)
            logger.info("报告生成完成")
        
        logger.info("arXiv论文跟踪系统运行完成")
        
    except Exception as e:
        logger.error(f"运行失败: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()
