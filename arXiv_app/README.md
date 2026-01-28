# arXiv论文跟踪系统

一个功能完整、可移植的arXiv论文跟踪和分析系统，支持自动爬取、下载、信息提取和智能分析。

## 目录结构

```
arXiv_app/
├── README.md                           # 项目总说明
├── LICENSE                            # 开源许可证
├── requirements.txt                   # 依赖包清单
├── pyproject.toml                     # 现代Python项目配置
├── setup.py                           # 传统打包配置
├── arxivtracker.py                    # 主程序入口
├── config/                            # 配置文件目录
│   ├── __init__.py
│   ├── system_config.json             # 系统配置
│   ├── api_config.json                # API配置模板
│   ├── categories.json                # 论文类别
│   └── logging_config.json            # 日志配置
├── src/                               # 源代码（符合Python包标准）
│   ├── __init__.py
│   ├── arxiv_tracker/                 # 主包
│   │   ├── __init__.py
│   │   ├── crawler.py                # 爬取模块
│   │   ├── downloader.py             # 下载模块
│   │   ├── extractor.py              # 信息提取模块
│   │   ├── analyzer.py               # 分析模块
│   │   ├── reporter.py               # 报告模块
│   │   ├── utils/                    # 工具模块
│   │   │   ├── __init__.py
│   │   │   ├── state_manager.py
│   │   │   ├── resource_monitor.py
│   │   │   ├── cache_manager.py
│   │   │   ├── file_utils.py
│   │   │   └── logger.py
│   │   └── data/                     # 数据存储（相对路径）
│   │       ├── papers/               # PDF文件
│   │       ├── reports/              # 报告文件
│   │       ├── cache/                # 缓存文件
│   │       └── logs/                 # 日志文件
├── scripts/                           # 辅助脚本
│   ├── __init__.py
│   ├── setup_venv.py                 # 环境设置（原第0步）
│   ├── reset_states.py               # 状态重置
│   ├── check_abstract.py             # 摘要检查
│   └── extract_from_pdf.py           # PDF提取
├── docs/                              # 项目文档
│   ├── requirements.md               # 需求文档
│   ├── technical_design.md           # 技术设计
│   ├── api_reference.md              # API参考
│   ├── installation.md               # 安装部署
│   ├── user_manual.md                # 用户手册
│   ├── maintenance.md                # 维护文档
│   └── images/                       # 文档图片
├── tests/                             # 测试文件
│   ├── __init__.py
│   ├── conftest.py                   # pytest配置
│   ├── test_crawler.py
│   ├── test_downloader.py
│   ├── test_extractor.py
│   ├── test_analyzer.py
│   └── integration/                  # 集成测试
├── examples/                          # 使用示例
│   ├── basic_usage.py
│   ├── custom_config.py
│   └── scheduled_task.py             # 定时任务示例
├── docker/                            # Docker配置
│   ├── Dockerfile
│   └── docker-compose.yml
└── notebooks/                         # Jupyter Notebook示例
    └── demo_usage.ipynb
```

## 功能特性

- **自动爬取**：从arXiv网站自动爬取最新论文信息
- **PDF下载**：自动下载论文PDF文件并按日期组织
- **信息提取**：从PDF文件中提取标题、作者、摘要等信息
- **智能分析**：使用LLM对论文进行智能分析和评分
- **报告生成**：生成结构化的分析报告
- **状态管理**：支持断点续传和状态恢复
- **资源监控**：监控系统资源使用情况
- **错误处理**：完善的错误处理和日志记录

## 快速开始

### 1. 环境准备

确保你的系统已安装Python 3.7或更高版本。

### 2. 安装依赖

```bash
# 方法1：使用pip直接安装
pip install -r requirements.txt

# 方法2：使用setup.py安装（推荐）
pip install -e .
```

### 3. 配置API密钥

复制并编辑API配置文件：

```bash
cp config/api_config.json.example config/api_config.json
# 编辑api_config.json，添加你的API密钥
```

### 4. 运行系统

```bash
# 基本用法
python arxivtracker.py --count 10

# 从PDF文件提取信息
python arxivtracker.py --count 10 --use-pdf

# 指定日期
python arxivtracker.py --date 20260128 --count 15
```

## 使用示例

### 命令行使用

```bash
# 爬取并分析5篇论文
arxiv-tracker --count 5

# 只爬取不分析
arxiv-tracker --count 10 --no-analysis

# 指定类别
arxiv-tracker --categories cs.AI,cs.LG --count 8
```

### 作为Python库使用

```python
from arxiv_tracker import ArxivTracker

# 创建跟踪器实例
tracker = ArxivTracker()

# 运行跟踪任务
results = tracker.run(
    categories=['cs.AI', 'cs.LG'],
    count=10,
    use_pdf=True,
    date='20260128'
)

# 查看结果
for paper in results:
    print(f"Title: {paper['title']}")
    print(f"Authors: {', '.join(paper['authors'])}")
    print(f"Score: {paper.get('score', 'N/A')}")
    print()
```

## 配置说明

### 系统配置

`config/system_config.json` 包含系统级配置：

- `data_dir`：数据存储目录
- `categories`：默认论文类别
- `max_workers`：并发工作线程数
- `timeout`：网络请求超时时间

### API配置

`config/api_config.json` 包含API相关配置：

- `dashscope_api_key`：阿里云DashScope API密钥
- `api_endpoint`：API端点地址
- `max_retries`：API请求最大重试次数

## 依赖项

- Python 3.7+
- requests - 网络请求
- beautifulsoup4 - HTML解析
- PyPDF2 - PDF文件处理
- psutil - 系统资源监控
- markdown - Markdown处理

## 许可证

本项目采用MIT许可证。

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

- 项目地址：https://github.com/yourusername/arxiv-tracker
- 问题反馈：https://github.com/yourusername/arxiv-tracker/issues
