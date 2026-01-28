# arXiv论文跟踪系统安装部署文档

## 1. 系统要求

### 1.1 硬件要求

| 硬件 | 最低要求 | 推荐要求 |
|------|----------|----------|
| CPU | 2核 | 4核及以上 |
| 内存 | 4GB | 8GB及以上 |
| 磁盘空间 | 50GB | 100GB及以上 |
| 网络 | 稳定的互联网连接 | 高速互联网连接 |

### 1.2 软件要求

| 软件 | 版本 | 用途 |
|------|------|------|
| Python | 3.7+ | 运行环境 |
| pip | 20.0+ | 包管理工具 |
| Git | 2.0+ | 版本控制（可选） |
| Docker | 20.0+ | 容器化部署（可选） |

### 1.3 操作系统支持

- **Windows**：Windows 10及以上
- **macOS**：macOS 10.15及以上
- **Linux**：Ubuntu 18.04+, CentOS 7+ 等主流Linux发行版

## 2. 安装方法

### 2.1 方法一：使用自动安装脚本

这是最简单的安装方法，适用于大多数用户。

1. **下载项目**

   ```bash
   # 使用Git克隆（推荐）
   git clone https://github.com/yourusername/arxiv-tracker.git
   cd arxiv-tracker

   # 或直接下载ZIP文件并解压
   ```

2. **运行安装脚本**

   ```bash
   # Windows
   python scripts/setup_venv.py

   # macOS/Linux
   python3 scripts/setup_venv.py
   ```

   该脚本会自动：
   - 创建虚拟环境
   - 升级pip
   - 安装所有依赖包

### 2.2 方法二：手动安装

1. **下载项目**

   ```bash
   git clone https://github.com/yourusername/arxiv-tracker.git
   cd arxiv-tracker
   ```

2. **创建虚拟环境**

   ```bash
   # Windows
   python -m venv venv

   # macOS/Linux
   python3 -m venv venv
   ```

3. **激活虚拟环境**

   ```bash
   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

4. **升级pip**

   ```bash
   pip install --upgrade pip
   ```

5. **安装依赖**

   ```bash
   pip install -r requirements.txt
   ```

### 2.3 方法三：使用pip安装（作为Python包）

```bash
# 从源码安装
pip install -e .

