#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
arXiv论文下载模块
"""

import os
import logging
import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict

class ArxivDownloader:
    """arXiv论文下载器"""
    
    def __init__(self, config):
        """初始化下载器"""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # 确保下载目录存在
        self.pdf_dir = os.path.join(
            os.path.dirname(__file__),
            '..',
            self.config.get('pdf_storage', 'data/papers')
        )
        os.makedirs(self.pdf_dir, exist_ok=True)
    
    def download(self, papers, date=None):
        """下载论文PDF文件"""
        if not papers:
            return papers
        
        # 创建日期子目录
        if date:
            download_dir = os.path.join(self.pdf_dir, date)
        else:
            from datetime import datetime
            download_dir = os.path.join(self.pdf_dir, datetime.now().strftime('%Y%m%d'))
        
        os.makedirs(download_dir, exist_ok=True)
        
        self.logger.info(f"PDF文件将下载到: {download_dir}")
        
        # 使用线程池并发下载
        max_workers = self.config.get('max_workers', 4)
        downloaded_papers = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_paper = {}
            
            for paper in papers:
                if paper.get('pdf_url'):
                    future = executor.submit(
                        self._download_paper, 
                        paper, 
                        download_dir
                    )
                    future_to_paper[future] = paper
            
            for future in tqdm(
                as_completed(future_to_paper),
                total=len(future_to_paper),
                desc="下载PDF文件"
            ):
                paper = future_to_paper[future]
                try:
                    result = future.result()
                    if result:
                        downloaded_papers.append(result)
                except Exception as e:
                    self.logger.error(f"下载论文失败 {paper.get('arxiv_id')}: {e}")
                    downloaded_papers.append(paper)
        
        return downloaded_papers
    
    def _download_paper(self, paper, download_dir):
        """下载单个论文"""
        arxiv_id = paper.get('arxiv_id')
        pdf_url = paper.get('pdf_url')
        
        if not arxiv_id or not pdf_url:
            self.logger.warning(f"论文缺少必要信息: {arxiv_id}")
            return paper
        
        # 构建文件名
        filename = f"{arxiv_id}.pdf"
        filepath = os.path.join(download_dir, filename)
        
        # 检查文件是否已存在
        if os.path.exists(filepath):
            self.logger.info(f"文件已存在，跳过下载: {filename}")
            paper['pdf_path'] = filepath
            return paper
        
        try:
            self.logger.info(f"开始下载: {arxiv_id}")
            
            # 发送请求
            response = requests.get(
                pdf_url, 
                timeout=self.config.get('timeout', 60),
                stream=True
            )
            response.raise_for_status()
            
            # 获取文件大小
            total_size = int(response.headers.get('content-length', 0))
            
            # 下载文件
            with open(filepath, 'wb') as f:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
            
            # 验证文件大小
            if os.path.getsize(filepath) == 0:
                os.remove(filepath)
                self.logger.error(f"下载的文件为空: {filename}")
                return paper
            
            self.logger.info(f"下载完成: {filename}")
            paper['pdf_path'] = filepath
            
        except Exception as e:
            self.logger.error(f"下载失败 {arxiv_id}: {e}")
            # 清理空文件
            if os.path.exists(filepath) and os.path.getsize(filepath) == 0:
                os.remove(filepath)
        
        return paper
