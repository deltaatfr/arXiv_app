# arXiv论文跟踪系统API参考文档

## 1. 概述

arXiv论文跟踪系统提供了一套完整的API，支持从命令行、Python代码和其他系统中调用。本文档详细说明了系统的API接口、参数和使用方法。

## 2. 命令行API

### 2.1 主命令

```bash
python arxivtracker.py [OPTIONS]
```

### 2.2 命令行选项

| 选项 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `--count` | 整数 | 10 | 要分析的论文数量 |
| `--date` | 字符串 | None | 目标日期（格式：YYYYMMDD），默认使用当前日期 |
| `--categories` | 字符串 | None | 论文类别，逗号分隔（如：cs.AI,cs.LG） |
| `--use-pdf` | 布尔值 | False | 从PDF文件提取信息，而不是从网页 |
| `--no-download` | 布尔值 | False | 跳过PDF下载步骤 |
| `--no-analysis` | 布尔值 | False | 跳过论文分析步骤 |
| `--no-report` | 布尔值 | False | 跳过报告生成步骤 |
| `--config` | 字符串 | None | 自定义配置文件路径 |
| `--debug` | 布尔值 | False | 启用调试模式，显示详细日志 |

### 2.3 使用示例

#### 2.3.1 基本用法

```bash
# 爬取并分析10篇最新论文
python arxivtracker.py --count 10
```

#### 2.3.2 指定日期和类别

```bash
# 爬取2026年1月28日的AI和LG类别的论文
python arxivtracker.py --date 20260128 --categories cs.AI,cs.LG --count 15
```

#### 2.3.3 从PDF提取信息

```bash
# 从PDF文件提取信息并分析
python arxivtracker.py --count 8 --use-pdf
```

#### 2.3.4 跳过特定步骤

```bash
# 只爬取和下载，不分析和报告
python arxivtracker.py --count 5 --no-analysis --no-report
```

## 3. Python API

### 3.1 主类 `ArxivTracker`

#### 3.1.1 初始化

```python
from arxiv_tracker import ArxivTracker

# 创建默认配置的跟踪器
tracker = ArxivTracker()

# 使用自定义配置
tracker = ArxivTracker(config_path='path/to/config.json')
```

#### 3.1.2 主要方法

##### `run(categories=None, count=None, use_pdf=False, date=None)`

运行完整的论文跟踪流程。

**参数：**
- `categories`：列表，论文类别列表（如 `['cs.AI', 'cs.LG']`）
- `count`：整数，要分析的论文数量
- `use_pdf`：布尔值，是否从PDF文件提取信息
- `date`：字符串，目标日期（格式：YYYYMMDD）

**返回值：**
- 论文对象列表，每个对象包含完整的论文信息和分析结果

**示例：**

```python
# 运行完整流程
results = tracker.run(
    categories=['cs.AI', 'cs.LG'],
    count=10,
    use_pdf=True,
    date='20260128'
)

# 处理结果
for paper in results:
    print(f"Title: {paper['title']}")
    print(f"Authors: {', '.join(paper['authors'])}")
    print(f"Score: {paper.get('score', 'N/A')}")
    print()
```

### 3.2 模块API

#### 3.2.1 爬取模块

```python
from arxiv_tracker.crawler import ArxivCrawler

# 创建爬取器
crawler = ArxivCrawler(config)

# 爬取论文
papers = crawler.crawl(date='20260128')
print(f"爬取了 {len(papers)} 篇论文")
```

#### 3.2.2 下载模块

```python
from arxiv_tracker.downloader import ArxivDownloader

# 创建下载器
downloader = ArxivDownloader(config)

# 下载PDF文件
downloaded_papers = downloader.download(papers, date='20260128')
print("PDF文件下载完成")
```

#### 3.2.3 提取模块

```python
from arxiv_tracker.extractor import ArxivExtractor

# 创建提取器
extractor = ArxivExtractor(config)

# 从PDF提取信息
extracted_papers = extractor.extract_from_pdfs(papers, date='20260128')
print("信息提取完成")

# 从网页提取信息
extracted_papers = extractor.extract_from_web(papers)
print("信息提取完成")
```

#### 3.2.4 分析模块

```python
from arxiv_tracker.analyzer import ArxivAnalyzer

# 创建分析器
analyzer = ArxivAnalyzer(config)

# 分析论文
analyzed_papers = analyzer.analyze(papers)
print("论文分析完成")
```

