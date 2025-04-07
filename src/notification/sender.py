"""
通知发送模块，包含邮件模板渲染和发送功能
"""
import os
from pathlib import Path
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
from typing import Dict, Optional

from src.core.config import SMTPConfig
from src.core.checker import Recipient


class NotificationSender:
    def __init__(self, smtp_config: SMTPConfig, templates_dir: str):
        """
        初始化通知发送器

        Args:
            smtp_config: SMTP配置
            templates_dir: 模板目录路径
        """
        self.smtp_config = smtp_config
        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=True
        )

    def _render_template(self, template_name: str, **kwargs) -> str:
        """渲染模板"""
        template = self.env.get_template(template_name)
        return template.render(**kwargs)

    def render_birthday_email(self, name: str, template_file: str, extra_info: Dict) -> str:
        """
        渲染生日邮件内容

        Args:
            name: 收件人姓名
            template_file: 模板文件名
            extra_info: 额外信息，包含生肖和节气等
        """
        template = self.env.get_template(template_file)
        return template.render(name=name, **extra_info)

    async def send_email(self, to_email: str, subject: str, content: str):
        """发送邮件"""
        message = MIMEMultipart()
        message["From"] = self.smtp_config.username
        message["To"] = to_email
        message["Subject"] = subject
        message.attach(MIMEText(content, "html"))

        async with aiosmtplib.SMTP(
            hostname=self.smtp_config.host,
            port=self.smtp_config.port,
            use_tls=self.smtp_config.use_tls
        ) as smtp:
            await smtp.login(self.smtp_config.username, self.smtp_config.password)
            await smtp.send_message(message)

    async def send_birthday_reminder(self, recipient: Recipient, content: str, days_until: int, age: int):
        """发送生日提醒邮件"""
        subject = f"生日提醒- {recipient.name} - {age}岁 - {days_until}天后"
        await self.send_email(recipient.email, subject, content)
