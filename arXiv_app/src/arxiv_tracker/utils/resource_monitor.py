#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
资源监控模块
"""

import psutil
import logging
import time
from typing import Dict, Any

class ResourceMonitor:
    """资源监控器"""
    
    def __init__(self):
        """初始化资源监控器"""
        self.logger = logging.getLogger(__name__)
        self.start_time = time.time()
    
    def get_system_stats(self) -> Dict[str, Any]:
        """获取系统统计信息
        
        Returns:
            系统统计信息
        """
        try:
            # CPU信息
            cpu_percent = psutil.cpu_percent(interval=0.1)
            cpu_count = psutil.cpu_count(logical=True)
            
            # 内存信息
            memory = psutil.virtual_memory()
            memory_used = memory.used / (1024 * 1024 * 1024)  # GB
            memory_total = memory.total / (1024 * 1024 * 1024)  # GB
            memory_percent = memory.percent
            
            # 磁盘信息
            disk = psutil.disk_usage('/')
            disk_used = disk.used / (1024 * 1024 * 1024)  # GB
            disk_total = disk.total / (1024 * 1024 * 1024)  # GB
            disk_percent = disk.percent
            
            # 网络信息
            net_io = psutil.net_io_counters()
            bytes_sent = net_io.bytes_sent / (1024 * 1024)  # MB
            bytes_recv = net_io.bytes_recv / (1024 * 1024)  # MB
            
            # 运行时间
            uptime = time.time() - self.start_time
            
            return {
                'cpu': {
                    'percent': cpu_percent,
                    'count': cpu_count
                },
                'memory': {
                    'used_gb': round(memory_used, 2),
                    'total_gb': round(memory_total, 2),
                    'percent': memory_percent
                },
                'disk': {
                    'used_gb': round(disk_used, 2),
                    'total_gb': round(disk_total, 2),
                    'percent': disk_percent
                },
                'network': {
                    'sent_mb': round(bytes_sent, 2),
                    'recv_mb': round(bytes_recv, 2)
                },
                'uptime': round(uptime, 2)
            }
            
        except Exception as e:
            self.logger.error(f"获取系统统计信息失败: {e}")
            return {}
    
    def log_stats(self, prefix: str = ""):
        """记录系统统计信息
        
        Args:
            prefix: 日志前缀
        """
        stats = self.get_system_stats()
        if stats:
            message = f"{prefix}系统资源使用情况: "
            message += f"CPU: {stats['cpu']['percent']}% "
            message += f"内存: {stats['memory']['used_gb']}/{stats['memory']['total_gb']}GB ({stats['memory']['percent']}%) "
            message += f"磁盘: {stats['disk']['used_gb']}/{stats['disk']['total_gb']}GB ({stats['disk']['percent']}%) "
            message += f"运行时间: {stats['uptime']}s"
            self.logger.info(message)
    
    def check_resources(self, cpu_threshold: float = 80.0, memory_threshold: float = 80.0) -> bool:
        """检查资源使用情况
        
        Args:
            cpu_threshold: CPU使用率阈值
            memory_threshold: 内存使用率阈值
        
        Returns:
            是否正常
        """
        stats = self.get_system_stats()
        if not stats:
            return True
        
        cpu_ok = stats['cpu']['percent'] < cpu_threshold
        memory_ok = stats['memory']['percent'] < memory_threshold
        
        if not cpu_ok:
            self.logger.warning(f"CPU使用率过高: {stats['cpu']['percent']}%")
        
        if not memory_ok:
            self.logger.warning(f"内存使用率过高: {stats['memory']['percent']}%")
        
        return cpu_ok and memory_ok
    
    def get_process_stats(self) -> Dict[str, Any]:
        """获取当前进程统计信息
        
        Returns:
            进程统计信息
        """
        try:
            process = psutil.Process()
            
            # 内存信息
            memory_info = process.memory_info()
            memory_rss = memory_info.rss / (1024 * 1024)  # MB
            memory_vms = memory_info.vms / (1024 * 1024)  # MB
            
            # CPU信息
            cpu_percent = process.cpu_percent(interval=0.1)
            
            # 其他信息
            create_time = process.create_time()
            threads = process.num_threads()
            
            return {
                'memory': {
                    'rss_mb': round(memory_rss, 2),
                    'vms_mb': round(memory_vms, 2)
                },
                'cpu_percent': cpu_percent,
                'threads': threads,
                'uptime': round(time.time() - create_time, 2)
            }
            
        except Exception as e:
            self.logger.error(f"获取进程统计信息失败: {e}")
            return {}


def get_resource_monitor():
    """获取资源监控器实例
    
    Returns:
        资源监控器实例
    """
    return ResourceMonitor()