#### 3.2.5 报告模块

```python
from arxiv_tracker.reporter import ArxivReporter

# 创建报告生成器
reporter = ArxivReporter(config)

# 生成报告
reporter.generate(papers, date='20260128')
print("报告生成完成")
```

### 3.3 工具API

#### 3.3.1 配置管理

```python
from arxiv_tracker.utils.config import load_config, save_config

# 加载配置
config = load_config()
print(f"当前配置: {config}")

# 修改配置
config['default_paper_count'] = 20

# 保存配置
save_config(config, 'new_config.json')
print("配置已保存")
```

#### 3.3.2 状态管理

```python
from arxiv_tracker.utils.state_manager import get_state_manager

# 获取状态管理器
state = get_state_manager()

# 获取状态
last_run = state.get('last_run')
print(f"上次运行时间: {last_run}")

# 设置状态
state.set('custom_key', 'custom_value')
print("状态已更新")

# 标记步骤完成
state.mark_step_completed('crawling')
print("步骤标记完成")

# 重置状态
state.reset()
print("状态已重置")
```

#### 3.3.3 缓存管理

```python
from arxiv_tracker.utils.cache_manager import get_cache_manager

# 获取缓存管理器
cache = get_cache_manager()

# 获取缓存
cached_data = cache.get('papers_20260128')
print(f"缓存数据: {cached_data}")

# 设置缓存
cache.set('papers_20260128', papers)
print("缓存已更新")

# 清空缓存
cache.clear()
print("缓存已清空")
```

#### 3.3.4 资源监控

```python
from arxiv_tracker.utils.resource_monitor import get_resource_monitor

# 获取资源监控器
monitor = get_resource_monitor()

# 获取系统统计信息
stats = monitor.get_system_stats()
print(f"CPU使用率: {stats['cpu']['percent']}%")
print(f"内存使用: {stats['memory']['used_gb']}GB")

# 记录资源使用情况
monitor.log_stats("处理前")
# 执行任务
monitor.log_stats("处理后")

# 检查资源使用情况
if not monitor.check_resources(cpu_threshold=80, memory_threshold=80):
    print("资源使用过高")
else:
    print("资源使用正常")
```

#### 3.3.5 文件工具

```python
from arxiv_tracker.utils.file_utils import get_file_utils

# 获取文件工具
files = get_file_utils()

# 确保目录存在
files.ensure_dir('path/to/dir')

# 写入JSON文件
files.write_json({'key': 'value'}, 'data.json')

# 读取JSON文件
data = files.read_json('data.json')
print(f"读取的数据: {data}")

# 写入文本文件
files.write_text('Hello, world!', 'text.txt')

# 读取文本文件
content = files.read_text('text.txt')
print(f"读取的内容: {content}")

# 复制文件
files.copy_file('source.txt', 'destination.txt')

# 删除文件
files.delete_file('temp.txt')
```

## 4. 辅助脚本API

### 4.1 环境设置脚本

```bash
python scripts/setup_venv.py
```

**功能：** 自动创建虚拟环境并安装依赖包。

**使用方法：** 直接运行，无需参数。

### 4.2 状态重置脚本

```bash
python scripts/reset_states.py [--step STEP]
```

**功能：** 重置系统状态。

**参数：**
- `--step`：可选，指定要重置的步骤名称。

**使用方法：**

```bash
# 重置所有状态
python scripts/reset_states.py

# 重置特定步骤
python scripts/reset_states.py --step crawling
```

### 4.3 摘要检查脚本

```bash
python scripts/check_abstract.py
```

**功能：** 测试摘要提取功能。

**使用方法：** 直接运行，无需参数。

### 4.4 PDF提取脚本

```bash
python scripts/extract_from_pdf.py PATH
```

**功能：** 从PDF文件中提取信息。

**参数：**
- `PATH`：必需，PDF文件路径或包含PDF文件的目录。

**使用方法：**

```bash
# 处理单个PDF文件
python scripts/extract_from_pdf.py path/to/paper.pdf

# 处理目录中的所有PDF文件
python scripts/extract_from_pdf.py path/to/papers/
```

## 5. 配置API

### 5.1 系统配置文件

配置文件路径：`config/system_config.json`

**配置项：**

