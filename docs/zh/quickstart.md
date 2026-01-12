# 快速开始

## 基本使用

### 1. 创建配置文件

在项目根目录创建 `config.yml` 文件（参考 `config.example.yml`）：

```yaml
notification:
  smtp:
    host: smtp.gmail.com
    port: 587
    username: your_email@gmail.com
    password: your_password
    from_email: your_email@gmail.com
    default_receive_email: default@example.com
    default_template_file: birthday.html
    default_reminder_days: 7

  serverchan:
    default_sckey: your_sckey
    default_reminder_days: 7

  start_notification: "email,serverchan"

recipients:
  - name: "张三"
    solar_birthday: "1990-05-15"
    email: zhangsan@example.com
    reminder_days: 7
    template_file: birthday.html

  - name: "李四"
    lunar_birthday: "1988-03-20"
    email: lisi@example.com
    reminder_days: 7
```

### 2. 本地运行

```bash
# 运行生日提醒
python -m src.main run --config config.yml

# 预览邮件
python -m src.main preview --config config.yml
```

### 3. 使用 GitHub Actions 部署

1. Fork 本仓库
2. 在仓库设置中添加 Secret `BIRTHDAY_YAML`，内容为你的配置文件
3. 进入 Actions 页面运行"每日生日检查"

### 4. 使用 Docker 部署

```bash
# 使用 Docker 运行
docker run -v ${PWD}/config.yml:/app/config.yml ghcr.io/wllzhang/birthdayrs:latest run

# 使用 Docker 预览
docker run -v ${PWD}/config.yml:/app/config.yml -v ${PWD}/previews:/app/previews ghcr.io/wllzhang/birthdayrs:latest preview
```

## 命令

### 运行生日检查

```bash
python -m src.main run --config config.yml
```

### 预览邮件

```bash
python -m src.main preview --config config.yml
```

### 验证配置

```bash
python -m src.main validate --config config.yml
```

### 显示应用信息

```bash
python -m src.main info --config config.yml
```

## 测试

```bash
# 运行所有测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=src

# 运行特定测试
pytest tests/test_main.py
```
