# arXiv论文跟踪系统用户手册

## 1. 系统简介

arXiv论文跟踪系统是一个自动化工具，用于从arXiv网站爬取最新论文信息，下载PDF文件，提取关键信息，并使用LLM进行智能分析和评分。系统旨在帮助研究人员和学者快速了解领域最新进展，发现高价值论文。

## 2. 快速开始

### 2.1 首次运行

1. **安装系统**

   请参考《安装部署文档》完成系统安装。

2. **配置API密钥**

   编辑 `config/api_config.json` 文件，添加你的DashScope API密钥：

   ```json
   {
       "dashscope_api_key": "YOUR_API_KEY_HERE"
   }
   ```

3. **运行系统**

   ```bash
   # 基本用法
   python arxivtracker.py --count 10
   ```

   系统会自动：
   - 爬取最新论文信息
   - 下载PDF文件
   - 提取论文信息
   - 分析论文并评分
   - 生成分析报告

### 2.2 查看结果

系统运行完成后，你可以在以下位置查看结果：

- **PDF文件**：`src/arxiv_tracker/data/papers/{date}/`
- **分析报告**：`src/arxiv_tracker/data/reports/{date}/`
- **日志文件**：`src/arxiv_tracker/data/logs/`

## 3. 命令行使用

### 3.1 基本命令

```bash
python arxivtracker.py [OPTIONS]
```

### 3.2 常用选项

| 选项 | 描述 | 示例 |
|------|------|------|
| `--count` | 论文数量 | `--count 20` |
| `--date` | 目标日期 | `--date 20260128` |
| `--categories` | 论文类别 | `--categories cs.AI,cs.LG` |
| `--use-pdf` | 从PDF提取信息 | `--use-pdf` |
| `--no-download` | 跳过PDF下载 | `--no-download` |
| `--no-analysis` | 跳过论文分析 | `--no-analysis` |
| `--no-report` | 跳过报告生成 | `--no-report` |
| `--debug` | 调试模式 | `--debug` |

### 3.3 使用示例

#### 3.3.1 爬取特定数量的论文

```bash
# 爬取并分析15篇论文
python arxivtracker.py --count 15
```

#### 3.3.2 爬取特定日期的论文

```bash
# 爬取2026年1月28日的论文
python arxivtracker.py --date 20260128 --count 10
```

#### 3.3.3 爬取特定类别的论文

```bash
# 爬取AI和机器学习类别的论文
python arxivtracker.py --categories cs.AI,cs.LG --count 12
```

#### 3.3.4 从PDF文件提取信息

```bash
# 从PDF文件提取信息并分析
python arxivtracker.py --count 8 --use-pdf
```

#### 3.3.5 跳过特定步骤

```bash
# 只爬取和下载，不分析和报告
python arxivtracker.py --count 5 --no-analysis --no-report
```

#### 3.3.6 启用调试模式

```bash
# 启用调试模式，查看详细日志
python arxivtracker.py --count 3 --debug
```

## 4. Python API使用

### 4.1 基本用法

```python
from arxiv_tracker import ArxivTracker

# 创建跟踪器实例
tracker = ArxivTracker()

# 运行完整流程
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

### 4.2 模块使用

#### 4.2.1 单独使用爬取模块

```python
from arxiv_tracker.crawler import ArxivCrawler
from arxiv_tracker.utils.config import load_config

# 加载配置
config = load_config()

# 创建爬取器
crawler = ArxivCrawler(config)

# 爬取论文
papers = crawler.crawl(date='20260128')
print(f"爬取了 {len(papers)} 篇论文")

# 查看第一篇论文
if papers:
    print(f"第一篇论文: {papers[0]['title']}")
```

#### 4.2.2 单独使用下载模块

```python
from arxiv_tracker.downloader import ArxivDownloader
from arxiv_tracker.utils.config import load_config

# 加载配置
config = load_config()

# 创建下载器
downloader = ArxivDownloader(config)

# 假设已经有了论文列表
papers = [
    {
        'arxiv_id': '2301.00001',
        'pdf_url': 'https://arxiv.org/pdf/2301.00001.pdf'
    }
]

# 下载PDF文件
downloaded_papers = downloader.download(papers, date='20260128')
print("PDF文件下载完成")

# 查看下载结果
for paper in downloaded_papers:
    if paper.get('pdf_path'):
        print(f"PDF已下载到: {paper['pdf_path']}")
```

#### 4.2.3 单独使用分析模块

```python
from arxiv_tracker.analyzer import ArxivAnalyzer
from arxiv_tracker.utils.config import load_config

# 加载配置
config = load_config()

# 创建分析器
analyzer = ArxivAnalyzer(config)

# 假设已经有了论文列表
papers = [
    {
        'title': 'Test Paper',
        'abstract': 'This is a test abstract.'
    }
]

# 分析论文
analyzed_papers = analyzer.analyze(papers)
print("论文分析完成")