| 配置项 | 类型 | 默认值 | 描述 |
|--------|------|--------|------|
| `data_dir` | 字符串 | `src/arxiv_tracker/data` | 数据存储根目录 |
| `pdf_storage` | 字符串 | `src/arxiv_tracker/data/papers` | PDF文件存储目录 |
| `report_storage` | 字符串 | `src/arxiv_tracker/data/reports` | 报告存储目录 |
| `cache_storage` | 字符串 | `src/arxiv_tracker/data/cache` | 缓存存储目录 |
| `log_dir` | 字符串 | `src/arxiv_tracker/data/logs` | 日志存储目录 |
| `categories` | 列表 | `["cs.AI", "cs.LG"]` | 默认论文类别 |
| `max_workers` | 整数 | 4 | 并发工作线程数 |
| `timeout` | 整数 | 30 | 网络请求超时时间（秒） |
| `max_retries` | 整数 | 3 | 网络请求最大重试次数 |
| `cache_ttl` | 整数 | 86400 | 缓存过期时间（秒） |
| `default_paper_count` | 整数 | 10 | 默认论文数量 |

### 5.2 API配置文件

配置文件路径：`config/api_config.json`

**配置项：**

| 配置项 | 类型 | 默认值 | 描述 |
|--------|------|--------|------|
| `dashscope_api_key` | 字符串 | `"YOUR_API_KEY_HERE"` | DashScope API密钥 |
| `api_endpoint` | 字符串 | `"https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"` | API端点URL |
| `max_retries` | 整数 | 3 | API请求最大重试次数 |
| `timeout` | 整数 | 60 | API请求超时时间（秒） |
| `model` | 字符串 | `"qwen-plus"` | 使用的模型名称 |
| `temperature` | 浮点数 | 0.3 | 生成温度参数 |
| `top_p` | 浮点数 | 0.8 | 生成top_p参数 |

### 5.3 类别配置文件

配置文件路径：`config/categories.json`

**配置项：**

```json
{
    "categories": [
        {
            "id": "cs.AI",
            "name": "人工智能",
            "full_name": "Computer Science - Artificial Intelligence"
        },
        {
            "id": "cs.LG",
            "name": "机器学习",
            "full_name": "Computer Science - Machine Learning"
        }
        // 更多类别...
    ]
}
```

### 5.4 日志配置文件

配置文件路径：`config/logging_config.json`

**配置项：** 遵循Python标准logging模块配置格式。

## 6. 数据结构API

### 6.1 论文对象

```python
{
    "arxiv_id": "2301.00001",          # arXiv论文ID
    "title": "Test Paper Title",        # 论文标题
    "authors": ["John Doe", "Jane Smith"],  # 作者列表
    "abstract": "This is a test abstract.",  # 摘要
    "category": "cs.AI",                # 论文类别
    "pdf_url": "https://arxiv.org/pdf/2301.00001.pdf",  # PDF链接
    "url": "https://arxiv.org/abs/2301.00001",  # 网页链接
    "pdf_path": "src/arxiv_tracker/data/papers/20260128/2301.00001.pdf",  # 本地路径
    "crawl_date": "20260128",           # 爬取日期
    "score": 8.5,                        # 评分
    "research_question": "...",          # 研究问题分析
    "method_innovation": "...",          # 方法创新分析
    "experimental_results": "...",       # 实验结果分析
    "application_value": "...",          # 应用价值分析
    "limitations": "...",                # 局限性分析
    "overall_evaluation": "..."          # 总体评价
}
```

### 6.2 分析结果

```python
{
    "research_question": "论文解决了什么问题？为什么这个问题重要？",
    "method_innovation": "论文提出了什么新方法或技术？与现有方法相比有什么优势？",
    "experimental_results": "论文报告了哪些关键实验结果？结果是否令人信服？",
    "application_value": "论文的研究成果有什么实际应用价值？",
    "limitations": "论文存在哪些局限性或未来工作方向？",
    "overall_evaluation": "对论文的整体质量和贡献进行评价。",
    "score": 8.5  # 1-10分的评分
}
```

### 6.3 系统状态

```python
{
    "last_run": "2026-01-28T12:00:00",  # 上次运行时间
    "completed_steps": ["crawling", "downloading", "extraction", "analysis", "reporting"],  # 已完成步骤
    "current_step": null,  # 当前步骤
    "papers": [],  # 论文列表
    "statistics": {  # 统计信息
        "total_papers": 10,
        "success_rate": 1.0,
        "average_score": 8.2
    }
}
```

