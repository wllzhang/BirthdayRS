# 贡献指南

感谢你对 BirthdayRS 的贡献兴趣！

## 如何贡献

### 报告错误

1. 在 GitHub 上检查现有 issues
2. 创建新 issue，包含：
   - 清晰的标题和描述
   - 复现步骤
   - 预期行为
   - 实际行为
   - 环境信息（Python 版本、操作系统等）

### 建议功能

1. 检查现有的功能请求
2. 创建新 issue，包含：
   - 功能的清晰描述
   - 用例和收益
   - 可能的实现方式

### 提交 Pull Request

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 进行更改
4. 运行测试和代码检查
5. 提交更改 (`git commit -m '添加某个功能'`)
6. 推送到分支 (`git push origin feature/amazing-feature`)
7. 创建 Pull Request

## 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/wllzhang/BirthdayRS.git
cd BirthdayRS

# 安装依赖
uv sync

# 或使用 pip
pip install -r requirements.txt
```

## 运行测试

```bash
# 运行所有测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=src

# 生成 HTML 覆盖率报告
pytest --cov=src --cov-report=html
```

## 代码风格

本项目使用 [flake8](https://flake8.pycqa.org/) 进行代码风格检查。

```bash
# 运行 flake8
flake8 .

# 配置文件在 .flake8
# - 最大行长度：100
# - 忽略：E501, W503
```

## 文档

文档使用 [Sphinx](https://www.sphinx-doc.org/) 构建，并自动部署到 GitHub Pages。

```bash
# 本地构建文档
cd docs
sphinx-build -b html . _build

# 或使用 make（如果可用）
make html
```

## 项目结构

```
BirthdayRS/
├── src/
│   ├── core/                   # 核心业务逻辑
│   ├── notification/           # 通知发送器
│   └── main.py                # 应用入口
├── tests/                     # 测试套件
├── templates/                 # Jinja2 邮件模板
├── docs/                      # 文档
│   ├── zh/                    # 中文文档
│   └── ...
├── .github/workflows/         # GitHub Actions 工作流
└── config.example.yml         # 配置示例
```

## 编码指南

1. 遵循 PEP 8 代码风格指南
2. 为新功能编写测试
3. 更新 API 变更的文档
4. 使用有意义的提交信息
5. 保持 Pull Request 简洁聚焦

## 许可证

通过向 BirthdayRS 贡献，你同意你的贡献将根据 MIT 许可证进行许可。
