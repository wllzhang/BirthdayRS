FROM python:3.11-slim

WORKDIR /app

# 安装 uv
RUN pip install --no-cache-dir uv

# 复制依赖文件
COPY pyproject.toml ./
COPY requirements.txt ./

# 安装项目依赖
RUN uv sync --no-dev

# 复制项目文件
COPY src/ ./src/
COPY templates/ ./templates/

# 设置环境变量
ENV PYTHONPATH=/app

# 设置入口点
ENTRYPOINT ["uv", "run", "python", "-m", "src.main"] 