#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件工具模块
"""

import os
import shutil
import logging
import json
from typing import List, Dict, Any, Optional

class FileUtils:
    """文件工具类"""
    
    def __init__(self):
        """初始化文件工具"""
        self.logger = logging.getLogger(__name__)
    
    def ensure_dir(self, directory: str):
        """确保目录存在
        
        Args:
            directory: 目录路径
        """
        try:
            os.makedirs(directory, exist_ok=True)
            return True
        except Exception as e:
            self.logger.error(f"创建目录失败 {directory}: {e}")
            return False
    
    def write_json(self, data: Any, filepath: str, indent: int = 2):
        """写入JSON文件
        
        Args:
            data: 数据
            filepath: 文件路径
            indent: 缩进
        
        Returns:
            是否成功
        """
        try:
            # 确保目录存在
            self.ensure_dir(os.path.dirname(filepath))
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=indent)
            self.logger.info(f"JSON文件已写入: {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"写入JSON文件失败 {filepath}: {e}")
            return False
    
    def read_json(self, filepath: str) -> Optional[Dict[str, Any]]:
        """读取JSON文件
        
        Args:
            filepath: 文件路径
        
        Returns:
            数据或None
        """
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                self.logger.warning(f"JSON文件不存在: {filepath}")
                return None
        except Exception as e:
            self.logger.error(f"读取JSON文件失败 {filepath}: {e}")
            return None
    
    def write_text(self, content: str, filepath: str):
        """写入文本文件
        
        Args:
            content: 内容
            filepath: 文件路径
        
        Returns:
            是否成功
        """
        try:
            # 确保目录存在
            self.ensure_dir(os.path.dirname(filepath))
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            self.logger.info(f"文本文件已写入: {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"写入文本文件失败 {filepath}: {e}")
            return False
    
    def read_text(self, filepath: str) -> Optional[str]:
        """读取文本文件
        
        Args:
            filepath: 文件路径
        
        Returns:
            内容或None
        """
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                self.logger.warning(f"文本文件不存在: {filepath}")
                return None
        except Exception as e:
            self.logger.error(f"读取文本文件失败 {filepath}: {e}")
            return None
    
    def copy_file(self, src: str, dst: str):
        """复制文件
        
        Args:
            src: 源文件
            dst: 目标文件
        
        Returns:
            是否成功
        """
        try:
            # 确保目录存在
            self.ensure_dir(os.path.dirname(dst))
            
            shutil.copy2(src, dst)
            self.logger.info(f"文件已复制: {src} -> {dst}")
            return True
        except Exception as e:
            self.logger.error(f"复制文件失败 {src} -> {dst}: {e}")
            return False
    
    def move_file(self, src: str, dst: str):
        """移动文件
        
        Args:
            src: 源文件
            dst: 目标文件
        
        Returns:
            是否成功
        """
        try:
            # 确保目录存在
            self.ensure_dir(os.path.dirname(dst))
            
            shutil.move(src, dst)
            self.logger.info(f"文件已移动: {src} -> {dst}")
            return True
        except Exception as e:
            self.logger.error(f"移动文件失败 {src} -> {dst}: {e}")
            return False
    
    def delete_file(self, filepath: str):
        """删除文件
        
        Args:
            filepath: 文件路径
        
        Returns:
            是否成功
        """
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                self.logger.info(f"文件已删除: {filepath}")
                return True
            else:
                self.logger.warning(f"文件不存在: {filepath}")
                return False
        except Exception as e:
            self.logger.error(f"删除文件失败 {filepath}: {e}")
            return False
    
    def list_files(self, directory: str, pattern: str = "*") -> List[str]:
        """列出目录中的文件
        
        Args:
            directory: 目录
            pattern: 文件模式
        
        Returns:
            文件列表
        """
        try:
            import glob
            search_path = os.path.join(directory, pattern)
            return glob.glob(search_path)
        except Exception as e:
            self.logger.error(f"列出文件失败 {directory}: {e}")
            return []
    
    def get_file_size(self, filepath: str) -> int:
        """获取文件大小
        
        Args:
            filepath: 文件路径
        
        Returns:
            文件大小（字节）
        """
        try:
            if os.path.exists(filepath):
                return os.path.getsize(filepath)
            else:
                return 0
        except Exception as e:
            self.logger.error(f"获取文件大小失败 {filepath}: {e}")
            return 0
    
    def get_relative_path(self, path: str, base: str) -> str:
        """获取相对路径
        
        Args:
            path: 路径
            base: 基础路径
        
        Returns:
            相对路径
        """
        try:
            return os.path.relpath(path, base)
        except Exception as e:
            self.logger.error(f"获取相对路径失败: {e}")
            return path


def get_file_utils():
    """获取文件工具实例
    
    Returns:
        文件工具实例
    """
    return FileUtils()
