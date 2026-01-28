# arXiv论文跟踪系统维护文档

## 1. 系统架构概览

### 1.1 模块结构

| 模块 | 职责 | 文件位置 | 依赖 |
|------|------|----------|------|
| 爬虫模块 | 爬取论文信息 | src/arxiv_tracker/crawler.py | requests, beautifulsoup4 |
| 下载模块 | 下载PDF文件 | src/arxiv_tracker/downloader.py | requests, tqdm |
| 提取模块 | 提取论文信息 | src/arxiv_tracker/extractor.py | PyPDF2 |
| 分析模块 | 分析论文内容 | src/arxiv_tracker/analyzer.py | dashscope |
| 报告模块 | 生成分析报告 | src/arxiv_tracker/reporter.py | markdown |
| 工具模块 | 提供辅助功能 | src/arxiv_tracker/utils/ | psutil, logging |

### 1.2 数据流

```
爬取模块 → 下载模块 → 提取模块 → 分析模块 → 报告模块
     ↓         ↓         ↓         ↓         ↓
  缓存     PDF文件     提取信息     分析结果     报告文件
```

## 2. 日常维护

### 2.1 系统监控

1. **日志监控**

   ```bash
   # 实时查看系统日志
   tail -f src/arxiv_tracker/data/logs/tracker.log

   # 查看错误日志
   grep -i error src/arxiv_tracker/data/logs/tracker.log

   # 查看特定日期的日志
   grep "2026-01-28" src/arxiv_tracker/data/logs/tracker.log
   ```

2. **资源监控**

   ```bash
   # 监控Python进程
   # Windows
   tasklist | findstr python

   # macOS/Linux
   ps aux | grep python | grep -v grep

   # 监控内存使用
   # Windows
   systeminfo | findstr "Available Physical Memory"

   # macOS/Linux
   free -h
   ```

3. **磁盘空间监控**

   ```bash
   # 检查数据目录大小
   # Windows
   dir src\arxiv_tracker\data

   # macOS/Linux
   du -sh src/arxiv_tracker/data/

   # 检查总体磁盘空间
   # Windows
   fsutil volume diskfree C:

   # macOS/Linux
   df -h
   ```

### 2.2 数据清理

1. **定期清理旧数据**

   ```bash
   # 删除30天前的PDF文件
   # Windows PowerShell
   Get-ChildItem -Path src\arxiv_tracker\data\papers -Recurse -Filter "*.pdf" | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-30) } | Remove-Item -Force

   # macOS/Linux
   find src/arxiv_tracker/data/papers -name "*.pdf" -mtime +30 -delete

   # 删除30天前的报告文件
   # Windows PowerShell
   Get-ChildItem -Path src\arxiv_tracker\data\reports -Recurse -Include "*.md", "*.json" | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-30) } | Remove-Item -Force

   # macOS/Linux
   find src/arxiv_tracker/data/reports -name "*.md" -o -name "*.json" | xargs -d '\n' rm

   # 删除30天前的日志文件
   # Windows PowerShell
   Get-ChildItem -Path src\arxiv_tracker\data\logs -Recurse -Filter "*.log" | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-30) } | Remove-Item -Force

   # macOS/Linux
   find src/arxiv_tracker/data/logs -name "*.log" -mtime +30 -delete
   ```

2. **清理缓存**

   ```bash
   # 清理爬取缓存
   # Windows
   Remove-Item -Path src\arxiv_tracker\data\cache\cache.json -Force

   # macOS/Linux
   rm src/arxiv_tracker/data/cache/cache.json

   # 清理状态文件
   # Windows
   Remove-Item -Path src\arxiv_tracker\data\cache\state.json -Force

   # macOS/Linux
   rm src/arxiv_tracker/data/cache/state.json
   ```

