# 第一阶段：构建依赖
FROM python:3.10-slim as builder

# 设置时区
ENV TZ Asia/Shanghai

# 设置容器内工作目录
WORKDIR /build

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY ./backend/requirements.txt .

# 安装依赖到指定目录
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple \
    --target=/home/deps

# 第二阶段：运行环境
FROM python:3.10-slim

# 使用 LABEL 替代 MAINTAINER
LABEL maintainer="948080782@qq.com"

# 设置时区
ENV TZ Asia/Shanghai

# 创建非root用户
RUN useradd -m -u 1001 fastapiadmin

# 设置容器内工作目录
WORKDIR /home

# 从构建阶段复制依赖
COPY --from=builder /home/deps /home/deps

# 设置PYTHONPATH
ENV PYTHONPATH=/home/deps:$PYTHONPATH

# 复制应用代码
COPY ./backend/ .

# 更改文件权限
RUN chown -R fastapiadmin:fastapiadmin /home

# 切换到非root用户
USER fastapiadmin

# 运行应用
CMD ["python", "main.py", "run", "--env=prod"]

# 暴露端口
EXPOSE 8001