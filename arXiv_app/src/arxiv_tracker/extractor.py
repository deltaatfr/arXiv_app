#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
arXiv论文信息提取模块
"""

import os
import re
import logging
from typing import List, Dict
import PyPDF2

class ArxivExtractor:
    """arXiv论文信息提取器"""
    
    def __init__(self, config):
        """初始化提取器"""
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def extract_from_pdfs(self, papers, date=None):
        """从PDF文件中提取信息"""
        if not papers:
            return papers
        
        # 获取PDF目录
        pdf_dir = os.path.join(
            os.path.dirname(__file__),
            '..',
            self.config.get('pdf_storage', 'data/papers')
        )
        
        if date:
            pdf_dir = os.path.join(pdf_dir, date)
        else:
            from datetime import datetime
            pdf_dir = os.path.join(pdf_dir, datetime.now().strftime('%Y%m%d'))
        
        self.logger.info(f"从PDF文件中提取信息: {pdf_dir}")
        
        for paper in papers:
            arxiv_id = paper.get('arxiv_id')
            if not arxiv_id:
                self.logger.warning("跳过无arxiv_id的论文")
                continue
            
            # 构建PDF文件路径
            pdf_filename = f"{arxiv_id}.pdf"
            pdf_path = os.path.join(pdf_dir, pdf_filename)
            
            if not os.path.exists(pdf_path):
                self.logger.warning(f"PDF文件不存在: {pdf_path}")
                continue
            
            try:
                self.logger.info(f"处理论文: {paper.get('title', 'Unknown')}")
                
                # 从PDF文件中提取文本
                with open(pdf_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    text = ""
                    # 读取前5页（摘要通常在前几页）
                    for page_num in range(min(5, len(reader.pages))):
                        page = reader.pages[page_num]
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text
                
                if not text:
                    self.logger.warning(f"无法从PDF文件中提取文本: {arxiv_id}")
                    continue
                
                # 提取标题
                title = self._extract_title(text)
                if title:
                    paper['title'] = title
                    self.logger.info(f"成功提取标题: {title[:50]}...")
                
                # 提取作者
                authors = self._extract_authors(text)
                if authors:
                    paper['authors'] = authors
                    self.logger.info(f"成功提取作者: {authors[:2]}...")
                
                # 提取摘要
                abstract = self._extract_abstract(text)
                if abstract:
                    paper['abstract'] = abstract
                    self.logger.info(f"成功提取摘要: {abstract[:100]}...")
                
            except Exception as e:
                self.logger.error(f"从PDF文件中提取信息失败: {arxiv_id} - {e}")
                import traceback
                self.logger.error(traceback.format_exc())
        
        return papers
    
    def extract_from_web(self, papers):
        """从网页信息中提取信息"""
        # 这里可以实现从网页HTML中提取更详细的信息
        # 目前我们假设爬取时已经提取了基本信息
        return papers
    
    def _extract_title(self, text):
        """从文本中提取标题"""
        # 尝试不同的标题提取模式
        patterns = [
            r'\bTitle\b[:\s]+([\s\S]+?)\bAuthors\b',
            r'([\s\S]{10,200})\n\n\b[A-Z][a-z]+\s+[A-Z][a-z]+',
            r'^([\s\S]{10,200})\n\n',
            r'\bAbstract\b[:\s]+([\s\S]+?)\b1\b\.',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                if len(title) > 10 and len(title) < 200:
                    return title
        
        return None
    
    def _extract_authors(self, text):
        """从文本中提取作者"""
        patterns = [
            r'\bAuthors\b[:\s]+([\s\S]+?)\bAbstract\b',
            r'\bAuthor\b[:\s]+([\s\S]+?)\bAbstract\b',
            r'\bby\b[:\s]+([\s\S]+?)\bAbstract\b',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                authors_text = match.group(1).strip()
                # 处理作者列表
                authors = self._parse_authors(authors_text)
                if authors:
                    return authors
        
        return []
    
    def _extract_abstract(self, text):
        """从文本中提取摘要"""
        patterns = [
            r'\bAbstract\b[:\s]+([\s\S]+?)(?:\b1\b\.|\bIntroduction\b|\bReferences\b|$)',
            r'\bABSTRACT\b[:\s]+([\s\S]+?)(?:\b1\b\.|\bINTRODUCTION\b|\bREFERENCES\b|$)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                abstract = match.group(1).strip()
                if len(abstract) > 50:
                    return abstract
        
        # 如果没有找到明确的摘要标记，尝试提取前1000字符
        if len(text) > 1000:
            return text[:1000].strip()
        
        return None
    
    def _parse_authors(self, authors_text):
        """解析作者文本为作者列表"""
        # 分割作者
        authors = []
        
        # 尝试不同的分割方式
        separators = [',', 'and', ';']
        
        for sep in separators:
            parts = re.split(f'\s*{re.escape(sep)}\s*', authors_text)
            if len(parts) > 1:
                for part in parts:
                    part = part.strip()
                    if part and len(part) > 2:
                        authors.append(part)
                break
        
        # 如果没有分割成功，返回原始文本作为单个作者
        if not authors and authors_text:
            authors = [authors_text.strip()]
        
        return authors