3. **清理临时文件**

   ```bash
   # 清理Python临时文件
   # Windows
   Remove-Item -Path "*.pyc" -Recurse -Force
   Remove-Item -Path "__pycache__" -Recurse -Force

   # macOS/Linux
   find . -name "*.pyc" -delete
   find . -name "__pycache__" -type d -exec rm -rf {} \;
   ```

### 2.3 备份策略

1. **数据备份**

   ```bash
   # 备份所有数据
   # Windows PowerShell
   Compress-Archive -Path src\arxiv_tracker\data -DestinationPath arxiv_data_backup_$(Get-Date -Format "yyyyMMdd").zip

   # macOS/Linux
   zip -r arxiv_data_backup_$(date +%Y%m%d).zip src/arxiv_tracker/data/

   # 备份配置文件
   # Windows PowerShell
   Compress-Archive -Path config -DestinationPath arxiv_config_backup_$(Get-Date -Format "yyyyMMdd").zip

   # macOS/Linux
   zip -r arxiv_config_backup_$(date +%Y%m%d).zip config/
   ```

2. **自动备份**

   创建定时备份脚本 `scripts/backup_data.py`：

   ```python
   #!/usr/bin/env python3
   """
   数据备份脚本
   """

   import os
   import zipfile
   from datetime import datetime

   def backup_data():
       """备份数据"""
       # 当前日期
       date_str = datetime.now().strftime("%Y%m%d")
       
       # 备份数据目录
       data_dir = "src/arxiv_tracker/data"
       backup_file = f"arxiv_data_backup_{date_str}.zip"
       
       print(f"开始备份数据到 {backup_file}")
       
       with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
           for root, _, files in os.walk(data_dir):
               for file in files:
                   file_path = os.path.join(root, file)
                   arcname = os.path.relpath(file_path, os.path.dirname(data_dir))
                   zipf.write(file_path, arcname)
       
       print(f"数据备份完成: {backup_file}")
       
       # 备份配置目录
       config_dir = "config"
       config_backup = f"arxiv_config_backup_{date_str}.zip"
       
       print(f"开始备份配置到 {config_backup}")
       
       with zipfile.ZipFile(config_backup, 'w', zipfile.ZIP_DEFLATED) as zipf:
           for root, _, files in os.walk(config_dir):
               for file in files:
                   file_path = os.path.join(root, file)
                   arcname = os.path.relpath(file_path, os.path.dirname(config_dir))
                   zipf.write(file_path, arcname)
       
       print(f"配置备份完成: {config_backup}")

   if __name__ == "__main__":
       backup_data()
   ```

   运行：

   ```bash
   python scripts/backup_data.py
   ```

### 2.4 依赖管理

1. **更新依赖**

   ```bash
   # 激活虚拟环境
   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate

   # 更新所有依赖
   pip install --upgrade -r requirements.txt

   # 更新单个依赖
   pip install --upgrade requests
   pip install --upgrade beautifulsoup4
   pip install --upgrade PyPDF2
   pip install --upgrade dashscope
   ```

2. **检查依赖版本**

   ```bash
   # 查看所有依赖版本
   pip list

   # 检查过期依赖
   pip list --outdated
   ```

3. **修复依赖冲突**

   ```bash
   # 生成依赖树
   pip show -f requests

   # 卸载冲突依赖
   pip uninstall conflicting-package

   # 重新安装
   pip install -r requirements.txt
   ```

## 3. 故障排除

### 3.1 常见错误及解决方案

| 错误类型 | 错误信息 | 可能原因 | 解决方案 |
|---------|---------|---------|----------|
| 网络错误 | ConnectTimeoutError | 网络连接超时 | 检查网络连接，增加超时时间 |
| 网络错误 | SSLError | SSL证书错误 | 更新证书，使用代理 |
| 网络错误 | HTTPError 403 | 被网站封禁 | 减少请求频率，使用代理 |
| API错误 | APIKeyError | API密钥无效 | 检查API密钥配置 |
| API错误 | RateLimitError | API调用频率超限 | 减少分析论文数量 |
| PDF错误 | PDFReadError | PDF文件损坏 | 重新下载PDF文件 |
| PDF错误 | EmptyFileError | PDF文件为空 | 跳过该文件，使用网页信息 |
| 内存错误 | MemoryError | 内存不足 | 减少并发数，分批处理 |
| 权限错误 | PermissionError | 文件权限不足 | 以管理员身份运行，检查权限 |
| 配置错误 | ConfigError | 配置文件无效 | 检查配置文件格式 |