# 或从PyPI安装（未来支持）
pip install arxiv-tracker
```

## 3. 配置步骤

### 3.1 基本配置

1. **配置文件结构**

   ```
   config/
   ├── system_config.json     # 系统配置
   ├── api_config.json        # API配置
   ├── categories.json        # 论文类别
   └── logging_config.json    # 日志配置
   ```

2. **系统配置**

   编辑 `config/system_config.json` 文件，根据需要修改以下配置：

   ```json
   {
       "data_dir": "src/arxiv_tracker/data",
       "pdf_storage": "src/arxiv_tracker/data/papers",
       "report_storage": "src/arxiv_tracker/data/reports",
       "cache_storage": "src/arxiv_tracker/data/cache",
       "log_dir": "src/arxiv_tracker/data/logs",
       "categories": ["cs.AI", "cs.LG", "cs.CL", "cs.CV", "cs.NE"],
       "max_workers": 4,
       "timeout": 30,
       "max_retries": 3,
       "cache_ttl": 86400,
       "default_paper_count": 10
   }
   ```

   关键配置项说明：
   - `categories`：要跟踪的论文类别列表
   - `max_workers`：并发工作线程数
   - `default_paper_count`：默认处理的论文数量

### 3.2 API配置

1. **获取API密钥**

   系统使用阿里云DashScope API进行论文分析，需要获取API密钥：

   1. 访问 [阿里云DashScope官网](https://dashscope.aliyun.com/)
   2. 注册并登录账号
   3. 进入控制台，创建API密钥
   4. 记录生成的API密钥

2. **配置API密钥**

   复制 `config/api_config.json` 文件并编辑：

   ```bash
   # 复制配置文件
   cp config/api_config.json config/api_config.json
   ```

   编辑 `config/api_config.json` 文件：

   ```json
   {
       "dashscope_api_key": "YOUR_API_KEY_HERE",
       "api_endpoint": "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
       "max_retries": 3,
       "timeout": 60,
       "model": "qwen-plus",
       "temperature": 0.3,
       "top_p": 0.8
   }
   ```

   将 `YOUR_API_KEY_HERE` 替换为你的实际API密钥。

### 3.3 类别配置

编辑 `config/categories.json` 文件，添加或修改论文类别：

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

### 3.4 日志配置

编辑 `config/logging_config.json` 文件，调整日志配置：

```json
{
    "version": 1,
    "disable_existing_loggers": false,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "INFO",
            "formatter": "standard",
            "filename": "src/arxiv_tracker/data/logs/tracker.log",
            "encoding": "utf-8"
        }
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": true
        }
    }
}
```

## 4. 部署方法

### 4.1 本地部署

1. **运行系统**

   ```bash
   # 激活虚拟环境（如果尚未激活）
   # Windows: venv\Scripts\activate
   # macOS/Linux: source venv/bin/activate

   # 运行主程序
   python arxivtracker.py --count 10
   ```

2. **验证安装**

   系统运行后，检查以下目录是否生成：
   - `src/arxiv_tracker/data/papers/` - PDF文件存储目录
   - `src/arxiv_tracker/data/reports/` - 报告存储目录
   - `src/arxiv_tracker/data/logs/` - 日志存储目录

   检查日志文件 `src/arxiv_tracker/data/logs/tracker.log` 确认系统运行状态。

### 4.2 Docker部署

1. **构建Docker镜像**

   ```bash
   # 在项目根目录执行
   docker build -t arxiv-tracker .
   ```

2. **运行Docker容器**

   ```bash
   # 运行容器
   docker run --name arxiv-tracker \
       -v "$(pwd)/src/arxiv_tracker/data:/app/src/arxiv_tracker/data" \
       -v "$(pwd)/config:/app/config" \
       arxiv-tracker
   ```

   **参数说明：**
   - `-v "$(pwd)/src/arxiv_tracker/data:/app/src/arxiv_tracker/data"` - 挂载数据目录
   - `-v "$(pwd)/config:/app/config"` - 挂载配置目录

3. **使用Docker Compose**

   创建 `docker-compose.yml` 文件：

   ```yaml
   version: '3'
   services:
     arxiv-tracker:
       build: .
       volumes:
         - ./src/arxiv_tracker/data:/app/src/arxiv_tracker/data
         - ./config:/app/config
       environment:
         - PYTHONUNBUFFERED=1
       restart: unless-stopped
   ```

   运行：

   ```bash
   docker-compose up -d
   ```

### 4.3 定时任务部署

1. **Windows任务计划程序**

   1. 打开「任务计划程序」
   2. 创建新任务
   3. 设置触发器（如每天凌晨2点）
   4. 设置操作：
      - 程序/脚本：`python.exe`
      - 添加参数：`arxivtracker.py --count 20`
      - 起始于：项目根目录

2. **Linux/macOS Crontab**

   ```bash
   # 编辑crontab
   crontab -e

   # 添加定时任务（每天凌晨2点运行）
   0 2 * * * cd /path/to/arxiv-tracker && venv/bin/python arxivtracker.py --count 20
   ```

3. **使用Python定时库**

   创建 `scheduled_task.py` 文件：

   ```python
   import schedule
   import time
   import subprocess
   import os

   def run_tracker():
       print("开始运行arXiv论文跟踪系统...")
       # 激活虚拟环境并运行
       if os.name == 'nt':
           # Windows
           cmd = ['venv\\Scripts\\python.exe', 'arxivtracker.py', '--count', '15']
       else:
           # macOS/Linux
           cmd = ['venv/bin/python', 'arxivtracker.py', '--count', '15']
       
       result = subprocess.run(cmd, capture_output=True, text=True)
       print(f"运行结果: {result.returncode}")
       print(f"输出: {result.stdout}")
       if result.stderr:
           print(f"错误: {result.stderr}")

   # 每天凌晨2点运行
   schedule.every().day.at("02:00").do(run_tracker)

   print("定时任务已启动，每天凌晨2点运行")
   while True:
       schedule.run_pending()
       time.sleep(60)
   ```

   运行：

   ```bash
   python scheduled_task.py
   ```

## 5. 环境变量

系统支持以下环境变量：

| 环境变量 | 描述 | 默认值 |
|---------|------|--------|
| `PYTHONUNBUFFERED` | 禁用Python输出缓冲 | 未设置 |
| `DASHSCOPE_API_KEY` | DashScope API密钥 | 从配置文件读取 |
| `ARXIV_TRACKER_CONFIG` | 自定义配置文件路径 | 未设置 |
| `ARXIV_TRACKER_DATA_DIR` | 数据存储目录 | `src/arxiv_tracker/data` |
| `ARXIV_TRACKER_LOG_LEVEL` | 日志级别 | `INFO` |

**使用示例：**

```bash
# 设置API密钥
export DASHSCOPE_API_KEY="your_api_key_here"

