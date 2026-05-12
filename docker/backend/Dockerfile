# ============================================
# FastapiAdmin Backend Dockerfile
# ============================================
# 多阶段构建：第一阶段安装依赖，第二阶段运行应用
# 优化：移除 build-essential，多数包已有预编译 wheel
# ============================================

# 第一阶段：安装依赖
FROM python:3.10-slim AS builder

ENV TZ=Asia/Shanghai \
    PIP_NO_CACHE_DIR=1

WORKDIR /build

# 复制依赖文件（利用 Docker 缓存层）
COPY ./backend/requirements.txt .

# 安装 Python 依赖（全部使用预编译 wheel，无需 gcc/build-essential）
RUN pip install --no-cache-dir --only-binary :all: \
    -r requirements.txt --target=/home/deps \
    -i https://pypi.tuna.tsinghua.edu.cn/simple 2>/dev/null \
    || pip install --no-cache-dir \
    -r requirements.txt --target=/home/deps \
    -i https://pypi.tuna.tsinghua.edu.cn/simple

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

WORKDIR /home

# 从构建阶段复制依赖
COPY --from=builder /home/deps /home/deps
ENV PYTHONPATH=/home/deps:$PYTHONPATH

# 复制应用代码（运行时由 volume 覆盖，此处仅作为镜像兜底）
COPY ./backend/ .

EXPOSE 8001

# 容器健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8001/common/health')" || exit 1

CMD ["python", "main.py", "run", "--env=prod"]
