# ============================================
# FastapiAdmin Backend Dockerfile
# ============================================
# 多阶段构建：第一阶段安装依赖，第二阶段运行应用
# ============================================

# 第一阶段：构建依赖
FROM python:3.10-slim AS builder

# 设置时区
ENV TZ=Asia/Shanghai

# 设置容器内工作目录
WORKDIR /build

# 安装编译依赖（部分包需要 build-essential）
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件（利用 Docker 缓存层）
COPY ./backend/requirements.txt .

# 安装 Python 依赖到指定目录
RUN pip install --no-cache-dir -r requirements.txt \
    --target=/home/deps

# 第二阶段：运行环境
FROM python:3.10-slim

LABEL maintainer="948080782@qq.com"
LABEL description="FastapiAdmin Backend Service"
LABEL version="1.0"

# Python 优化环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    TZ=Asia/Shanghai

# 创建非 root 用户
RUN groupadd -r fastapiadmin && \
    useradd -r -g fastapiadmin -u 1001 -m -s /sbin/nologin fastapiadmin

# 创建日志目录
RUN mkdir -p /home/logs && \
    chmod 755 /home/logs

# 设置工作目录
WORKDIR /home

# 从构建阶段复制依赖
COPY --from=builder /home/deps /home/deps

# 设置 PYTHONPATH
ENV PYTHONPATH=/home/deps:$PYTHONPATH

# 复制应用代码
COPY ./backend/ .

# 更改文件所有权
RUN chown -R fastapiadmin:fastapiadmin /home

# 切换到非 root 用户
USER fastapiadmin

# 暴露端口
EXPOSE 8001

# 容器健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8001/api/v1/health')" || exit 1

# 运行应用
CMD ["python", "main.py", "run", "--env=prod"]