### 3.2 详细故障排除步骤

#### 3.2.1 网络连接问题

1. **检查网络连接**

   ```bash
   # 测试基本网络连接
   ping google.com

   # 测试arXiv网站连接
   ping arxiv.org

   # 测试API连接
   ping dashscope.aliyuncs.com
   ```

2. **测试HTTP请求**

   ```bash
   # 使用curl测试（如果可用）
   curl -I https://arxiv.org
   curl -I https://dashscope.aliyuncs.com

   # 使用Python测试
   python -c "import requests; print(requests.get('https://arxiv.org', timeout=10).status_code)"
   ```

3. **检查代理设置**

   ```bash
   # 查看系统代理设置
   # Windows
   netsh winhttp show proxy

   # macOS/Linux
   env | grep -i proxy
   ```

4. **修改网络配置**

   编辑 `config/system_config.json` 文件：

   ```json
   {
       "timeout": 60,      # 增加超时时间
       "max_retries": 5,   # 增加重试次数
       "proxy": "http://your-proxy-server:port"  # 添加代理
   }
   ```

#### 3.2.2 API调用问题

1. **检查API密钥**

   ```bash
   # 查看API配置
   cat config/api_config.json

   # 测试API密钥
   python -c "
   import json
   import requests
   config = json.load(open('config/api_config.json'))
   api_key = config.get('dashscope_api_key')
   if not api_key or api_key == 'YOUR_API_KEY_HERE':
       print('API密钥未配置')
   else:
       print('API密钥已配置')
   "
   ```

2. **测试API连接**

   ```bash
   # 使用Python测试API连接
   python -c "
   import json
   import requests
   config = json.load(open('config/api_config.json'))
   api_key = config.get('dashscope_api_key')
   if api_key and api_key != 'YOUR_API_KEY_HERE':
       headers = {'Authorization': f'Bearer {api_key}'}
       try:
           response = requests.get('https://dashscope.aliyuncs.com/api/v1/services', headers=headers, timeout=10)
           print(f'API连接状态: {response.status_code}')
       except Exception as e:
           print(f'API连接错误: {e}')
   else:
       print('API密钥未配置')
   "
   ```

3. **检查API配额**

   访问阿里云DashScope控制台，查看API调用配额和使用情况。

4. **修改API配置**

   编辑 `config/api_config.json` 文件：

   ```json
   {
       "timeout": 120,     # 增加API超时时间
       "max_retries": 5,   # 增加重试次数
       "temperature": 0.1  # 减少随机性，提高稳定性
   }
   ```

#### 3.2.3 PDF提取问题

1. **检查PDF文件**

   ```bash
   # 检查PDF文件是否存在
   ls -la src/arxiv_tracker/data/papers/20260128/

   # 检查PDF文件大小
   # Windows
   Get-ChildItem -Path src\arxiv_tracker\data\papers\20260128\*.pdf | Select-Object Name, Length

   # macOS/Linux
   ls -lh src/arxiv_tracker/data/papers/20260128/
   ```

2. **测试PDF提取**

   ```bash
   # 使用辅助脚本测试
   python scripts/extract_from_pdf.py src/arxiv_tracker/data/papers/20260128/your-paper.pdf

   # 或使用Python直接测试
   python -c "
   from PyPDF2 import PdfReader
   try:
       reader = PdfReader('src/arxiv_tracker/data/papers/20260128/your-paper.pdf')
       print(f'PDF页数: {len(reader.pages)}')
       page = reader.pages[0]
       text = page.extract_text()
       print(f'第一页文本长度: {len(text)}')
   except Exception as e:
       print(f'PDF提取错误: {e}')
   "
   ```

