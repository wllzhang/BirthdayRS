"""
通知发送器工厂 - 简单实用的对象创建
"""
from typing import List
from src.core.config import Config
from src.notification.notification_base import NotificationBase
import logging

logger = logging.getLogger(__name__)


class NotificationFactory:
    """通知发送器工厂 - 只做必要的对象创建"""

    def __init__(self, templates_dir: str):
        self.templates_dir = templates_dir

    def create_senders(self, config: Config) -> List[NotificationBase]:
        """根据配置创建通知发送器列表"""
        senders = []

        for notify_type in config.notification_types:
            sender = self._create_sender(notify_type, config)
            if sender:
                senders.append(sender)
                logger.info(f"Created {notify_type} sender")

        return senders

    def _create_sender(self, notify_type: str, config: Config):
        """创建单个通知发送器"""
        try:
            if notify_type == "email" and config.smtp_config:
                from src.notification.sender_email import EmailSender
                return EmailSender(config.smtp_config, self.templates_dir)

            elif notify_type == "serverchan" and config.serverchan_config:
                from src.notification.sender_serverchan import ServerChanSender
                return ServerChanSender(config.serverchan_config.default_sckey)

            else:
                logger.warning(f"Unknown notification type or missing config: {notify_type}")
                return None

        except Exception as e:
            logger.error(f"Failed to create {notify_type} sender: {e}")
            return None
