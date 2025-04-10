# 生日提醒系统 (Birthday Reminder System)

一个功能强大的生日提醒系统，支持农历和阳历生日提醒，并提供丰富的中国传统文化信息。

## CI/CD 状态

[![CI](https://github.com/wllzhang/BirthdayRS/actions/workflows/ci.yml/badge.svg)](https://github.com/wllzhang/BirthdayRS/actions/workflows/ci.yml)
[![Docker](https://github.com/wllzhang/BirthdayRS/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/wllzhang/BirthdayRS/actions/workflows/docker-publish.yml)
[![Daily Check](https://github.com/wllzhang/BirthdayRS/actions/workflows/daily_check.yml/badge.svg)](https://github.com/wllzhang/BirthdayRS/actions/workflows/daily_check.yml)

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
- **TODO**
  - [ ] 支持多通知源

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

## 安装说明

1. 克隆项目到本地：
```bash
git clone https://github.com/wllzhang/BirthdayRS.git
cd python_birthday_reminder
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 配置说明

在项目根目录创建 `config.yml` 文件（可以参考 `config.example.yml`），配置格式如下：

```yaml
smtp:
  host: smtp.example.com
  port: 587
  username: your_email@example.com
  password: your_password
  use_tls: true

recipients:
  - name: 张三
    email: zhangsan@example.com
    solar_birthday: 1990-01-01  # 阳历生日
    reminder_days: 3  # 提前3天提醒
  - name: 李四
    email: lisi@example.com
    lunar_birthday: 1995-02-15  # 农历生日
    reminder_days: 7  # 提前7天提醒
```

## 使用方法

1. 本地运行
   1. 运行生日提醒：
    ```bash
    python -m src.main run
    ```
   2. 预览邮件内容：
    ```bash
    # 预览默认测试用户的邮件
    python -m src.main preview

    # 预览指定收件人的邮件
    python -m src.main preview --recipient "张三"

    # 预览指定日期的邮件
    python -m src.main preview --recipient "张三" --date "2024-01-01"
    ```
    3. 查看帮助信息：
    ```bash
    python -m src.main --help
    python -m src.main preview --help
    ```
2. Github Action
   1. Frok仓库, setting配置vars:BIRTHDAY_YAML,值为config.yaml内容
   2. 点击Action,运行Action:`Daily Birthday Check`
   
3. Docker
```bash
# 运行生日提醒
docker run -v ${PWD}/config.yml:/app/config.yml ghcr.io/wllzhang/birthdayrs run
# 预览邮件
docker run -v ${PWD}/config.yml:/app/config.yml `
           -v ${PWD}/previews:/app/previews `
           ghcr.io/wllzhang/birthdayrs  preview -r "测试用户" -d "2024-01-01"
```

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

## 日志

系统运行日志保存在 `birthday_reminder.log` 文件中，包含以下信息：
- 配置加载状态
- 生日检查结果
- 邮件发送状态
- 错误信息（如果有）
 
## 许可证

MIT License 