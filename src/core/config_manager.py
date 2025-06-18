"""
配置管理器 - 简单实用的配置管理
"""
from pathlib import Path
from typing import Optional
from src.core.config import Config
import logging

logger = logging.getLogger(__name__)


class ConfigManager:
    """配置管理器 - 只做必要的配置管理"""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self._config: Optional[Config] = None

    @property
    def config(self) -> Config:
        """获取配置，如果未加载则自动加载"""
        if self._config is None:
            self._config = self.load_config()
        return self._config

    def load_config(self) -> Config:
        """加载配置文件"""
        try:
            if not self.config_path:
                # 使用默认配置路径
                root_dir = Path(__file__).parent.parent.parent
                self.config_path = str(root_dir / "config.yml")

            logger.info(f"Loading config from: {self.config_path}")
            config = Config.from_yaml(self.config_path)
            logger.info("Config loaded successfully")
            return config

        except FileNotFoundError:
            logger.error(f"Config file not found: {self.config_path}")
            raise
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            raise

    def get_templates_dir(self) -> str:
        """获取模板目录路径"""
        root_dir = Path(__file__).parent.parent.parent
        return str(root_dir / "templates")

    def validate_config(self) -> bool:
        """验证配置的有效性"""
        try:
            config = self.config

            # 验证收件人配置
            if not config.recipients:
                logger.warning("No recipients configured")
                return False

            # 验证通知类型配置
            if not config.notification_types:
                logger.warning("No notification types configured")
                return False

            # 验证SMTP配置
            if "email" in config.notification_types and not config.smtp_config:
                logger.error("Email notification enabled but SMTP config missing")
                return False

            # 验证ServerChan配置
            if "serverchan" in config.notification_types and not config.serverchan_config:
                logger.error("ServerChan notification enabled but config missing")
                return False

            logger.info("Config validation passed")
            return True

        except Exception as e:
            logger.error(f"Config validation failed: {e}")
            return False
