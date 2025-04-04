# 生日提醒系统 (Birthday Reminder System)

一个功能强大的生日提醒系统，支持农历和阳历生日提醒，并提供丰富的中国传统文化信息。


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
  - [ ] 支持多通知源
  - [ ] 预览邮件
  - [ ] github action支持
## 安装说明

1. 克隆项目到本地：
```bash
git clone [项目地址]
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

1. 直接运行主程序：
```bash
python src/main.py
```

2. 使用定时任务（推荐）：
```bash
# Linux/Mac (crontab -e)
0 9 * * * cd /path/to/python_birthday_reminder && python src/main.py

# Windows (任务计划程序)
# 创建每天早上9点运行的计划任务
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

运行覆盖率测试：
```bash
pytest --cov=src tests/
```

## 依赖项

- Python >= 3.8
- lunar_python >= 1.3.0
- aiosmtplib >= 2.0.0
- pyyaml >= 6.0.0
- jinja2 >= 3.0.0
- pytest >= 7.0.0
- pytest-asyncio >= 0.18.0
- pytest-cov >= 3.0.0

## 许可证

MIT License 