### 6.4 系统统计信息

```python
{
    "cpu": {
        "percent": 25.5,  # CPU使用率
        "count": 8        # CPU核心数
    },
    "memory": {
        "used_gb": 4.5,   # 已用内存
        "total_gb": 16.0,  # 总内存
        "percent": 28.1    # 内存使用率
    },
    "disk": {
        "used_gb": 100.0,  # 已用磁盘
        "total_gb": 500.0, # 总磁盘
        "percent": 20.0    # 磁盘使用率
    },
    "network": {
        "sent_mb": 10.5,   # 发送数据
        "recv_mb": 20.3    # 接收数据
    },
    "uptime": 3600.0  # 运行时间（秒）
}
```

## 7. 错误处理API

### 7.1 异常类型

| 异常类型 | 描述 | 处理方法 |
|----------|------|----------|
| `requests.exceptions.RequestException` | 网络请求异常 | 检查网络连接，增加超时时间 |
| `PyPDF2.errors.PdfReadError` | PDF读取异常 | 跳过该文件，使用网页信息 |
| `ValueError` | 数据格式异常 | 检查输入数据格式 |
| `FileNotFoundError` | 文件不存在异常 | 检查文件路径，创建必要的目录 |
| `PermissionError` | 权限异常 | 检查文件权限 |

### 7.2 错误处理示例

```python
try:
    # 尝试运行跟踪器
    results = tracker.run(count=10)
    print(f"成功处理 {len(results)} 篇论文")
except requests.exceptions.RequestException as e:
    print(f"网络错误: {e}")
    # 使用缓存数据
    cached_results = load_cached_results()
    print(f"使用缓存数据: {len(cached_results)} 篇论文")
except PyPDF2.errors.PdfReadError as e:
    print(f"PDF读取错误: {e}")
    # 跳过PDF提取，使用网页信息
    results = tracker.run(count=10, use_pdf=False)
except Exception as e:
    print(f"未知错误: {e}")
    # 记录错误并退出
    import traceback
    traceback.print_exc()
```

## 8. 集成示例

### 8.1 与定时任务集成

```python
# scheduled_task.py
import schedule
import time
from arxiv_tracker import ArxivTracker

def run_tracker():
    print("开始运行arXiv论文跟踪系统...")
    tracker = ArxivTracker()
    try:
        results = tracker.run(count=20)
        print(f"成功处理 {len(results)} 篇论文")
    except Exception as e:
        print(f"运行失败: {e}")

# 每天凌晨2点运行
schedule.every().day.at("02:00").do(run_tracker)

print("定时任务已启动，每天凌晨2点运行")
while True:
    schedule.run_pending()
    time.sleep(60)
```

### 8.2 与Web应用集成

```python
# web_app.py
from flask import Flask, jsonify, request
from arxiv_tracker import ArxivTracker

app = Flask(__name__)
tracker = ArxivTracker()

@app.route('/api/arxiv', methods=['GET'])
def get_arxiv_papers():
    """获取arXiv论文"""
    # 获取参数
    count = request.args.get('count', 10, type=int)
    categories = request.args.get('categories', 'cs.AI,cs.LG')
    categories = categories.split(',')
    date = request.args.get('date')
    use_pdf = request.args.get('use_pdf', 'false').lower() == 'true'
    
    try:
        # 运行跟踪器
        results = tracker.run(
            categories=categories,
            count=count,
            use_pdf=use_pdf,
            date=date
        )
        
        # 格式化响应
        response = {
            'status': 'success',
            'total': len(results),
            'papers': results
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
```

### 8.3 与数据分析工具集成

```python
# data_analysis.py
import pandas as pd
from arxiv_tracker import ArxivTracker

# 运行跟踪器
tracker = ArxivTracker()
results = tracker.run(count=50, categories=['cs.AI', 'cs.LG'])

# 转换为DataFrame
df = pd.DataFrame(results)

# 分析数据
print("\n=== 数据分析 ===")
print(f"总论文数: {len(df)}")
print(f"平均评分: {df['score'].mean():.2f}")
print(f"评分标准差: {df['score'].std():.2f}")

# 按类别分析
print("\n=== 按类别分析 ===")
category_stats = df.groupby('category')['score'].agg(['mean', 'count'])
print(category_stats)

# 按评分排序
top_papers = df.sort_values('score', ascending=False).head(5)
print("\n=== 评分最高的5篇论文 ===")
for i, (_, paper) in enumerate(top_papers.iterrows(), 1):
    print(f"{i}. {paper['title']} (评分: {paper['score']})")
    print(f"   作者: {', '.join(paper['authors'])}")
    print()
```

