#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
状态管理模块
"""

import os
import json
import logging
from datetime import datetime

class StateManager:
    """状态管理器"""
    
    def __init__(self, state_file=None):
        """初始化状态管理器
        
        Args:
            state_file: 状态文件路径
        """
        self.logger = logging.getLogger(__name__)
        
        if state_file:
            self.state_file = state_file
        else:
            # 默认状态文件路径
            self.state_file = os.path.join(
                os.path.dirname(__file__),
                '..',
                'data',
                'cache',
                'state.json'
            )
        
        # 确保目录存在
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        
        # 加载状态
        self.state = self._load_state()
    
    def _load_state(self):
        """加载状态"""
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.error(f"加载状态失败: {e}")
        
        # 返回默认状态
        return {
            'last_run': None,
            'completed_steps': [],
            'current_step': None,
            'papers': [],
            'statistics': {}
        }
    
    def save(self):
        """保存状态"""
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(self.state, f, ensure_ascii=False, indent=2)
            self.logger.info(f"状态已保存到: {self.state_file}")
        except Exception as e:
            self.logger.error(f"保存状态失败: {e}")
    
    def get(self, key, default=None):
        """获取状态值
        
        Args:
            key: 键
            default: 默认值
        
        Returns:
            状态值
        """
        return self.state.get(key, default)
    
    def set(self, key, value):
        """设置状态值
        
        Args:
            key: 键
            value: 值
        """
        self.state[key] = value
        self.save()
    
    def mark_step_completed(self, step):
        """标记步骤完成
        
        Args:
            step: 步骤名称
        """
        if step not in self.state.get('completed_steps', []):
            self.state.setdefault('completed_steps', []).append(step)
            self.state['current_step'] = None
            self.state['last_run'] = datetime.now().isoformat()
            self.save()
    
    def set_current_step(self, step):
        """设置当前步骤
        
        Args:
            step: 步骤名称
        """
        self.state['current_step'] = step
        self.save()
    
    def reset(self):
        """重置状态"""
        self.state = {
            'last_run': None,
            'completed_steps': [],
            'current_step': None,
            'papers': [],
            'statistics': {}
        }
        self.save()
    
    def reset_step(self, step):
        """重置指定步骤
        
        Args:
            step: 步骤名称
        """
        if step in self.state.get('completed_steps', []):
            self.state['completed_steps'].remove(step)
            self.save()
    
    def is_step_completed(self, step):
        """检查步骤是否完成
        
        Args:
            step: 步骤名称
        
        Returns:
            是否完成
        """
        return step in self.state.get('completed_steps', [])
    
    def get_statistics(self):
        """获取统计信息
        
        Returns:
            统计信息
        """
        return self.state.get('statistics', {})
    
    def update_statistics(self, stats):
        """更新统计信息
        
        Args:
            stats: 统计信息字典
        """
        self.state.setdefault('statistics', {}).update(stats)
        self.save()


def get_state_manager():
    """获取状态管理器实例
    
    Returns:
        状态管理器实例
    """
    return StateManager()