# 设置日志级别
export ARXIV_TRACKER_LOG_LEVEL="DEBUG"

# 运行系统
python arxivtracker.py
```

## 6. 依赖管理

### 6.1 依赖包列表

| 依赖包 | 版本 | 用途 |
|--------|------|------|
| requests | >=2.31.0 | 网络请求 |
| beautifulsoup4 | >=4.12.2 | HTML解析 |
| tqdm | >=4.66.1 | 进度显示 |
| psutil | >=5.9.6 | 系统资源监控 |
| dashscope | >=1.17.0 | LLM API |
| PyPDF2 | >=3.0.1 | PDF文件处理 |
| markdown | >=3.4.4 | Markdown处理 |

### 6.2 安装额外依赖

**开发依赖：**

```bash
pip install -e "[dev]"
```

**测试依赖：**

```bash
pip install pytest pytest-cov
```

### 6.3 依赖包更新

```bash
# 更新所有依赖
pip install --upgrade -r requirements.txt

# 更新单个依赖
pip install --upgrade requests
```

## 7. 多环境部署

### 7.1 开发环境

```bash
# 克隆代码
git clone https://github.com/yourusername/arxiv-tracker.git
cd arxiv-tracker

# 创建开发环境
python -m venv venv_dev
venv_dev\Scripts\activate  # Windows
# source venv_dev/bin/activate  # macOS/Linux

# 安装开发依赖
pip install -e "[dev]"

# 运行测试
pytest
```

### 7.2 测试环境

```bash
# 创建测试环境
python -m venv venv_test
venv_test\Scripts\activate  # Windows
# source venv_test/bin/activate  # macOS/Linux

# 安装测试依赖
pip install -e .
pip install pytest pytest-cov

# 运行完整测试套件
pytest --cov=src/arxiv_tracker
```

### 7.3 生产环境

```bash
# 创建生产环境
python -m venv venv_prod
venv_prod\Scripts\activate  # Windows
# source venv_prod/bin/activate  # macOS/Linux

# 安装生产依赖
pip install -e .