## 9. 最佳实践

### 9.1 API使用建议

1. **合理设置并发数**：根据系统资源设置适当的 `max_workers`，避免资源耗尽。

2. **使用缓存**：对于频繁访问的数据，使用缓存减少重复计算和网络请求。

3. **错误处理**：实现完善的错误处理机制，确保系统在各种异常情况下能够正常运行。

4. **资源监控**：定期监控系统资源使用情况，及时发现和解决资源问题。

5. **配置管理**：使用配置文件管理系统参数，避免硬编码。

6. **日志记录**：使用适当的日志级别记录系统运行情况，便于调试和问题排查。

7. **API密钥保护**：不要将API密钥硬编码在代码中，使用配置文件或环境变量。

8. **批量处理**：对于大量数据，使用批量处理减少API调用次数。

### 9.2 性能优化建议

1. **减少网络请求**：使用缓存和批量请求减少网络请求次数。

2. **优化PDF处理**：对于大型PDF文件，使用流式处理减少内存使用。

3. **并行处理**：使用并发处理提高系统效率，但要注意资源限制。

4. **延迟加载**：对于非关键数据，使用延迟加载减少启动时间。

5. **内存管理**：及时释放不再使用的资源，避免内存泄漏。

6. **数据库优化**：如果使用数据库，合理设计表结构和索引。

7. **代码优化**：定期审查和优化代码，消除性能瓶颈。

### 9.3 安全建议

1. **输入验证**：验证所有用户输入，避免注入攻击。

2. **权限控制**：合理设置文件和目录权限，避免未授权访问。

3. **数据加密**：对敏感数据（如API密钥）进行加密存储。

4. **网络安全**：使用HTTPS协议，避免明文传输敏感数据。

5. **依赖管理**：定期更新依赖包，修复安全漏洞。

6. **日志安全**：避免在日志中记录敏感信息。

7. **访问控制**：实现适当的访问控制机制，限制系统功能的使用。

## 10. 故障排除

### 10.1 常见问题

| 问题 | 可能原因 | 解决方案 |
|------|---------|----------|
| 网络连接失败 | 网络不稳定或防火墙阻止 | 检查网络连接，增加超时时间 |
| API调用失败 | API密钥无效或配额用尽 | 检查API密钥，等待配额重置 |
| PDF提取失败 | PDF文件损坏或加密 | 跳过该文件，使用网页信息 |
| 内存不足 | 处理论文数量过多 | 减少处理数量，增加系统内存 |
| 磁盘空间不足 | 下载的PDF文件过多 | 清理旧文件，增加磁盘空间 |
| 权限错误 | 文件权限不足 | 检查文件权限，以管理员身份运行 |
| 配置错误 | 配置文件格式不正确 | 检查配置文件格式，使用默认配置 |

### 10.2 调试技巧

1. **启用调试模式**：使用 `--debug` 参数运行系统，查看详细日志。

2. **检查日志文件**：查看 `src/arxiv_tracker/data/logs/` 目录下的日志文件。

3. **测试单个模块**：使用辅助脚本测试单个模块的功能。

4. **使用断点**：在关键位置设置断点，检查变量值。

5. **简化配置**：使用默认配置，逐步添加自定义配置。

6. **隔离问题**：逐步禁用系统功能，确定问题所在。

7. **查看系统状态**：使用状态管理API查看系统状态。

8. **检查资源使用**：使用资源监控API检查系统资源使用情况。

## 11. 版本历史

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| 1.0.0 | 2026-01-28 | 初始版本，包含完整的论文跟踪、分析和报告功能 |

## 12. 联系与支持

如果您在使用API过程中遇到问题，请通过以下方式获取支持：

- **项目文档**：查看 `docs/` 目录下的详细文档
- **GitHub Issues**：在项目仓库中提交问题
- **邮件支持**：contact@arxiv-tracker.example

## 13. 许可证

本API参考文档和相关代码遵循MIT许可证。