3. **使用网页信息作为备选**

   不使用 `--use-pdf` 选项，系统会自动从网页获取信息：

   ```bash
   python arxivtracker.py --count 5
   ```

#### 3.2.4 内存和性能问题

1. **检查系统资源**

   ```bash
   # 检查内存使用
   # Windows
   systeminfo | findstr "Total Physical Memory"
   systeminfo | findstr "Available Physical Memory"

   # macOS/Linux
   free -h

   # 检查CPU使用
   # Windows
   tasklist | findstr python

   # macOS/Linux
   top -p $(pgrep -f python)
   ```

2. **优化系统配置**

   编辑 `config/system_config.json` 文件：

   ```json
   {
       "max_workers": 2,            # 减少并发数
       "default_paper_count": 10,    # 减少默认论文数量
       "batch_size": 5               # 分批处理
   }
   ```

3. **使用分批处理**

   ```bash
   # 分批处理论文
   python arxivtracker.py --count 10
   python arxivtracker.py --count 10 --offset 10
   python arxivtracker.py --count 10 --offset 20
   ```

### 3.3 日志分析

1. **查看详细日志**

   ```bash
   # 查看最近的日志
   # Windows
   Get-Content -Path src\arxiv_tracker\data\logs\tracker.log -Tail 100

   # macOS/Linux
   tail -n 100 src/arxiv_tracker/data/logs/tracker.log

   # 搜索错误信息
   # Windows
   Select-String -Path src\arxiv_tracker\data\logs\tracker.log -Pattern "ERROR"

   # macOS/Linux
   grep -i error src/arxiv_tracker/data/logs/tracker.log

   # 搜索特定时间段的日志
   # Windows
   Select-String -Path src\arxiv_tracker\data\logs\tracker.log -Pattern "2026-01-28"

   # macOS/Linux
   grep "2026-01-28" src/arxiv_tracker/data/logs/tracker.log
   ```

2. **启用调试日志**

   编辑 `config/logging_config.json` 文件：

   ```json
   {
       "loggers": {
           "": {
               "handlers": ["console", "file"],
               "level": "DEBUG",  # 改为DEBUG级别
               "propagate": true
           }
       }
   }
   ```

   然后运行系统：

   ```bash
   python arxivtracker.py --debug --count 1
   ```

## 4. 系统恢复

### 4.1 从备份恢复

1. **恢复数据**

   ```bash
   # 解压备份文件
   # Windows PowerShell
   Expand-Archive -Path arxiv_data_backup_20260128.zip -DestinationPath .

   # macOS/Linux
   unzip arxiv_data_backup_20260128.zip -d .

   # 恢复配置文件
   # Windows PowerShell
   Expand-Archive -Path arxiv_config_backup_20260128.zip -DestinationPath .

   # macOS/Linux
   unzip arxiv_config_backup_20260128.zip -d .
   ```

2. **验证恢复**

   ```bash
   # 检查数据目录
   ls -la src/arxiv_tracker/data/

   # 检查配置文件
   cat config/api_config.json
   ```

### 4.2 重置系统状态

1. **完全重置**

   ```bash
   # 使用辅助脚本
   python scripts/reset_states.py

   # 或手动重置
   # 删除状态文件
   # Windows
   Remove-Item -Path src\arxiv_tracker\data\cache\state.json -Force

   # macOS/Linux
   rm src/arxiv_tracker/data/cache/state.json

   # 删除缓存文件
   # Windows
   Remove-Item -Path src\arxiv_tracker\data\cache\cache.json -Force

   # macOS/Linux
   rm src/arxiv_tracker/data/cache/cache.json
   ```

