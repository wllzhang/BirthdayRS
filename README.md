# Birthday Reminder System

[![Docker Image](https://img.shields.io/badge/docker-ghcr.io/wllzhang/birthdayrs-blue)](https://github.com/wllzhang/BirthdayRS/pkgs/container/birthdayrs)
[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/wllzhang/BirthdayRS/actions/workflows/ci.yml/badge.svg)](https://github.com/wllzhang/BirthdayRS/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A powerful birthday reminder system supporting both lunar and solar calendars with rich Chinese cultural information.

**[中文文档](README.zh-CN.md) | [Documentation](https://wllzhang.github.io/BirthdayRS/)**

## Features

- **Dual Calendar Support** - Solar (Gregorian) & Lunar (Chinese) birthdays
- **Rich Date Information** - GanZhi, zodiac, festivals, solar terms, constellations
- **Multiple Notifications** - Email & [ServerChan](https://sct.ftqq.com/)
- **Flexible Deployment** - Local, Docker, GitHub Actions

## Quick Start

```bash
# Install
pip install -r requirements.txt

# Configure
cp config.example.yml config.yml
# Edit config.yml with your settings

# Run
python -m src.main run --config config.yml
```

## Documentation

Full documentation is available at [https://wllzhang.github.io/BirthdayRS/](https://wllzhang.github.io/BirthdayRS/)

## Docker

```bash
docker run -v ${PWD}/config.yml:/app/config.yml ghcr.io/wllzhang/birthdayrs:latest run
```

## License

MIT License
