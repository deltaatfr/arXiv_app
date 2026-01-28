#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境设置脚本
自动创建和配置Python虚拟环境
"""

import os
import sys
import subprocess
import logging

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_venv():
    """创建虚拟环境"""
    venv_dir = os.path.join(os.path.dirname(__file__), '..', 'venv')
    
    if os.path.exists(venv_dir):
        logger.info(f"虚拟环境已存在: {venv_dir}")
        return True
    
    logger.info(f"开始创建虚拟环境: {venv_dir}")
    
    try:
        # 创建虚拟环境
        subprocess.run(
            [sys.executable, '-m', 'venv', venv_dir],
            check=True,
            capture_output=True,
            text=True
        )
        logger.info("虚拟环境创建成功")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"创建虚拟环境失败: {e.stderr}")
        return False

def install_dependencies():
    """安装依赖包"""
    venv_dir = os.path.join(os.path.dirname(__file__), '..', 'venv')
    requirements_file = os.path.join(os.path.dirname(__file__), '..', 'requirements.txt')
    
    # 确定pip路径
    if sys.platform.startswith('win'):
        pip_exe = os.path.join(venv_dir, 'Scripts', 'pip.exe')
    else:
        pip_exe = os.path.join(venv_dir, 'bin', 'pip')
    
    if not os.path.exists(pip_exe):
        logger.error(f"pip可执行文件不存在: {pip_exe}")
        return False
    
    logger.info("开始安装依赖包")
    
    try:
        # 升级pip
        subprocess.run(
            [pip_exe, 'install', '--upgrade', 'pip'],
            check=True,
            capture_output=True,
            text=True
        )
        logger.info("pip升级成功")
        
        # 安装依赖
        subprocess.run(
            [pip_exe, 'install', '-r', requirements_file],
            check=True,
            capture_output=True,
            text=True
        )
        logger.info("依赖包安装成功")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"安装依赖失败: {e.stderr}")
        return False

def main():
    """主函数"""
    logger.info("开始设置Python环境")
    
    # 创建虚拟环境
    if not create_venv():
        logger.error("环境设置失败")
        return False
    
    # 安装依赖
    if not install_dependencies():
        logger.error("环境设置失败")
        return False
    
    logger.info("环境设置完成！")
    logger.info("使用以下命令激活虚拟环境:")
    
    venv_dir = os.path.join(os.path.dirname(__file__), '..', 'venv')
    if sys.platform.startswith('win'):
        logger.info(f"  {os.path.join(venv_dir, 'Scripts', 'activate')}")
    else:
        logger.info(f"  source {os.path.join(venv_dir, 'bin', 'activate')}")
    
    logger.info("然后运行:")
    logger.info("  python arxivtracker.py --help")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
