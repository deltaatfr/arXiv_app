# arxiv_tracker package

from .crawler import ArxivCrawler
from .downloader import ArxivDownloader
from .extractor import ArxivExtractor
from .analyzer import ArxivAnalyzer
from .reporter import ArxivReporter
from .cli import main

__version__ = "1.0.0"
__all__ = [
    "ArxivCrawler",
    "ArxivDownloader",
    "ArxivExtractor",
    "ArxivAnalyzer",
    "ArxivReporter",
    "main"
]

class ArxivTracker:
    """arXiv论文跟踪系统主类"""
    
    def __init__(self, config_path=None):
        """初始化跟踪器"""
        from .utils.config import load_config
        from .utils.logger import setup_logger
        
        # 加载配置
        self.config = load_config(config_path)
        
        # 设置日志
        setup_logger()
        
        # 初始化各个组件
        self.crawler = ArxivCrawler(self.config)
        self.downloader = ArxivDownloader(self.config)
        self.extractor = ArxivExtractor(self.config)
        self.analyzer = ArxivAnalyzer(self.config)
        self.reporter = ArxivReporter(self.config)
    
    def run(self, categories=None, count=None, use_pdf=False, date=None):
        """运行完整的跟踪流程"""
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            # 使用参数覆盖配置
            if categories:
                self.config['categories'] = categories
            if count:
                self.config['default_paper_count'] = count
            
            # 1. 爬取论文信息
            logger.info("开始爬取论文信息")
            papers = self.crawler.crawl(date=date)
            logger.info(f"成功爬取 {len(papers)} 篇论文")
            
            # 2. 下载PDF文件
            logger.info("开始下载PDF文件")
            papers = self.downloader.download(papers, date=date)
            logger.info("PDF文件下载完成")
            
            # 3. 提取信息
            logger.info("开始提取论文信息")
            if use_pdf:
                papers = self.extractor.extract_from_pdfs(papers, date=date)
            else:
                papers = self.extractor.extract_from_web(papers)
            logger.info("论文信息提取完成")
            
            # 4. 分析论文
            logger.info("开始分析论文")
            papers = self.analyzer.analyze(papers)
            logger.info("论文分析完成")
            
            # 5. 生成报告
            logger.info("开始生成报告")
            self.reporter.generate(papers, date=date)
            logger.info("报告生成完成")
            
            return papers
            
        except Exception as e:
            logger.error(f"运行失败: {e}")
            import traceback
            logger.error(traceback.format_exc())
            raise
