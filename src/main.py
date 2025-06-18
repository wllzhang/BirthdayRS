"""
主程序入口
"""

import asyncio
import logging
import sys
from typing import List, Tuple, Dict
import click

from src.core.config_manager import ConfigManager
from src.core.notification_factory import NotificationFactory
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
        # 初始化配置管理器
        self.config_manager = ConfigManager(config_path)

        # 验证配置
        if not self.config_manager.validate_config():
            raise ValueError("Invalid configuration")

        # 获取配置
        self.config = self.config_manager.config

        # 初始化组件
        self._initialize_components()

    def _initialize_components(self):
        """初始化组件 - 简单直接"""
        try:
            # 创建生日检查器
            self.birthday_checker = BirthdayChecker()

            # 创建通知发送器
            notification_factory = NotificationFactory(self.config_manager.get_templates_dir())
            self.notification_senders = notification_factory.create_senders(self.config)

            logger.info("Components initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize components: {e}")
            raise

    async def send_birthday_reminder(self, recipient: Recipient, extra_info: Dict) -> None:
        """发送生日提醒"""
        try:
            logger.info(f"Sending birthday reminder to {recipient.name}")

            for sender in self.notification_senders:
                try:
                    # 渲染内容
                    content = sender.render_content(
                        name=recipient.name,
                        template_file=recipient.template_file,
                        extra_info=extra_info,
                    )

                    # 发送通知
                    await sender.send(
                        recipient=recipient,
                        content=content,
                        days_until=extra_info["days_until"],
                        age=extra_info["age"],
                    )

                    logger.info(f"Successfully sent {type(sender).__name__} notification to {recipient.name}")

                except Exception as e:
                    logger.error(f"Failed to send {type(sender).__name__} notification to {recipient.name}: {e}")
                    # 继续尝试其他发送器，不中断整个流程

        except Exception as e:
            logger.error(f"Failed to send birthday reminder to {recipient.name}: {e}")
            raise

    def check_birthdays(self) -> List[Tuple[Recipient, bool, Dict]]:
        """检查所有人的生日"""
        try:
            logger.info(f"Checking birthdays for {len(self.config.recipients)} recipients")
            results = self.birthday_checker.check_birthdays(self.config.recipients)

            # 统计结果
            birthday_count = sum(1 for _, is_birthday, _ in results if is_birthday)
            logger.info(f"Found {birthday_count} birthdays today")

            return results

        except Exception as e:
            logger.error(f"Failed to check birthdays: {e}")
            raise

    async def run(self) -> None:
        """运行生日提醒主流程"""
        try:
            logger.info("Starting birthday reminder application")

            # 检查生日
            birthday_results = self.check_birthdays()

            # 收集需要发送提醒的任务
            tasks = []
            for recipient, is_birthday, extra_info in birthday_results:
                if is_birthday:
                    logger.info(f"Processing birthday for {recipient.name}")
                    tasks.append(self.send_birthday_reminder(recipient, extra_info))

            # 并发发送所有提醒
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
                logger.info(f"Successfully processed {len(tasks)} birthday reminders")
            else:
                logger.info("No birthdays to process today")

        except Exception as e:
            logger.error(f"Application error: {type(e).__name__}: {e}")
            raise

    def reload_config(self) -> None:
        """重新加载配置"""
        try:
            # 重新加载配置
            self.config_manager._config = None
            self.config = self.config_manager.config

            # 重新初始化组件
            self._initialize_components()

            logger.info("Configuration reloaded successfully")

        except Exception as e:
            logger.error(f"Failed to reload configuration: {e}")
            raise


@click.group()
def cli():
    """生日提醒系统 - 简洁版本"""
    pass


@cli.command()
@click.option('--config', '-c', help='配置文件路径', default="config.yml")
def run(config):
    """运行生日提醒主流程"""
    try:
        app = BirthdayReminder(config)
        asyncio.run(app.run())
    except Exception as e:
        logger.error(f"Application failed: {e}")
        sys.exit(1)


@cli.command()
@click.option('--config', '-c', help='配置文件路径', default="config.yml")
def preview():
    """预览生日提醒邮件内容（默认模板）"""
    try:
        from src.notification.sender_email import EmailSender
        EmailSender.preview_email(web_open=True)
        print("已生成预览文件并尝试打开浏览器。")
    except Exception as e:
        logger.error(f"Preview failed: {e}")
        sys.exit(1)


@cli.command()
@click.option('--config', '-c', help='配置文件路径', default="config.yml")
def validate(config):
    """验证配置文件"""
    try:
        config_manager = ConfigManager(config)
        if config_manager.validate_config():
            print("✅ 配置文件验证通过")
        else:
            print("❌ 配置文件验证失败")
            sys.exit(1)
    except Exception as e:
        print(f"❌ 配置文件验证失败: {e}")
        sys.exit(1)


@cli.command()
@click.option('--config', '-c', help='配置文件路径', default="config.yml")
def info(config):
    """显示应用信息"""
    try:
        config_manager = ConfigManager(config)
        config = config_manager.config

        print("📋 应用信息:")
        print(f"  检查生日人数: {len(config.recipients)}")
        print(f"  通知类型: {', '.join(config.notification_types)}")
        print(f"  模板目录: {config_manager.get_templates_dir()}")

        if config.smtp_config:
            print(f"  SMTP服务器: {config.smtp_config.host}:{config.smtp_config.port}")

        if config.serverchan_config:
            print("  ServerChan: 已配置")

    except Exception as e:
        logger.error(f"Failed to get app info: {e}")
        sys.exit(1)


if __name__ == "__main__":
    cli()
