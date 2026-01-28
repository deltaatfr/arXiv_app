#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
arXiv论文分析模块
"""

import os
import json
import logging
from typing import List, Dict
from dashscope import Generation

class ArxivAnalyzer:
    """arXiv论文分析器"""
    
    def __init__(self, config):
        """初始化分析器"""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # 加载API配置
        api_config_path = os.path.join(
            os.path.dirname(__file__),
            '..',
            '..',
            'config',
            'api_config.json'
        )
        
        self.api_key = None
        if os.path.exists(api_config_path):
            with open(api_config_path, 'r', encoding='utf-8') as f:
                api_config = json.load(f)
                self.api_key = api_config.get('dashscope_api_key')
        
        if not self.api_key:
            self.logger.warning("未配置API密钥，分析功能将不可用")
    
    def analyze(self, papers):
        """分析论文列表"""
        if not papers:
            return papers
        
        if not self.api_key:
            self.logger.warning("API密钥未配置，跳过分析")
            return papers
        
        analyzed_papers = []
        
        for paper in papers:
            try:
                self.logger.info(f"分析论文: {paper.get('title', 'Unknown')}")
                analysis = self._analyze_paper(paper)
                if analysis:
                    paper.update(analysis)
                    analyzed_papers.append(paper)
                else:
                    analyzed_papers.append(paper)
            except Exception as e:
                self.logger.error(f"分析论文失败: {e}")
                analyzed_papers.append(paper)
        
        return analyzed_papers
    
    def _analyze_paper(self, paper):
        """分析单个论文"""
        title = paper.get('title', '')
        abstract = paper.get('abstract', '')
        authors = paper.get('authors', [])
        
        if not title or not abstract:
            self.logger.warning("论文缺少标题或摘要，跳过分析")
            return {}
        
        # 构建分析提示
        prompt = self._build_analysis_prompt(title, abstract, authors)
        
        try:
            # 调用LLM API
            response = Generation.call(
                model="qwen-plus",
                prompt=prompt,
                api_key=self.api_key,
                temperature=0.3,
                top_p=0.8,
                max_tokens=2000
            )
            
            if response.status_code == 200:
                result = response.output.text
                return self._parse_analysis_result(result)
            else:
                self.logger.error(f"API调用失败: {response.message}")
                return {}
                
        except Exception as e:
            self.logger.error(f"分析论文时API调用失败: {e}")
            return {}
    
    def _build_analysis_prompt(self, title, abstract, authors):
        """构建分析提示"""
        return f"""请分析以下arXiv论文并提供详细评估：

标题：{title}

作者：{', '.join(authors) if authors else 'Unknown'}

摘要：{abstract}

请从以下几个方面进行分析：
1. 研究问题：论文解决了什么问题？为什么这个问题重要？
2. 方法创新：论文提出了什么新方法或技术？与现有方法相比有什么优势？
3. 实验结果：论文报告了哪些关键实验结果？结果是否令人信服？
4. 应用价值：论文的研究成果有什么实际应用价值？
5. 局限性：论文存在哪些局限性或未来工作方向？
6. 总体评价：对论文的整体质量和贡献进行评价。
7. 评分：请对论文进行1-10分的评分，10分为最高。

请按照以下JSON格式返回分析结果：
{
  "research_question": "研究问题分析",
  "method_innovation": "方法创新分析",
  "experimental_results": "实验结果分析",
  "application_value": "应用价值分析",
  "limitations": "局限性分析",
  "overall_evaluation": "总体评价",
  "score": 8.5
}

请确保返回的是有效的JSON格式，不要包含任何额外的文本。"""
    
    def _parse_analysis_result(self, result):
        """解析分析结果"""
        try:
            # 提取JSON部分
            import re
            json_match = re.search(r'\{[\s\S]*\}', result)
            if json_match:
                json_str = json_match.group(0)
                analysis = json.loads(json_str)
                return analysis
            else:
                # 尝试直接解析整个结果
                analysis = json.loads(result)
                return analysis
        except Exception as e:
            self.logger.error(f"解析分析结果失败: {e}")
            # 返回默认值
            return {
                "research_question": "",
                "method_innovation": "",
                "experimental_results": "",
                "application_value": "",
                "limitations": "",
                "overall_evaluation": "",
                "score": 5.0
            }
