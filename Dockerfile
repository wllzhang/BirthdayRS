FROM python:3.11-slim

WORKDIR /app

# 安装 uv
RUN pip install --no-cache-dir uv

# 复制依赖文件
COPY pyproject.toml ./

# 安装项目依赖（会创建 .venv 虚拟环境）
RUN uv sync --no-dev

# 复制项目文件
COPY src/ ./src/
COPY templates/ ./templates/

# 设置环境变量
ENV PYTHONPATH=/app
ENV PATH="/app/.venv/bin:$PATH"

# 设置入口点（直接使用虚拟环境中的 Python）
ENTRYPOINT [".venv/bin/python", "-m", "src.main"] 