# 查看分析结果
for paper in analyzed_papers:
    if paper.get('score'):
        print(f"论文评分: {paper['score']}")
        print(f"总体评价: {paper.get('overall_evaluation', 'N/A')}")
```

## 5. 辅助脚本

### 5.1 环境设置脚本

```bash
# 自动创建虚拟环境并安装依赖
python scripts/setup_venv.py
```

### 5.2 状态重置脚本

```bash
# 重置所有状态
python scripts/reset_states.py

# 重置特定步骤
python scripts/reset_states.py --step crawling
```

### 5.3 PDF提取脚本

```bash
# 从单个PDF文件提取信息
python scripts/extract_from_pdf.py path/to/paper.pdf

# 从目录中提取所有PDF文件
python scripts/extract_from_pdf.py path/to/papers/
```

### 5.4 摘要检查脚本

```bash
# 测试摘要提取功能
python scripts/check_abstract.py
```

## 6. 配置管理

### 6.1 系统配置

编辑 `config/system_config.json` 文件：

```json
{
    "data_dir": "src/arxiv_tracker/data",
    "pdf_storage": "src/arxiv_tracker/data/papers",
    "report_storage": "src/arxiv_tracker/data/reports",
    "cache_storage": "src/arxiv_tracker/data/cache",
    "log_dir": "src/arxiv_tracker/data/logs",
    "categories": ["cs.AI", "cs.LG"],
    "max_workers": 4,
    "timeout": 30,
    "max_retries": 3,
    "cache_ttl": 86400,
    "default_paper_count": 10
}
```

### 6.2 常用配置项

| 配置项 | 说明 | 建议值 |
|--------|------|--------|
| `categories` | 默认论文类别 | 根据研究领域设置 |
| `max_workers` | 并发线程数 | CPU核心数的1-2倍 |
| `timeout` | 网络超时时间 | 30-60秒 |
| `default_paper_count` | 默认论文数量 | 10-50篇 |

### 6.3 API配置

编辑 `config/api_config.json` 文件：

```json
{
    "dashscope_api_key": "YOUR_API_KEY_HERE",
    "model": "qwen-plus",
    "temperature": 0.3,
    "top_p": 0.8
}
```

## 7. 报告查看

### 7.1 报告类型

系统生成三种类型的报告：

1. **Markdown报告**：`arxiv_report_{date}.md`
2. **JSON报告**：`arxiv_report_{date}.json`
3. **摘要报告**：`arxiv_summary_{date}.md`

### 7.2 查看Markdown报告

使用任何支持Markdown的编辑器打开 `src/arxiv_tracker/data/reports/{date}/arxiv_report_{date}.md` 文件。

**报告内容包括：**
- 报告概览
- 论文列表
- 每篇论文的详细信息
- 分析结果和评分

### 7.3 查看JSON报告

使用JSON查看器或编程语言处理 `src/arxiv_tracker/data/reports/{date}/arxiv_report_{date}.json` 文件。

**报告结构：**
```json
{
    "generated_at": "2026-01-28T12:00:00",
    "report_date": "20260128",
    "total_papers": 10,
    "papers": [
        {
            "arxiv_id": "2301.00001",
            "title": "Test Paper",
            "authors": ["John Doe"],
            "abstract": "...",
            "score": 8.5,
            "analysis": "..."
        }
    ]
}
```

### 7.4 查看摘要报告

打开 `src/arxiv_tracker/data/reports/{date}/arxiv_summary_{date}.md` 文件，查看评分最高的论文和统计信息。

## 8. 数据管理

### 8.1 数据目录结构

```
src/arxiv_tracker/data/
├── papers/          # PDF文件
│   ├── 20260128/     # 按日期组织
│   └── 20260129/
├── reports/         # 分析报告
│   ├── 20260128/
│   └── 20260129/
├── cache/           # 缓存文件
│   ├── cache.json    # 爬取缓存
│   └── state.json    # 系统状态
└── logs/            # 日志文件
    ├── tracker.log   # 系统日志
    └── errors.log    # 错误日志
```

### 8.2 清理旧数据

```bash
# 删除30天前的PDF文件
find src/arxiv_tracker/data/papers -name "*.pdf" -mtime +30 -delete

# 删除30天前的报告文件
find src/arxiv_tracker/data/reports -name "*.md" -o -name "*.json" | xargs -d '\n' rm

# 删除30天前的日志文件
find src/arxiv_tracker/data/logs -name "*.log" -mtime +30 -delete
```

### 8.3 备份数据

```bash
# 备份所有数据
zip -r arxiv_data_backup.zip src/arxiv_tracker/data/

