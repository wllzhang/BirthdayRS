# 生日提醒系统 (Birthday Reminder System)
[![Docker Image](https://img.shields.io/badge/docker%20image-ghcr.io/wllzhang/birthdayrs-blue)](https://github.com/wllzhang/BirthdayRS/pkgs/container/birthdayrs)
[![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Code Style](https://img.shields.io/badge/code%20style-flake8-black.svg)](https://flake8.pycqa.org/)

[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
![GitHub last commit](https://img.shields.io/github/last-commit/wllzhang/BirthdayRS)
[![CI](https://github.com/wllzhang/BirthdayRS/actions/workflows/ci.yml/badge.svg)](https://github.com/wllzhang/BirthdayRS/actions/workflows/ci.yml)
[![Daily Check](https://github.com/wllzhang/BirthdayRS/actions/workflows/daily_check.yml/badge.svg)](https://github.com/wllzhang/BirthdayRS/actions/workflows/daily_check.yml)

![GitHub stars](https://img.shields.io/github/stars/wllzhang/BirthdayRS?style=social)
![GitHub forks](https://img.shields.io/github/forks/wllzhang/BirthdayRS?style=social)
![GitHub issues](https://img.shields.io/github/issues/wllzhang/BirthdayRS) 


一个功能强大的生日提醒系统，支持农历和阳历生日提醒，并提供丰富的中国传统文化信息。

[[中文文档](README.zh-CN.md)]  [[English Doc](README.md)] 
## 功能特点

- **双历支持**
  - [x] 支持阳历（公历）生日提醒
  - [x] 支持农历（阴历）生日提醒
  - [x] 智能处理闰月情况

- **丰富的日期信息**
  - [x] 显示干支纪年、纪月、纪日、纪时
  - [x] 显示生肖属相
  - [x] 显示农历节日
  - [x] 显示阳历节日
  - [x] 显示二十四节气
  - [x] 显示星期信息
  - [x] 显示星座信息

- **灵活的提醒设置**
  - [x] 可自定义提前提醒天数
  - [x] 支持多人生日提醒
  - [x] 支持邮件通知
  - [x] 支持邮件预览功能
  - [x] 预览邮件
  - [x] 添加default 
  - [x] github action支持
  - [X] Docker部署
  - [X] 支持多通知源 （email,[Server酱](https://sct.ftqq.com/)）


## 配置说明

在项目根目录创建 `config.yml` 文件（可以参考 `config.example.yml`） 

## 使用方法

### 1.本地运行
#### 运行
```bash
git clone https://github.com/wllzhang/BirthdayRS.git
cd BirthdayRS
# 安装依赖 
pip install -r requirements.txt
# 本地运行
python -m src.main run
# 预览
python -m src.main preview
# 验证配置
python -m src.main validate --config config.yml
# 查看信息
python -m src.main info --config config.yml
```
#### 查看帮助信息：
```bash
python -m src.main --help
python -m src.main preview --help
```
### 2.Github Action
   1. Frok仓库, setting配置vars:BIRTHDAY_YAML,值为config.yaml内容
   2. 点击Action,运行Action:`Daily Birthday Check`
   
### 3.Docker运行

#### 可用标签
- `latest`: 最新稳定版本
- `vX.Y.Z`: 特定版本（如 v1.0.0）
- `sha-XXXXXX`: 特定提交的构建

#### 运行示例

```bash
# 运行生日提醒
docker run -v ${PWD}/config.yml:/app/config.yml ghcr.io/wllzhang/birthdayrs:latest run
docker run -v ${PWD}/config.yml:/app/config.yml -v ${PWD}/previews:/app/previews  ghcr.io/wllzhang/birthdayrs:latest preview
``` 

## 许可证

MIT License 

<details>

## 日志

系统运行日志保存在 `birthday_reminder.log` 文件中，包含以下信息：
- 配置加载状态
- 生日检查结果
- 邮件发送状态
- 错误信息（如果有）
 

## 邮件模板

系统使用 Jinja2 模板引擎渲染邮件内容，支持自定义邮件模板。默认模板位于 `templates/birthday.html`，包含以下信息：

- 基本生日信息
- 农历日期信息
- 干支纪年月日时
- 生肖和星座
- 节日和节气信息
- 星期信息

## 测试

运行测试用例：
```bash
pytest
```

## CI/CD 流程

本项目使用 GitHub Actions 实现完整的 CI/CD 流程：

### 持续集成 (CI)

每次推送代码或创建 Pull Request 时，会自动运行以下检查：

1. **代码测试**
   - 运行单元测试
   - 生成测试覆盖率报告
   - 测试结果作为工件保存

2. **代码质量检查**
   - 使用 flake8 进行代码风格检查
   - 确保代码符合 PEP 8 规范

3. **Docker 镜像构建**
   - 自动构建 Docker 镜像
   - 推送到 GitHub Container Registry

### 持续部署 (CD)

1. **每日检查**
   - 每天自动运行生日检查
   - 发送提醒邮件
   - 支持开发环境和生产环境

2. **Docker 部署**
   - 支持通过 Docker 快速部署
   - 提供最新版本的镜像

### 自动化流程

- **README 自动更新**
  - 自动更新文档中的仓库链接
  - 保持文档与代码同步

 </details>