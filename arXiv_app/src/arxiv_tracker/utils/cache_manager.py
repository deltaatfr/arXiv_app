#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
缓存管理模块
"""

import os
import json
import time
import logging
from typing import Dict, Any, Optional

class CacheManager:
    """缓存管理器"""
    
    def __init__(self, cache_file=None, ttl=86400):
        """初始化缓存管理器
        
        Args:
            cache_file: 缓存文件路径
            ttl: 缓存过期时间（秒）
        """
        self.logger = logging.getLogger(__name__)
        self.ttl = ttl
        
        if cache_file:
            self.cache_file = cache_file
        else:
            # 默认缓存文件路径
            self.cache_file = os.path.join(
                os.path.dirname(__file__),
                '..',
                'data',
                'cache',
                'cache.json'
            )
        
        # 确保目录存在
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
        
        # 加载缓存
        self.cache = self._load_cache()
    
    def _load_cache(self):
        """加载缓存"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 检查缓存是否过期
                    if 'timestamp' in data:
                        if time.time() - data['timestamp'] < self.ttl:
                            return data.get('data', {})
                        else:
                            self.logger.info("缓存已过期，将重新加载")
        except Exception as e:
            self.logger.error(f"加载缓存失败: {e}")
        
        # 返回空缓存
        return {}
    
    def save(self):
        """保存缓存"""
        try:
            data = {
                'timestamp': time.time(),
                'data': self.cache
            }
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.logger.info(f"缓存已保存到: {self.cache_file}")
        except Exception as e:
            self.logger.error(f"保存缓存失败: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取缓存值
        
        Args:
            key: 键
            default: 默认值
        
        Returns:
            缓存值
        """
        return self.cache.get(key, default)
    
    def set(self, key: str, value: Any):
        """设置缓存值
        
        Args:
            key: 键
            value: 值
        """
        self.cache[key] = value
        self.save()
    
    def delete(self, key: str):
        """删除缓存值
        
        Args:
            key: 键
        """
        if key in self.cache:
            del self.cache[key]
            self.save()
    
    def clear(self):
        """清空缓存"""
        self.cache = {}
        self.save()
    
    def exists(self, key: str) -> bool:
        """检查键是否存在
        
        Args:
            key: 键
        
        Returns:
            是否存在
        """
        return key in self.cache
    
    def get_cache_size(self) -> int:
        """获取缓存大小
        
        Returns:
            缓存项数量
        """
        return len(self.cache)
    
    def get_cache_info(self) -> Dict[str, Any]:
        """获取缓存信息
        
        Returns:
            缓存信息
        """
        return {
            'size': self.get_cache_size(),
            'file': self.cache_file,
            'ttl': self.ttl
        }


def get_cache_manager():
    """获取缓存管理器实例
    
    Returns:
        缓存管理器实例
    """
    return CacheManager()
