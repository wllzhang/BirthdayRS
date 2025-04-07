FROM python:3.9-slim

WORKDIR /app

# 复制项目文件
COPY requirements.txt .
COPY src/ ./src/
COPY templates/ ./templates/


# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 设置环境变量
ENV PYTHONPATH=/app

# 设置入口点
ENTRYPOINT ["python", "src/main.py"] 