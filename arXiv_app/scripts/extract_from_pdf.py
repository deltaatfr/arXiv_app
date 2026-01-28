#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF信息提取脚本
"""

import os
import sys
import logging
from typing import List, Dict, Any

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

def extract_from_pdf(pdf_path: str) -> Dict[str, Any]:
    """从单个PDF文件提取信息
    
    Args:
        pdf_path: PDF文件路径
    
    Returns:
        提取的信息
    """
    logger.info(f"开始从PDF文件提取信息: {pdf_path}")
    
    # 加载配置
    config = load_config()
    
    # 创建提取器
    extractor = ArxivExtractor(config)
    
    # 构建论文对象
    arxiv_id = os.path.basename(pdf_path).replace('.pdf', '')
    paper = {
        'arxiv_id': arxiv_id,
        'pdf_path': pdf_path
    }
    
    try:
        # 从PDF文件中提取文本
        import PyPDF2
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            # 读取前5页
            for page_num in range(min(5, len(reader.pages))):
                page = reader.pages[page_num]
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        
        if not text:
            logger.warning("无法从PDF文件中提取文本")
            return paper
        
        # 提取信息
        title = extractor._extract_title(text)
        authors = extractor._extract_authors(text)
        abstract = extractor._extract_abstract(text)
        
        # 更新论文信息
        if title:
            paper['title'] = title
            logger.info(f"成功提取标题: {title[:50]}...")
        
        if authors:
            paper['authors'] = authors
            logger.info(f"成功提取作者: {authors[:2]}...")
        
        if abstract:
            paper['abstract'] = abstract
            logger.info(f"成功提取摘要: {abstract[:100]}...")
        
    except Exception as e:
        logger.error(f"从PDF文件中提取信息失败: {e}")
        import traceback
        logger.error(traceback.format_exc())
    
    return paper

def batch_extract(pdf_dir: str) -> List[Dict[str, Any]]:
    """批量从PDF文件提取信息
    
    Args:
        pdf_dir: PDF文件目录
    
    Returns:
        提取的信息列表
    """
    logger.info(f"开始批量从PDF文件提取信息: {pdf_dir}")
    
    results = []
    
    if os.path.exists(pdf_dir):
        for filename in os.listdir(pdf_dir):
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(pdf_dir, filename)
                result = extract_from_pdf(pdf_path)
                results.append(result)
    else:
        logger.error(f"PDF目录不存在: {pdf_dir}")
    
    logger.info(f"批量提取完成，处理了 {len(results)} 个PDF文件")
    return results

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="从PDF文件提取信息")
    parser.add_argument(
        'path',
        type=str,
        help="PDF文件路径或目录"
    )
    
    args = parser.parse_args()
    
    if os.path.isfile(args.path) and args.path.endswith('.pdf'):
        # 处理单个文件
        result = extract_from_pdf(args.path)
        logger.info(f"提取结果: {result}")
    elif os.path.isdir(args.path):
        # 处理目录
        results = batch_extract(args.path)
        logger.info(f"共提取 {len(results)} 个PDF文件")
    else:
        logger.error("无效的路径，请提供PDF文件或目录")

if __name__ == "__main__":
    main()
