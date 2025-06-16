"""
配置管理模块
"""

from dataclasses import dataclass
from typing import List, Optional
import yaml


@dataclass
class SMTPConfig:
    """SMTP服务器配置"""

    host: str
    port: int
    username: str
    password: str
    use_tls: bool = True
    default_receive_email: Optional[str] = None
    default_template_file: str = "birthday.html"
    default_reminder_days: int = 0


@dataclass
class ServerChanConfig:
    default_sckey: Optional[str] = None
    default_reminder_days: int = 0


@dataclass
class Recipient:
    """收件人信息"""

    name: str
    email: Optional[str] = None
    solar_birthday: Optional[str] = None  # YYYY-MM-DD 格式
    lunar_birthday: Optional[str] = None  # YYYY-MM-DD 格式（阳历日期）
    reminder_days: Optional[int] = None
    template_file: Optional[str] = None

    def __post_init__(self):
        """验证至少有一个生日日期"""
        if not self.solar_birthday and not self.lunar_birthday:
            raise ValueError(
                "At least one of solar_birthday or lunar_birthday must be provided"
            )


@dataclass
class Config:
    """应用配置"""

    smtp_config: Optional[SMTPConfig]
    serverchan_config: Optional[ServerChanConfig]
    recipients: List[Recipient]
    notification_types: List[str]

    @classmethod
    def from_yaml(cls, config_path: str) -> "Config":
        """从YAML文件加载配置"""
        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        notification = data.get("notification", {})
        notification_types = [
            t.strip() for t in notification.get("type", "email").split(",") if t.strip()
        ]
        smtp_config = (
            SMTPConfig(**notification["smtp"]) if "smtp" in notification else None
        )
        serverchan_config = (
            ServerChanConfig(**notification["serverchan"])
            if "serverchan" in notification
            else None
        )

        recipients = []
        for r in data.get("recipients", []):
            # 邮件相关默认
            if smtp_config:
                if "email" not in r and smtp_config.default_receive_email:
                    r["email"] = smtp_config.default_receive_email
                if "reminder_days" not in r:
                    r["reminder_days"] = smtp_config.default_reminder_days
                if "template_file" not in r:
                    r["template_file"] = smtp_config.default_template_file
            # Server酱相关默认
            if serverchan_config:
                if "reminder_days" not in r:
                    r["reminder_days"] = serverchan_config.default_reminder_days
            recipients.append(Recipient(**r))

        return cls(
            smtp_config=smtp_config,
            serverchan_config=serverchan_config,
            recipients=recipients,
            notification_types=notification_types,
        )


if __name__ == "__main__":
    config = Config.from_yaml("config.example.yml")
    print(config)
