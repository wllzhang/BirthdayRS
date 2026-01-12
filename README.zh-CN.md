# 生日提醒系统 (Birthday Reminder System)

[![Docker Image](https://img.shields.io/badge/docker-ghcr.io/wllzhang/birthdayrs-blue)](https://github.com/wllzhang/BirthdayRS/pkgs/container/birthdayrs)
[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/wllzhang/BirthdayRS/actions/workflows/ci.yml/badge.svg)](https://github.com/wllzhang/BirthdayRS/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

一个功能强大的生日提醒系统，支持农历和阳历生日，提供丰富的中国传统文化信息。

**[English Doc](README.md) | [文档](https://wllzhang.github.io/BirthdayRS/)**

## 功能特点

- **双历支持** - 阳历（公历）& 农历（阴历）生日
- **丰富的日期信息** - 干支、生肖、节日、节气、星座
- **多种通知方式** - 邮件 & [Server酱](https://sct.ftqq.com/)
- **灵活部署** - 本地、Docker、GitHub Actions

## 快速开始

```bash
# 安装
pip install -r requirements.txt

# 配置
cp config.example.yml config.yml
# 编辑 config.yml 填入你的配置

# 运行
python -m src.main run --config config.yml
```

## 文档

完整文档请访问 [https://wllzhang.github.io/BirthdayRS/](https://wllzhang.github.io/BirthdayRS/)

## Docker

```bash
docker run -v ${PWD}/config.yml:/app/config.yml ghcr.io/wllzhang/birthdayrs:latest run
```

## 许可证

MIT License