# 运行系统
python arxivtracker.py --count 50
```

## 8. 故障排除

### 8.1 常见安装问题

| 问题 | 可能原因 | 解决方案 |
|------|---------|----------|
| 虚拟环境创建失败 | Python版本不兼容 | 确保使用Python 3.7+ |
| 依赖安装失败 | pip版本过低 | 升级pip：`pip install --upgrade pip` |
| 网络连接失败 | 网络不稳定或代理设置 | 检查网络连接，配置代理 |
| API调用失败 | API密钥无效 | 检查API密钥是否正确 |
| PDF提取失败 | PyPDF2版本问题 | 确保使用PyPDF2 3.0.1+ |
| 权限错误 | 文件权限不足 | 以管理员身份运行命令 |

### 8.2 调试步骤

1. **检查Python版本**

   ```bash
   python --version
   ```

2. **检查依赖安装状态**

   ```bash
   pip list
   ```

3. **检查配置文件**

   ```bash
   # 检查API配置
   cat config/api_config.json

   # 检查系统配置
   cat config/system_config.json
   ```

4. **运行调试模式**

   ```bash
   python arxivtracker.py --debug --count 1
   ```

5. **检查日志文件**

   ```bash
   tail -f src/arxiv_tracker/data/logs/tracker.log
   ```

6. **测试网络连接**

   ```bash
   # 测试arXiv网站连接
   curl -I https://arxiv.org

   # 测试API连接
   curl -I https://dashscope.aliyuncs.com
   ```

### 8.3 性能问题排查

1. **检查系统资源**

   ```bash
   # Windows
   tasklist | findstr python

   # macOS/Linux
   top -p $(pgrep -f python)
   ```

2. **优化配置**

   - 减少 `max_workers` 值
   - 减少 `default_paper_count` 值
   - 增加系统内存

3. **磁盘空间问题**

   ```bash
   # 检查磁盘空间
   # Windows
   dir

   # macOS/Linux
   df -h
   ```

4. **网络速度问题**

   ```bash
   # 测试网络速度
   # Windows
   ping -n 10 arxiv.org

   # macOS/Linux
   ping -c 10 arxiv.org
   ```

## 9. 升级与迁移

### 9.1 版本升级

1. **备份数据**

   ```bash
   # 备份数据目录
   cp -r src/arxiv_tracker/data src/arxiv_tracker/data_backup

   # 备份配置文件
   cp -r config config_backup
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
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # macOS/Linux

   # 更新依赖
   pip install --upgrade -r requirements.txt
   ```

4. **检查配置文件**

   检查新版本是否需要更新配置文件格式，根据需要更新配置。

5. **验证升级**

   ```bash
   # 运行系统
   python arxivtracker.py --count 1

   # 检查日志
   tail src/arxiv_tracker/data/logs/tracker.log
   ```

### 9.2 数据迁移

1. **导出数据**

   ```bash
   # 打包数据目录
   zip -r arxiv_data_backup.zip src/arxiv_tracker/data
   ```

2. **导入数据**

   ```bash
   # 解压数据
   unzip arxiv_data_backup.zip -d /path/to/new/install
   ```

3. **验证数据**

   ```bash
   # 检查数据完整性
   ls -la src/arxiv_tracker/data/papers/
   ```

## 10. 安全注意事项

### 10.1 API密钥安全

- **不要**将API密钥硬编码在代码中
- **不要**将API密钥提交到版本控制系统
- **不要**在日志中记录API密钥
- **定期**轮换API密钥
- **使用**环境变量或加密的配置文件存储API密钥

### 10.2 网络安全

- **使用**HTTPS协议进行所有网络通信
- **设置**合理的网络超时和重试机制
- **限制**并发请求数，避免被服务器封禁
- **遵循**robots.txt规则，合理爬取网站

### 10.3 文件系统安全

- **设置**适当的文件和目录权限
- **定期**清理旧数据，避免磁盘空间耗尽
- **备份**重要数据，防止数据丢失
- **扫描**下载的文件，防止恶意软件

### 10.4 系统安全

- **定期**更新依赖包，修复安全漏洞
- **使用**防火墙限制网络访问
- **监控**系统资源使用情况，防止资源耗尽
- **记录**系统活动日志，便于安全审计

## 11. 监控与维护

### 11.1 系统监控

1. **日志监控**

   ```bash
   # 实时查看日志
   tail -f src/arxiv_tracker/data/logs/tracker.log

   # 查看错误日志
   grep -i error src/arxiv_tracker/data/logs/tracker.log
   ```

2. **资源监控**

   ```bash
   # 使用系统工具监控
   # Windows: 任务管理器
   # macOS: 活动监视器
   # Linux: top, htop
   ```

3. **数据监控**

   ```bash
   # 检查数据目录大小
   du -sh src/arxiv_tracker/data/

   # 检查PDF文件数量
   find src/arxiv_tracker/data/papers -name "*.pdf" | wc -l
   ```

### 11.2 定期维护

1. **清理旧数据**

   ```bash
   # 删除30天前的PDF文件
   find src/arxiv_tracker/data/papers -name "*.pdf" -mtime +30 -delete

   # 删除30天前的日志文件
   find src/arxiv_tracker/data/logs -name "*.log" -mtime +30 -delete
   ```

2. **备份数据**

   ```bash
   # 备份数据目录
   tar -czf arxiv_data_$(date +%Y%m%d).tar.gz src/arxiv_tracker/data/

   # 备份配置文件
   tar -czf arxiv_config_$(date +%Y%m%d).tar.gz config/
   ```

3. **更新依赖**

   ```bash
   # 定期更新依赖包
   pip install --upgrade -r requirements.txt
   ```

4. **检查系统状态**

   ```bash
   # 运行状态检查
   python scripts/reset_states.py

   # 检查API配置
   python -c "import json; print(json.load(open('config/api_config.json'))['dashscope_api_key'])
   ```

## 12. 总结

arXiv论文跟踪系统的安装部署过程包括以下主要步骤：

1. **环境准备**：确保系统满足硬件和软件要求
2. **安装依赖**：使用自动脚本或手动安装依赖包
3. **配置系统**：设置API密钥和系统参数
4. **部署运行**：选择本地、Docker或定时任务部署方式
5. **监控维护**：定期监控系统状态，进行必要的维护

通过本文档的指导，您应该能够成功安装和部署arXiv论文跟踪系统，开始自动跟踪和分析arXiv论文。如果在安装过程中遇到问题，请参考故障排除部分或联系技术支持。
