"""
配置管理模块
"""
from dataclasses import dataclass
from typing import List, Optional, Dict
import yaml


@dataclass
class SMTPConfig:
    """SMTP服务器配置"""
    host: str
    port: int
    username: str
    password: str
    use_tls: bool = True


@dataclass
class DefaultConfig:
    """默认配置"""
    email: str
    reminder_days: int = 0
    template_file: str = "birthday.html"


@dataclass
class Recipient:
    """收件人信息"""
    name: str
    email: str
    solar_birthday: Optional[str] = None  # YYYY-MM-DD 格式
    lunar_birthday: Optional[str] = None  # YYYY-MM-DD 格式（阳历日期）
    reminder_days: int = 0  # 提前提醒天数
    template_file: str = "birthday.html"  # 模板文件名

    def __post_init__(self):
        """验证至少有一个生日日期"""
        if not self.solar_birthday and not self.lunar_birthday:
            raise ValueError(
                "At least one of solar_birthday or lunar_birthday must be provided")


@dataclass
class Config:
    """应用配置"""
    smtp: SMTPConfig
    recipients: List[Recipient]
    default: Optional[DefaultConfig] = None

    @classmethod
    def from_yaml(cls, config_path: str) -> 'Config':
        """从YAML文件加载配置"""
        with open(config_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        smtp_config = SMTPConfig(**data['smtp'])
        default_config = DefaultConfig(
            **data['default']) if 'default' in data else None

        recipients = []
        for r in data['recipients']:
            # 如果有默认配置，使用默认值
            if default_config:
                if 'email' not in r:
                    r['email'] = default_config.email
                if 'reminder_days' not in r:
                    r['reminder_days'] = default_config.reminder_days
                if 'template_file' not in r:
                    r['template_file'] = default_config.template_file
            else:
                # 设置默认值
                r.setdefault('reminder_days', 0)
                r.setdefault('template_file', 'birthday.html')

            recipients.append(Recipient(**r))

        return cls(
            smtp=smtp_config,
            recipients=recipients,
            default=default_config
        )
