"""
测试配置管理器
"""
import pytest
from unittest.mock import Mock, patch
from unittest.mock import PropertyMock
from src.core.config_manager import ConfigManager
from src.core.config import Config


class TestConfigManager:
    """测试配置管理器"""

    def test_initialization(self):
        """测试初始化"""
        config_manager = ConfigManager()
        assert config_manager.config_path is None
        assert config_manager._config is None

    def test_initialization_with_path(self):
        """测试带路径的初始化"""
        config_manager = ConfigManager("test_config.yml")
        assert config_manager.config_path == "test_config.yml"

    def test_get_templates_dir(self):
        """测试获取模板目录"""
        config_manager = ConfigManager()
        templates_dir = config_manager.get_templates_dir()

        assert isinstance(templates_dir, str)
        assert "templates" in templates_dir

    @patch('src.core.config_manager.Config.from_yaml')
    def test_load_config_success(self, mock_from_yaml):
        """测试成功加载配置"""
        mock_config = Mock(spec=Config)
        mock_from_yaml.return_value = mock_config

        config_manager = ConfigManager("test_config.yml")
        config = config_manager.load_config()

        assert config == mock_config
        mock_from_yaml.assert_called_once_with("test_config.yml")

    @patch('src.core.config_manager.Config.from_yaml')
    def test_load_config_file_not_found(self, mock_from_yaml):
        """测试配置文件不存在"""
        mock_from_yaml.side_effect = FileNotFoundError("Config file not found")

        config_manager = ConfigManager("nonexistent.yml")
        with pytest.raises(FileNotFoundError):
            config_manager.load_config()

    @patch('src.core.config_manager.Config.from_yaml')
    def test_load_config_other_error(self, mock_from_yaml):
        """测试其他配置加载错误"""
        mock_from_yaml.side_effect = Exception("Other error")

        config_manager = ConfigManager("test_config.yml")
        with pytest.raises(Exception):
            config_manager.load_config()

    @patch('src.core.config_manager.Config.from_yaml')
    def test_config_property_lazy_loading(self, mock_from_yaml):
        """测试配置属性的懒加载"""
        mock_config = Mock(spec=Config)
        mock_from_yaml.return_value = mock_config

        config_manager = ConfigManager("test_config.yml")

        # 第一次访问时应该加载配置
        config = config_manager.config
        assert config == mock_config
        mock_from_yaml.assert_called_once()

        # 第二次访问时不应该重新加载
        config2 = config_manager.config
        assert config2 == mock_config
        mock_from_yaml.assert_called_once()  # 仍然只调用一次

    def test_validate_config_no_recipients(self):
        """测试验证配置 - 没有收件人"""
        with patch.object(ConfigManager, 'config', new_callable=PropertyMock) as mock_config_property:
            mock_config = Mock()
            mock_config.recipients = []
            mock_config.notification_types = ["email"]
            mock_config.smtp_config = Mock()
            mock_config_property.return_value = mock_config

            config_manager = ConfigManager()
            result = config_manager.validate_config()

            assert result is False

    def test_validate_config_no_notification_types(self):
        """测试验证配置 - 没有通知类型"""
        with patch.object(ConfigManager, 'config', new_callable=PropertyMock) as mock_config_property:
            mock_config = Mock()
            mock_config.recipients = [Mock()]
            mock_config.notification_types = []
            mock_config_property.return_value = mock_config

            config_manager = ConfigManager()
            result = config_manager.validate_config()

            assert result is False

    def test_validate_config_email_without_smtp(self):
        """测试验证配置 - 邮件通知但没有SMTP配置"""
        with patch.object(ConfigManager, 'config', new_callable=PropertyMock) as mock_config_property:
            mock_config = Mock()
            mock_config.recipients = [Mock()]
            mock_config.notification_types = ["email"]
            mock_config.smtp_config = None
            mock_config_property.return_value = mock_config

            config_manager = ConfigManager()
            result = config_manager.validate_config()

            assert result is False

    def test_validate_config_serverchan_without_config(self):
        """测试验证配置 - ServerChan通知但没有配置"""
        with patch.object(ConfigManager, 'config', new_callable=PropertyMock) as mock_config_property:
            mock_config = Mock()
            mock_config.recipients = [Mock()]
            mock_config.notification_types = ["serverchan"]
            mock_config.serverchan_config = None
            mock_config_property.return_value = mock_config

            config_manager = ConfigManager()
            result = config_manager.validate_config()

            assert result is False

    def test_validate_config_success(self):
        """测试验证配置成功"""
        with patch.object(ConfigManager, 'config', new_callable=PropertyMock) as mock_config_property:
            mock_config = Mock()
            mock_config.recipients = [Mock()]
            mock_config.notification_types = ["email"]
            mock_config.smtp_config = Mock()
            mock_config.serverchan_config = None
            mock_config_property.return_value = mock_config

            config_manager = ConfigManager()
            result = config_manager.validate_config()

            assert result is True

    def test_validate_config_exception(self):
        """测试验证配置时发生异常"""
        with patch.object(ConfigManager, 'config', new_callable=PropertyMock, side_effect=Exception("Config error")):
            config_manager = ConfigManager()
            result = config_manager.validate_config()

            assert result is False
