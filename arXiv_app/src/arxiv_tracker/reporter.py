#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
arXiv论文报告模块
"""

import os
import json
import markdown
from datetime import datetime
from typing import List, Dict
import logging

class ArxivReporter:
    """arXiv论文报告生成器"""
    
    def __init__(self, config):
        """初始化报告生成器"""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # 确保报告目录存在
        self.report_dir = os.path.join(
            os.path.dirname(__file__),
            '..',
            self.config.get('report_storage', 'data/reports')
        )
        os.makedirs(self.report_dir, exist_ok=True)
    
    def generate(self, papers, date=None):
        """生成报告"""
        if not papers:
            self.logger.warning("没有论文数据，跳过报告生成")
            return
        
        # 创建日期子目录
        if date:
            report_dir = os.path.join(self.report_dir, date)
        else:
            report_date = datetime.now().strftime('%Y%m%d')
            report_dir = os.path.join(self.report_dir, report_date)
        
        os.makedirs(report_dir, exist_ok=True)
        
        self.logger.info(f"报告将生到: {report_dir}")
        
        # 生成不同格式的报告
        self._generate_markdown_report(papers, report_dir, date)
        self._generate_json_report(papers, report_dir, date)
        self._generate_summary_report(papers, report_dir, date)
    
    def _generate_markdown_report(self, papers, report_dir, date):
        """生成Markdown格式报告"""
        report_date = date or datetime.now().strftime('%Y%m%d')
        filename = f"arxiv_report_{report_date}.md"
        filepath = os.path.join(report_dir, filename)
        
        # 构建报告内容
        content = f"""# arXiv论文分析报告

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 报告概览

- 分析论文数量: {len(papers)}
- 分析日期: {report_date}

## 论文列表

"""
        
        # 添加论文详情
        for i, paper in enumerate(papers, 1):
            content += f"""
### {i}. {paper.get('title', 'Unknown Title')}

**作者**: {', '.join(paper.get('authors', [])) if paper.get('authors') else 'Unknown'}
**arXiv ID**: {paper.get('arxiv_id', 'Unknown')}
**类别**: {paper.get('category', 'Unknown')}
**评分**: {paper.get('score', 'N/A')}

**摘要**:
{paper.get('abstract', 'No abstract available')}

"""
            
            # 添加分析结果
            if paper.get('overall_evaluation'):
                content += f"""
**分析结果**:
- **研究问题**: {paper.get('research_question', 'N/A')}
- **方法创新**: {paper.get('method_innovation', 'N/A')}
- **实验结果**: {paper.get('experimental_results', 'N/A')}
- **应用价值**: {paper.get('application_value', 'N/A')}
- **局限性**: {paper.get('limitations', 'N/A')}
- **总体评价**: {paper.get('overall_evaluation', 'N/A')}

"""
        
        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.logger.info(f"Markdown报告生成完成: {filename}")
    
    def _generate_json_report(self, papers, report_dir, date):
        """生成JSON格式报告"""
        report_date = date or datetime.now().strftime('%Y%m%d')
        filename = f"arxiv_report_{report_date}.json"
        filepath = os.path.join(report_dir, filename)
        
        # 构建报告数据
        report_data = {
            "generated_at": datetime.now().isoformat(),
            "report_date": report_date,
            "total_papers": len(papers),
            "papers": papers
        }
        
        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"JSON报告生成完成: {filename}")
    
    def _generate_summary_report(self, papers, report_dir, date):
        """生成摘要报告"""
        report_date = date or datetime.now().strftime('%Y%m%d')
        filename = f"arxiv_summary_{report_date}.md"
        filepath = os.path.join(report_dir, filename)
        
        # 计算统计信息
        total_papers = len(papers)
        scored_papers = [p for p in papers if 'score' in p and p['score']]
        avg_score = sum(p['score'] for p in scored_papers) / len(scored_papers) if scored_papers else 0
        
        # 按评分排序
        top_papers = sorted(papers, key=lambda x: x.get('score', 0), reverse=True)[:5]
        
        # 构建报告内容
        content = f"""
# arXiv论文分析摘要

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 统计概览

- 分析论文总数: {total_papers}
- 有评分论文数: {len(scored_papers)}
- 平均评分: {avg_score:.2f}
- 分析日期: {report_date}

## 评分最高的5篇论文

"""
        
        # 添加top论文
        for i, paper in enumerate(top_papers, 1):
            content += f"""
### {i}. {paper.get('title', 'Unknown Title')}

**作者**: {', '.join(paper.get('authors', [])) if paper.get('authors') else 'Unknown'}
**评分**: {paper.get('score', 'N/A')}
**摘要**:
{paper.get('abstract', 'No abstract available')[:200]}...

"""
        
        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.logger.info(f"摘要报告生成完成: {filename}")
