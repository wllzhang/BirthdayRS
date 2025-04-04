import asyncio
import logging
import os
import sys
from pathlib import Path
from typing import List, Tuple, Dict

from src.core.config import Config
from src.core.checker import BirthdayChecker, Recipient
from src.notification.sender import NotificationSender

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('birthday_reminder.log')
    ]
)
logger = logging.getLogger(__name__)


class BirthdayReminder:
    def __init__(self, config_path: str = None):
        self.root_dir = Path(__file__).parent.parent
        self.config_path = config_path or str(
            self.root_dir / "config.yml")
        self.config = self._load_config()
        self.notification_sender = NotificationSender(
            self.config.smtp,
            str(self.root_dir / "templates")
        )
        self.birthday_checker = BirthdayChecker()

    def _load_config(self) -> Config:
        """加载配置文件"""
        try:
            return Config.from_yaml(self.config_path)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            raise

    async def send_birthday_reminder(self, recipient: Recipient, extra_info: Dict) -> None:
        """发送生日提醒邮件"""
        try:
            content = self.notification_sender.render_birthday_email(
                name=recipient.name,
                template_file=recipient.template_file,
                extra_info=extra_info
            )

            await self.notification_sender.send_birthday_reminder(
                recipient_name=recipient.name,
                recipient_email=recipient.email,
                content=content,
                days_until=extra_info['days_until']
            )
            logger.info(
                f"Successfully sent birthday reminder to {recipient.name}")
        except Exception as e:
            logger.error(f"Failed to send email to {recipient.name}: {e}")
            raise

    def check_birthdays(self) -> List[Tuple[Recipient, bool, Dict]]:
        """检查所有人的生日"""
        try:
            return self.birthday_checker.check_birthdays(self.config.recipients)
        except Exception as e:
            logger.error(f"Failed to check birthdays: {e}")
            raise

    async def run(self) -> None:
        """运行生日提醒主流程"""
        logger.info("Starting birthday reminder check")
        try:
            birthday_results = self.check_birthdays()

            for recipient, is_birthday, extra_info in birthday_results:
                logger.info(f"Checking birthday for {recipient.name}")
                if is_birthday:
                    await self.send_birthday_reminder(recipient, extra_info)

            logger.info("Birthday check completed successfully")
        except Exception as e:
            logger.error(f"Error during birthday check: {e}")
            raise


async def main():
    """主入口函数"""
    try:
        reminder = BirthdayReminder()
        await reminder.run()
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
