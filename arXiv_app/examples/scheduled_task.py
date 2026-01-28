#!/usr/bin/env python3
"""
定时任务示例

这个脚本展示了如何将arXiv论文跟踪系统设置为定时任务运行，包括：
1. 使用schedule库设置定时任务
2. 配置任务参数
3. 处理任务执行结果
4. 错误处理和日志记录

用法：
    python examples/scheduled_task.py

注意：
    1. 此脚本需要安装schedule库: pip install schedule
    2. 运行此脚本会持续运行，直到手动停止
"""

import os
import sys
import time
import schedule
import threading

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from arxiv_tracker import ArxivTracker
from arxiv_tracker.utils.logger import setup_logger

# 设置日志
logger = setup_logger('scheduled_task')


class ScheduledArxivTracker:
    """定时运行arXiv论文跟踪系统"""
    
    def __init__(self):
        """初始化"""
        self.tracker = ArxivTracker()
        self.running = False
        self.lock = threading.Lock()
    
    def run_task(self):
        """运行跟踪任务"""
        # 避免并发执行
        with self.lock:
            if not self.running:
                self.running = True
                try:
                    logger.info("定时任务开始执行")
                    
                    # 运行跟踪系统
                    results = self.tracker.run(
                        count=10,  # 处理10篇论文
                        categories=['cs.AI', 'cs.LG', 'cs.CV'],  # 处理AI、机器学习和计算机视觉
                        use_pdf=True,  # 从PDF提取信息
                        date=None  # 使用当前日期
                    )
                    
                    logger.info(f"定时任务执行完成，共处理了 {len(results)} 篇论文")
                    
                    # 记录高评分论文
                    high_score_papers = [p for p in results if p.get('score', 0) >= 8.0]
                    if high_score_papers:
                        logger.info(f"\n发现 {len(high_score_papers)} 篇高评分论文:")
                        for i, paper in enumerate(high_score_papers[:3], 1):
                            logger.info(f"\n=== 高评分论文 {i} ===")
                            logger.info(f"标题: {paper.get('title', 'N/A')}")
                            logger.info(f"评分: {paper.get('score', 'N/A')}")
                            logger.info(f"论文ID: {paper.get('arxiv_id', 'N/A')}")
                    
                except Exception as e:
                    logger.error(f"定时任务执行出错: {e}")
                    import traceback
                    traceback.print_exc()
                finally:
                    self.running = False
            else:
                logger.warning("定时任务正在运行，跳过本次执行")
    
    def start_schedule(self):
        """开始定时任务"""
        logger.info("启动定时任务")
        
        # 设置定时任务
        # 每天凌晨2点运行
        schedule.every().day.at("02:00").do(self.run_task)
        
        # 每小时运行一次（用于测试）
        schedule.every().hour.do(self.run_task)
        
        logger.info("定时任务已设置")
        logger.info("- 每天凌晨2点运行完整任务")
        logger.info("- 每小时运行一次（测试模式）")
        logger.info("按 Ctrl+C 停止定时任务")
        
        # 立即运行一次
        logger.info("\n立即运行一次任务...")
        self.run_task()
        
        # 持续运行
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次
            except KeyboardInterrupt:
                logger.info("定时任务已停止")
                break
            except Exception as e:
                logger.error(f"调度器出错: {e}")
                time.sleep(60)


def run_scheduled_task():
    """运行定时任务示例"""
    logger.info("开始定时任务示例")
    
    try:
        # 检查schedule库是否安装
        try:
            import schedule
        except ImportError:
            logger.warning("schedule库未安装，正在安装...")
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "schedule"])
            import schedule
        
        # 创建定时跟踪器
        scheduled_tracker = ScheduledArxivTracker()
        
        # 启动定时任务
        scheduled_tracker.start_schedule()
        
    except Exception as e:
        logger.error(f"运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_scheduled_task()
