# 配置说明

## 配置文件结构

`config.yml` 是 BirthdayRS 的主配置文件，包含通知和收件人的设置。

## 通知设置

### SMTP 配置

```yaml
notification:
  smtp:
    host: smtp.gmail.com              # SMTP 服务器地址
    port: 587                          # SMTP 服务器端口
    username: your_email@gmail.com     # SMTP 用户名
    password: your_password            # SMTP 密码
    from_email: your_email@gmail.com   # 发件人邮箱
    default_receive_email: default@example.com  # 默认收件人
    default_template_file: birthday.html         # 默认邮件模板
    default_reminder_days: 7           # 默认提前提醒天数
```

### ServerChan 配置

```yaml
notification:
  serverchan:
    default_sckey: your_sckey          # ServerChan API 密钥
    default_reminder_days: 7           # 默认提前提醒天数
```

### 通知类型

```yaml
notification:
  start_notification: "email,serverchan"  # 逗号分隔的列表
```

可用值：
- `email` - 发送邮件通知
- `serverchan` - 发送 ServerChan 通知
- `email,serverchan` - 同时发送两种通知

## 收件人配置

### 收件人字段

每个收件人可以包含以下字段：

```yaml
recipients:
  - name: "收件人姓名"                  # 必填：收件人姓名
    solar_birthday: "1990-05-15"       # 可选：阳历生日（YYYY-MM-DD）
    lunar_birthday: "1988-03-20"       # 可选：阴历生日（YYYY-MM-DD）
    email: recipient@example.com       # 可选：邮箱地址
    reminder_days: 7                   # 可选：提前提醒天数
    template_file: birthday.html       # 可选：邮件模板文件
```

### 多个收件人

```yaml
recipients:
  - name: "张三"
    solar_birthday: "1990-05-15"
    email: zhangsan@example.com

  - name: "李四"
    lunar_birthday: "1988-03-20"
    email: lisi@example.com
    reminder_days: 14

  - name: "王五"
    solar_birthday: "1985-12-25"
    email: wangwu@example.com
    template_file: custom.html
```

## 默认值

如果收件人未明确设置，将继承默认值：

- `email` - 继承自 `notification.smtp.default_receive_email`
- `reminder_days` - 继承自 SMTP 或 ServerChan 的默认值
- `template_file` - 继承自 `notification.smtp.default_template_file`

## 生日格式

### 阳历生日

```yaml
solar_birthday: "1990-05-15"  # YYYY-MM-DD 格式
```

### 阴历生日

```yaml
lunar_birthday: "1988-03-20"  # 存储为对应的阳历日期
```

**注意**：配置中的阴历生日存储为其对应的阳历（公历）日期。系统使用 `lunar_python` 库处理转换。

## 邮件模板

邮件模板使用 Jinja2，位于 `templates/` 目录。

### 模板变量

模板中可用的变量：
- `recipient` - 收件人信息
- `extra_info` - 丰富的日期信息，包括：
  - `gan_zhi` - 年、月、日、时的干支
  - `zodiac` - 生肖
  - `lunar_festivals` - 阴历节日
  - `solar_festivals` - 阳历节日
  - `solar_terms` - 节气
  - `week` - 星期信息
  - `constellation` - 星座信息

### 自定义模板

```yaml
recipients:
  - name: "张三"
    solar_birthday: "1990-05-15"
    template_file: custom.html
```

## 配置示例

参考项目根目录的 `config.example.yml` 查看完整示例配置。
