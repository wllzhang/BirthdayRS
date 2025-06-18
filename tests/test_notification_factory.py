"""
测试通知工厂
"""
import pytest
from unittest.mock import Mock, patch
from src.core.notification_factory import NotificationFactory
from src.core.config import Config


class TestNotificationFactory:
    """测试通知工厂"""

    def test_initialization(self):
        """测试初始化"""
        factory = NotificationFactory("/test/templates")
        assert factory.templates_dir == "/test/templates"

    def test_create_senders_empty_config(self):
        """测试创建空的发送器列表"""
        factory = NotificationFactory("/test/templates")
        mock_config = Mock()
        mock_config.notification_types = []

        senders = factory.create_senders(mock_config)
        assert senders == []

    @patch('src.notification.sender_email.EmailSender')
    def test_create_email_sender(self, mock_email_sender):
        """测试创建邮件发送器"""
        factory = NotificationFactory("/test/templates")
        mock_config = Mock()
        mock_config.notification_types = ["email"]
        mock_config.smtp_config = Mock()
        mock_config.serverchan_config = None

        mock_sender = Mock()
        mock_email_sender.return_value = mock_sender

        senders = factory.create_senders(mock_config)

        assert len(senders) == 1
        assert senders[0] == mock_sender
        mock_email_sender.assert_called_once_with(mock_config.smtp_config, "/test/templates")

    @patch('src.notification.sender_serverchan.ServerChanSender')
    def test_create_serverchan_sender(self, mock_serverchan_sender):
        """测试创建ServerChan发送器"""
        factory = NotificationFactory("/test/templates")
        mock_config = Mock()
        mock_config.notification_types = ["serverchan"]
        mock_config.smtp_config = None
        mock_config.serverchan_config = Mock()
        mock_config.serverchan_config.default_sckey = "test_key"

        mock_sender = Mock()
        mock_serverchan_sender.return_value = mock_sender

        senders = factory.create_senders(mock_config)

        assert len(senders) == 1
        assert senders[0] == mock_sender
        mock_serverchan_sender.assert_called_once_with("test_key")

    @patch('src.notification.sender_email.EmailSender')
    @patch('src.notification.sender_serverchan.ServerChanSender')
    def test_create_multiple_senders(self, mock_serverchan_sender, mock_email_sender):
        """测试创建多个发送器"""
        factory = NotificationFactory("/test/templates")
        mock_config = Mock()
        mock_config.notification_types = ["email", "serverchan"]
        mock_config.smtp_config = Mock()
        mock_config.serverchan_config = Mock()
        mock_config.serverchan_config.default_sckey = "test_key"

        mock_email = Mock()
        mock_serverchan = Mock()
        mock_email_sender.return_value = mock_email
        mock_serverchan_sender.return_value = mock_serverchan

        senders = factory.create_senders(mock_config)

        assert len(senders) == 2
        assert mock_email in senders
        assert mock_serverchan in senders

    def test_create_unknown_sender_type(self):
        """测试创建未知的发送器类型"""
        factory = NotificationFactory("/test/templates")
        mock_config = Mock()
        mock_config.notification_types = ["unknown"]
        mock_config.smtp_config = None
        mock_config.serverchan_config = None

        senders = factory.create_senders(mock_config)

        assert senders == []

    def test_create_email_sender_without_smtp_config(self):
        """测试创建邮件发送器但没有SMTP配置"""
        factory = NotificationFactory("/test/templates")
        mock_config = Mock()
        mock_config.notification_types = ["email"]
        mock_config.smtp_config = None
        mock_config.serverchan_config = None

        senders = factory.create_senders(mock_config)

        assert senders == []

    def test_create_serverchan_sender_without_config(self):
        """测试创建ServerChan发送器但没有配置"""
        factory = NotificationFactory("/test/templates")
        mock_config = Mock()
        mock_config.notification_types = ["serverchan"]
        mock_config.smtp_config = None
        mock_config.serverchan_config = None

        senders = factory.create_senders(mock_config)

        assert senders == []

    @patch('src.notification.sender_email.EmailSender')
    def test_create_email_sender_exception(self, mock_email_sender):
        """测试创建邮件发送器时发生异常"""
        factory = NotificationFactory("/test/templates")
        mock_config = Mock()
        mock_config.notification_types = ["email"]
        mock_config.smtp_config = Mock()
        mock_config.serverchan_config = None

        mock_email_sender.side_effect = Exception("Email sender error")

        senders = factory.create_senders(mock_config)

        assert senders == []

    @patch('src.notification.sender_serverchan.ServerChanSender')
    def test_create_serverchan_sender_exception(self, mock_serverchan_sender):
        """测试创建ServerChan发送器时发生异常"""
        factory = NotificationFactory("/test/templates")
        mock_config = Mock()
        mock_config.notification_types = ["serverchan"]
        mock_config.smtp_config = None
        mock_config.serverchan_config = Mock()
        mock_config.serverchan_config.default_sckey = "test_key"

        mock_serverchan_sender.side_effect = Exception("ServerChan sender error")

        senders = factory.create_senders(mock_config)

        assert senders == []

    def test_create_senders_with_mixed_valid_invalid(self):
        """测试创建发送器时混合有效和无效类型"""
        factory = NotificationFactory("/test/templates")
        mock_config = Mock()
        mock_config.notification_types = ["email", "unknown", "serverchan"]
        mock_config.smtp_config = Mock()
        mock_config.serverchan_config = Mock()
        mock_config.serverchan_config.default_sckey = "test_key"

        with patch('src.notification.sender_email.EmailSender') as mock_email_sender, \
                patch('src.notification.sender_serverchan.ServerChanSender') as mock_serverchan_sender:

            mock_email = Mock()
            mock_serverchan = Mock()
            mock_email_sender.return_value = mock_email
            mock_serverchan_sender.return_value = mock_serverchan

            senders = factory.create_senders(mock_config)

            # 应该只创建有效的发送器
            assert len(senders) == 2
            assert mock_email in senders
            assert mock_serverchan in senders