# 备份配置文件
zip -r arxiv_config_backup.zip config/
```

## 9. 常见问题

### 9.1 网络问题

**问题**：爬取失败，显示网络连接错误

**解决方案**：
- 检查网络连接
- 增加超时时间：修改 `config/system_config.json` 中的 `timeout` 值
- 增加重试次数：修改 `config/system_config.json` 中的 `max_retries` 值

### 9.2 API问题

**问题**：分析失败，显示API调用错误

**解决方案**：
- 检查API密钥是否正确
- 检查API配额是否用尽
- 增加API超时时间：修改 `config/api_config.json` 中的 `timeout` 值

### 9.3 PDF提取问题

**问题**：从PDF提取信息失败

**解决方案**：
- 使用 `--use-pdf` 选项重新运行
- 检查PDF文件是否损坏
- 尝试使用网页信息：不使用 `--use-pdf` 选项

### 9.4 资源问题

**问题**：系统运行缓慢或内存不足

**解决方案**：
- 减少 `--count` 值
- 减少 `max_workers` 值
- 增加系统内存
- 清理磁盘空间

### 9.5 权限问题

**问题**：文件操作失败，显示权限错误

**解决方案**：
- 以管理员身份运行命令
- 检查文件和目录权限
- 修改数据存储目录权限

## 10. 高级功能

### 10.1 定时运行

#### 10.1.1 Windows任务计划程序

1. 打开「任务计划程序」
2. 创建新任务
3. 设置触发器（如每天凌晨2点）
4. 设置操作：
   - 程序/脚本：`python.exe`
   - 添加参数：`arxivtracker.py --count 30`
   - 起始于：项目根目录

#### 10.1.2 Linux/macOS Crontab

```bash
# 编辑crontab
crontab -e

# 添加定时任务（每天凌晨2点运行）
0 2 * * * cd /path/to/arxiv-tracker && venv/bin/python arxivtracker.py --count 30
```

### 10.2 自定义分析

#### 10.2.1 使用Python API进行自定义分析

```python
from arxiv_tracker import ArxivTracker
import pandas as pd

# 运行跟踪器
tracker = ArxivTracker()
results = tracker.run(count=50, categories=['cs.AI', 'cs.LG'])

# 转换为DataFrame
df = pd.DataFrame(results)

# 自定义分析
print("=== 自定义分析 ===")
print(f"总论文数: {len(df)}")
print(f"平均评分: {df['score'].mean():.2f}")

# 按类别分析
category_stats = df.groupby('category')['score'].agg(['mean', 'count'])
print("\n=== 按类别分析 ===")
print(category_stats)

# 评分分布
print("\n=== 评分分布 ===")
score_dist = df['score'].value_counts().sort_index()
print(score_dist)
```

### 10.3 集成到其他系统

#### 10.3.1 与Web应用集成

```python
from flask import Flask, jsonify
from arxiv_tracker import ArxivTracker

app = Flask(__name__)
tracker = ArxivTracker()

@app.route('/api/papers', methods=['GET'])
def get_papers():
    """获取论文列表"""
    count = request.args.get('count', 10, type=int)
    categories = request.args.get('categories', 'cs.AI').split(',')
    
    try:
        results = tracker.run(count=count, categories=categories)
        return jsonify({
            'status': 'success',
            'papers': results
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
```

## 11. 性能优化

### 11.1 提高爬取速度

- **增加并发数**：修改 `config/system_config.json` 中的 `max_workers` 值
- **使用缓存**：系统会自动缓存爬取结果
- **减少论文数量**：使用 `--count` 选项限制数量

### 11.2 减少内存使用

- **分批处理**：每次处理较少的论文
- **清理缓存**：定期清理 `src/arxiv_tracker/data/cache/` 目录
- **关闭调试模式**：不使用 `--debug` 选项

### 11.3 节省API调用

- **复用分析结果**：系统会缓存分析结果
- **选择性分析**：只分析重要的论文
- **调整分析参数**：修改 `config/api_config.json` 中的模型参数

## 12. 故障排除

### 12.1 查看日志

```bash
# 查看系统日志
tail -f src/arxiv_tracker/data/logs/tracker.log

# 查看错误日志
tail -f src/arxiv_tracker/data/logs/errors.log
```

### 12.2 启用调试模式

```bash
# 启用调试模式运行
python arxivtracker.py --debug --count 1
```

### 12.3 测试网络连接

```bash
# 测试arXiv网站连接
ping arxiv.org

# 测试API连接
ping dashscope.aliyuncs.com
```

### 12.4 检查系统状态

```bash
# 查看系统状态
python -c "import json; print(json.load(open('src/arxiv_tracker/data/cache/state.json', 'r', encoding='utf-8')))"

# 重置系统状态
python scripts/reset_states.py
```

## 13. 总结

arXiv论文跟踪系统是一个功能强大的工具，可以帮助你：

- **自动跟踪**：定期爬取最新论文
- **智能分析**：使用LLM评估论文质量
- **快速筛选**：基于评分发现高价值论文
- **全面报告**：生成详细的分析报告

通过本文档的指导，你应该能够熟练使用系统的各种功能，定制适合自己的论文跟踪流程。如果在使用过程中遇到问题，请参考常见问题和故障排除部分，或联系技术支持。

**祝你使用愉快！**
