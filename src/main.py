"""
主程序入口
"""

import asyncio
import logging
import sys
from pathlib import Path
from typing import List, Tuple, Dict
import click
from src.core.config import Config
from src.core.checker import BirthdayChecker, Recipient


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("birthday_reminder.log"),
    ],
)
logger = logging.getLogger(__name__)


class BirthdayReminder:
    def __init__(self, config_path: str = None):
        self.root_dir = Path(__file__).parent.parent
        self.config_path = config_path or str(self.root_dir / "config.yml")
        self.config = self._load_config()
        self.notification_senders = []
        for notify_type in self.config.notification_types:
            if notify_type == "email" and self.config.smtp_config:
                from src.notification.sender_email import EmailSender

                self.notification_senders.append(
                    EmailSender(
                        self.config.smtp_config, str(self.root_dir / "templates")
                    )
                )
            elif notify_type == "serverchan" and self.config.serverchan_config:
                from src.notification.sender_serverchan import ServerChanSender

                self.notification_senders.append(
                    ServerChanSender(self.config.serverchan_config.default_sckey)
                )
        self.birthday_checker = BirthdayChecker()

    def _load_config(self) -> Config:
        """加载配置文件"""
        try:
            return Config.from_yaml(self.config_path)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            raise

    async def send_birthday_reminder(
        self, recipient: Recipient, extra_info: Dict
    ) -> None:
        """发送生日提醒邮件"""
        try:
            for sender in self.notification_senders:
                content = sender.render_content(
                    name=recipient.name,
                    template_file=recipient.template_file,
                    extra_info=extra_info,
                )
                await sender.send(
                    recipient=recipient,
                    content=content,
                    days_until=extra_info["days_until"],
                    age=extra_info["age"],
                )
            logger.info(f"Successfully sent birthday reminder to {recipient.name}")
        except Exception as e:
            logger.error(f"Failed to send notification to {recipient.name}: {e}")
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
            tasks = []

            for recipient, is_birthday, extra_info in birthday_results:
                logger.info(f"Checking birthday for {recipient.name}")
                if is_birthday:
                    tasks.append(self.send_birthday_reminder(recipient, extra_info))

            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
                logger.info(f"Successfully processed {len(tasks)} birthday reminders")
            else:
                logger.info("No birthdays to process today")

        except Exception as e:
            logger.error(f"Error during birthday check: {type(e).__name__}: {e}")
            raise


@click.group()
def cli():
    """生日提醒系统"""
    pass


@cli.command()
def run():
    """运行生日提醒主流程"""
    asyncio.run(BirthdayReminder().run())


@cli.command()
def preview():
    """预览生日提醒邮件内容（默认模板）"""
    from src.notification.sender_email import EmailSender
    EmailSender.preview_email(web_open=True)
    print("已生成预览文件并尝试打开浏览器。")


if __name__ == "__main__":
    cli()
