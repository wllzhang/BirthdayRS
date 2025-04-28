"""
通知发送模块，包含邮件模板渲染和发送功能
"""
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
from typing import Dict
import asyncio
import logging
from functools import wraps

from src.core.config import SMTPConfig
from src.core.checker import Recipient

logger = logging.getLogger(__name__)


def retry_on_failure(max_retries=3, delay=1):
    """重试装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds...")
                        await asyncio.sleep(delay)
            raise last_exception
        return wrapper
    return decorator


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
        try:
            template = self.env.get_template(template_name)
            return template.render(**kwargs)
        except Exception as e:
            logger.error(f"Failed to render template {template_name}: {e}")
            raise

    def render_birthday_email(self, name: str, template_file: str, extra_info: Dict) -> str:
        """
        渲染生日邮件内容

        Args:
            name: 收件人姓名
            template_file: 模板文件名
            extra_info: 额外信息，包含生肖和节气等
        """
        try:
            template = self.env.get_template(template_file)
            return template.render(name=name, **extra_info)
        except Exception as e:
            logger.error(f"Failed to render birthday email for {name}: {e}")
            raise

    @retry_on_failure()
    async def send_email(self, to_email: str, subject: str, content: str):
        """发送邮件"""
        try:
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
                logger.info(f"Successfully sent email to {to_email}")
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {type(e).__name__}: {e}")
            raise

    async def send_birthday_reminder(self, recipient: Recipient, content: str, days_until: int, age: int):
        """发送生日提醒邮件"""
        try:
            subject = f"生日提醒- {recipient.name} - {age}岁 - {days_until}天后"
            await self.send_email(recipient.email, subject, content)
        except Exception as e:
            logger.error(f"Failed to send birthday reminder to {recipient.name} ({recipient.email}): {e}")
            raise
