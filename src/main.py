"""
主程序入口
"""
import asyncio
import logging
import sys
import webbrowser
from pathlib import Path
from typing import List, Tuple, Dict
import click
from datetime import datetime

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
        self.config_path = config_path or str(self.root_dir / "config.yml")
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
                recipient=recipient,
                content=content,
                days_until=extra_info['days_until'],
                age=extra_info['age']
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

    async def preview_email(self, recipient_name: str = None, date_str: str = None) -> None:
        """预览邮件内容"""
        recipient = Recipient(
            name=recipient_name or "测试用户",
            email="test@example.com",
            solar_birthday="1990-01-01",
            lunar_birthday="1990-02-15",
            reminder_days=3,
            template_file="birthday.html"
        )

        check_date = datetime.strptime(
            date_str, "%Y-%m-%d") if date_str else datetime.now()

        extra_info = {
            'solar_match': True,
            'lunar_match': False,
            'days_until': 0,
            'age': 34,
            'zodiac': '马',
            'gz_year': '庚午',
            'gz_month': '戊寅',
            'gz_day': '甲子',
            'gz_hour': '甲子',
            'lunar_month': '正月',
            'lunar_day': '十五',
            'lunar_festival': '元宵节',
            'solar_festival': '元旦',
            'solar_term': '立春',
            'week_name': '星期一',
            'constellation': '摩羯座'
        }

        content = self.notification_sender.render_birthday_email(
            name=recipient.name,
            template_file=recipient.template_file,
            extra_info=extra_info
        )

        preview_dir = self.root_dir / "previews"
        preview_dir.mkdir(exist_ok=True)
        preview_file = preview_dir / \
            f"preview_{recipient.name}_{check_date.strftime('%Y%m%d')}.html"

        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>生日提醒预览 - {recipient.name}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .preview-info {{
                    background-color: #f5f5f5;
                    padding: 10px;
                    margin-bottom: 20px;
                    border-radius: 5px;
                }}
            </style>
        </head>
        <body>
            <div class="preview-info">
                <h2>邮件预览信息</h2>
                <p><strong>收件人:</strong> {recipient.name} &lt;{recipient.email}&gt;</p>
                <p><strong>日期:</strong> {check_date.strftime('%Y-%m-%d')}</p>
                <p><strong>提前天数:</strong> {extra_info['days_until']}</p>
            </div>
            {content}
        </body>
        </html>
        """

        with open(preview_file, "w", encoding="utf-8") as f:
            f.write(full_html)

        webbrowser.open(f"file://{preview_file.absolute()}")
        print(f"预览文件已保存到: {preview_file}")


@click.group()
def cli():
    """生日提醒系统"""
    pass


@cli.command()
@click.option('--recipient', '-r', help='要预览的收件人姓名')
@click.option('--date', '-d', help='预览日期 (格式: YYYY-MM-DD)')
def preview(recipient, date):
    """预览邮件内容"""
    asyncio.run(BirthdayReminder().preview_email(recipient, date))


@cli.command()
def run():
    """运行生日提醒主流程"""
    asyncio.run(BirthdayReminder().run())


if __name__ == "__main__":
    cli()
