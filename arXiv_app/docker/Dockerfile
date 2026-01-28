# arXiv论文跟踪系统 Dockerfile

# 使用Python 3.9作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY . /app

# 创建虚拟环境
RUN python3 -m venv venv

# 激活虚拟环境并安装依赖
RUN /app/venv/bin/pip install --upgrade pip && \
    /app/venv/bin/pip install -r requirements.txt

# 创建数据目录
RUN mkdir -p /app/src/arxiv_tracker/data/papers && \
    mkdir -p /app/src/arxiv_tracker/data/reports && \
    mkdir -p /app/src/arxiv_tracker/data/cache && \
    mkdir -p /app/src/arxiv_tracker/data/logs

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 运行命令
CMD ["python3", "arxivtracker.py", "--count", "10"]
