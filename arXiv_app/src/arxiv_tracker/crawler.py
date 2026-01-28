#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
arXiv论文爬取模块
"""

import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional

class ArxivCrawler:
    """arXiv论文爬取器"""
    
    def __init__(self, config):
        """初始化爬取器"""
        self.config = config
        self.base_url = "https://arxiv.org"
        self.logger = logging.getLogger(__name__)
    
    def crawl(self, date=None):
        """爬取指定日期的论文"""
        papers = []
        categories = self.config.get('categories', ['cs.AI', 'cs.LG'])
        max_workers = self.config.get('max_workers', 4)
        
        # 使用线程池并发爬取多个类别
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_category = {}
            
            for category in categories:
                future = executor.submit(
                    self._crawl_category, 
                    category, 
                    date
                )
                future_to_category[future] = category
            
            for future in as_completed(future_to_category):
                category = future_to_category[future]
                try:
                    category_papers = future.result()
                    papers.extend(category_papers)
                    self.logger.info(f"类别 {category} 爬取完成，获取 {len(category_papers)} 篇论文")
                except Exception as e:
                    self.logger.error(f"类别 {category} 爬取失败: {e}")
        
        # 限制数量
        max_count = self.config.get('default_paper_count', 10)
        if len(papers) > max_count:
            papers = papers[:max_count]
        
        return papers
    
    def _crawl_category(self, category, date=None):
        """爬取单个类别的论文"""
        papers = []
        
        # 构建URL
        if date:
            # 尝试爬取指定日期的论文
            year = date[:4]
            month = date[4:6]
            day = date[6:8]
            url = f"{self.base_url}/list/{category}/{year}-{month}"
        else:
            # 爬取最新论文
            url = f"{self.base_url}/list/{category}/new"
        
        try:
            response = requests.get(url, timeout=self.config.get('timeout', 30))
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找论文列表
            dl_elements = soup.find_all('dl')
            if not dl_elements:
                self.logger.warning(f"类别 {category} 未找到论文列表")
                return papers
            
            dl = dl_elements[0]
            dt_elements = dl.find_all('dt')
            dd_elements = dl.find_all('dd')
            
            for dt, dd in zip(dt_elements, dd_elements):
                paper = self._parse_paper(dt, dd, category)
                if paper:
                    papers.append(paper)
                    
                    # 达到数量限制
                    if len(papers) >= self.config.get('default_paper_count', 10):
                        break
        
        except Exception as e:
            self.logger.error(f"爬取类别 {category} 失败: {e}")
        
        return papers
    
    def _parse_paper(self, dt, dd, category):
        """解析单个论文信息"""
        try:
            # 提取论文ID
            id_link = dt.find('a', title='Abstract')
            if not id_link:
                return None
            
            id_text = id_link.text.strip()
            arxiv_id = id_text.split(':')[-1].strip()
            
            # 提取标题
            title_element = dd.find('div', class_='list-title')
            if title_element:
                title = title_element.text.replace('Title:', '').strip()
            else:
                title = ""
            
            # 提取作者
            authors_element = dd.find('div', class_='list-authors')
            authors = []
            if authors_element:
                author_links = authors_element.find_all('a')
                authors = [author.text.strip() for author in author_links]
            
            # 提取摘要
            abstract_element = dd.find('p', class_='mathjax')
            abstract = ""
            if abstract_element:
                abstract = abstract_element.text.strip()
            
            # 提取链接
            pdf_link = dt.find('a', title='Download PDF')
            pdf_url = ""
            if pdf_link:
                pdf_url = f"{self.base_url}{pdf_link.get('href')}"
            
            paper = {
                'arxiv_id': arxiv_id,
                'title': title,
                'authors': authors,
                'abstract': abstract,
                'category': category,
                'pdf_url': pdf_url,
                'url': f"{self.base_url}/abs/{arxiv_id}",
                'crawl_date': datetime.now().strftime('%Y%m%d')
            }
            
            return paper
            
        except Exception as e:
            self.logger.error(f"解析论文失败: {e}")
            return None