2. **部分重置**

   ```bash
   # 重置特定步骤
   python scripts/reset_states.py --step crawling
   python scripts/reset_states.py --step downloading
   python scripts/reset_states.py --step extracting
   python scripts/reset_states.py --step analyzing
   ```

### 4.3 重新安装系统

1. **备份重要数据**

   ```bash
   # 备份数据和配置
   # Windows PowerShell
   Compress-Archive -Path src\arxiv_tracker\data -DestinationPath arxiv_data_backup.zip
   Compress-Archive -Path config -DestinationPath arxiv_config_backup.zip

   # macOS/Linux
   zip -r arxiv_data_backup.zip src/arxiv_tracker/data/
   zip -r arxiv_config_backup.zip config/
   ```

2. **清理现有安装**

   ```bash
   # 删除虚拟环境
   # Windows
   Remove-Item -Path venv -Recurse -Force

   # macOS/Linux
   rm -rf venv

   # 删除临时文件
   # Windows
   Remove-Item -Path "*.pyc" -Recurse -Force
   Remove-Item -Path "__pycache__" -Recurse -Force

   # macOS/Linux
   find . -name "*.pyc" -delete
   find . -name "__pycache__" -type d -exec rm -rf {} \;
   ```

3. **重新安装**

   ```bash
   # 重新创建虚拟环境
   python -m venv venv

   # 激活虚拟环境
   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate

   # 安装依赖
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **恢复数据**

   ```bash
   # 恢复数据和配置
   # Windows PowerShell
   Expand-Archive -Path arxiv_data_backup.zip -DestinationPath .
   Expand-Archive -Path arxiv_config_backup.zip -DestinationPath .

   # macOS/Linux
   unzip arxiv_data_backup.zip -d .
   unzip arxiv_config_backup.zip -d .
   ```

## 5. 性能优化

### 5.1 爬取性能优化

1. **增加并发数**

   编辑 `config/system_config.json` 文件：

   ```json
   {
       "max_workers": 8  # 根据CPU核心数调整
   }
   ```

2. **使用缓存**

   系统会自动缓存爬取结果，避免重复请求。

3. **优化请求头**

   编辑 `src/arxiv_tracker/crawler.py` 文件，添加合适的User-Agent：

   ```python
   headers = {
       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
   }
   ```

### 5.2 下载性能优化

1. **使用多线程下载**

   系统已经使用 `ThreadPoolExecutor` 进行并行下载，可调整线程数。

2. **使用断点续传**

   系统支持断点续传，网络中断后重新运行会自动继续下载。

3. **优化下载参数**

   编辑 `src/arxiv_tracker/downloader.py` 文件，调整块大小：

   ```python
   CHUNK_SIZE = 1024 * 1024  # 1MB 块大小
   ```

### 5.3 分析性能优化

1. **减少API调用**

   - 只分析重要的论文
   - 复用分析结果
   - 调整分析参数

2. **批量处理**

   系统已经支持批量分析，可调整批处理大小。

3. **优化提示词**

   编辑 `src/arxiv_tracker/analyzer.py` 文件，优化LLM提示词，减少生成内容。

### 5.4 内存使用优化

1. **分批处理**

   ```bash
   # 分批处理论文
   python arxivtracker.py --count 10
   python arxivtracker.py --count 10 --offset 10
   ```

2. **释放内存**

   编辑代码，及时释放不再使用的对象：

   ```python
   # 使用后释放内存
   import gc
   gc.collect()
   ```

3. **使用生成器**

   对于大量数据处理，使用生成器代替列表：

   ```python
   def process_papers(papers):
       for paper in papers:
           # 处理单个论文
           yield processed_paper
   ```

## 6. 安全维护

### 6.1 API密钥安全

1. **保护API密钥**

   - 不要将API密钥硬编码在代码中
   - 不要将API密钥提交到版本控制系统
   - 使用环境变量或加密的配置文件

2. **定期轮换API密钥**

   - 每3-6个月轮换一次API密钥
   - 更新配置文件中的API密钥

3. **监控API使用**

   - 定期检查API调用记录
   - 发现异常使用及时处理

### 6.2 网络安全

1. **使用HTTPS**

   系统已经使用HTTPS进行所有网络通信。

2. **限制请求频率**

   - 避免频繁请求同一网站
   - 使用随机延迟

3. **使用代理**

   编辑 `config/system_config.json` 文件，添加代理：

   ```json
   {
       "proxy": "http://your-proxy-server:port"
   }
   ```

### 6.3 文件系统安全

1. **设置适当的文件权限**

   ```bash
   # 设置配置文件权限
   # Windows
   icacls config /inheritance:r /grant:r "%USERNAME%":(F)

   # macOS/Linux
   chmod 600 config/api_config.json
   ```

2. **扫描下载的文件**

   - 定期使用防病毒软件扫描PDF文件
   - 避免下载可疑文件

3. **备份重要文件**

   - 定期备份配置文件和数据
   - 存储备份到安全位置

## 7. 升级与迁移

### 7.1 版本升级

1. **备份数据**

   ```bash
   # 备份数据和配置
   # Windows PowerShell
   Compress-Archive -Path src\arxiv_tracker\data -DestinationPath arxiv_data_backup.zip
   Compress-Archive -Path config -DestinationPath arxiv_config_backup.zip

   # macOS/Linux
   zip -r arxiv_data_backup.zip src/arxiv_tracker/data/
   zip -r arxiv_config_backup.zip config/
   ```

2. **更新代码**

   ```bash
   # 使用Git更新
   git pull

   # 或下载新版本并解压
   ```

3. **更新依赖**

   ```bash
   # 激活虚拟环境
   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate

   # 更新依赖
   pip install --upgrade -r requirements.txt
   ```

4. **检查配置文件**

   - 检查新版本是否需要更新配置文件格式
   - 根据需要更新配置文件

5. **验证升级**

   ```bash
   # 运行系统
   python arxivtracker.py --count 1

   # 检查日志
   tail src/arxiv_tracker/data/logs/tracker.log
   ```

### 7.2 系统迁移

1. **准备新系统**

   - 安装Python 3.7+
   - 安装必要的依赖

2. **备份旧系统数据**

   ```bash
   # 备份所有数据
   # Windows PowerShell
   Compress-Archive -Path src\arxiv_tracker\data -DestinationPath arxiv_data_backup.zip
   Compress-Archive -Path config -DestinationPath arxiv_config_backup.zip
   Compress-Archive -Path requirements.txt -DestinationPath arxiv_requirements_backup.zip

   # macOS/Linux
   zip -r arxiv_migration_backup.zip src/arxiv_tracker/data/ config/ requirements.txt
   ```

3. **在新系统安装**

   ```bash
   # 复制备份文件到新系统
   # 解压备份
   # 安装依赖
   pip install -r requirements.txt
   ```

4. **验证迁移**

   ```bash
   # 运行系统
   python arxivtracker.py --count 1

   # 检查数据
   ls -la src/arxiv_tracker/data/
   ```

## 8. 总结

arXiv论文跟踪系统的维护工作包括：

- **日常监控**：定期检查系统运行状态
- **数据管理**：清理旧数据，备份重要数据
- **依赖管理**：更新依赖，修复冲突
- **故障排除**：解决常见错误和问题
- **性能优化**：提高系统运行效率
- **安全维护**：保护API密钥，确保系统安全
- **版本升级**：更新系统到最新版本

通过本文档的指导，系统管理员可以有效地维护和管理arXiv论文跟踪系统，确保其稳定运行，为用户提供高质量的论文跟踪和分析服务。

**维护建议频率：**
- 日常监控：每日
- 数据清理：每周
- 依赖更新：每月
- 完整备份：每月
- 安全检查：每季度
- 版本升级：每半年
