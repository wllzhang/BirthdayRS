# 安装

## 系统要求

- Python 3.8 或更高版本
- pip 或 uv 包管理器

## 从源码安装

```bash
# 克隆仓库
git clone https://github.com/wllzhang/BirthdayRS.git
cd BirthdayRS

# 使用 uv 安装依赖（推荐）
uv sync

# 或使用 pip 安装
pip install -r requirements.txt
```

## 开发环境安装

```bash
# 以开发模式安装
pip install -e .

# 安装开发依赖
pip install -r requirements.txt
```

## Docker 安装

```bash
# 拉取最新镜像
docker pull ghcr.io/wllzhang/birthdayrs:latest

# 或从源码构建
docker build -t birthdayrs .
```

## 验证安装

```bash
# 检查包是否已安装
python -m src.main --help

# 验证配置
python -m src.main validate --config config.yml

# 显示应用信息
python -m src.main info --config config.yml
```
