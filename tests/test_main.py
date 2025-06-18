import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from src.main import BirthdayReminder


@pytest.fixture
def mock_extra_info():
    """模拟的额外信息，使用checker.py中的默认值"""
    return {
        'solar_match': False,
        'lunar_match': False,
        'days_until': 0,
        'age': 34,
        'zodiac': '',
        'gz_year': '',
        'gz_month': '',
        'gz_day': '',
        'gz_hour': '',
        'lunar_month': '',
        'lunar_day': '',
        'lunar_festival': '',
        'solar_festival': '',
        'solar_term': '',
        'week_name': '',
        'constellation': ''
    }


@pytest.fixture
def reminder_and_checker(test_config):
    """创建BirthdayReminder实例和相关的mock对象"""
    with patch('src.main.ConfigManager') as mock_config_manager_cls, \
            patch('src.main.NotificationFactory') as mock_factory_cls, \
            patch('src.main.BirthdayChecker') as mock_checker_cls:

        # Mock ConfigManager
        mock_config_manager = Mock()
        mock_config_manager.config = test_config
        mock_config_manager.validate_config.return_value = True
        mock_config_manager.get_templates_dir.return_value = "/test/templates"
        mock_config_manager_cls.return_value = mock_config_manager

        # Mock NotificationFactory
        mock_factory = Mock()
        mock_email_sender = Mock()
        mock_email_sender.render_content.return_value = "Test content"
        mock_email_sender.send = AsyncMock()
        mock_factory.create_senders.return_value = [mock_email_sender]
        mock_factory_cls.return_value = mock_factory

        # Mock BirthdayChecker
        mock_checker = Mock()
        mock_checker_cls.return_value = mock_checker

        reminder = BirthdayReminder()
        return reminder, mock_checker, mock_email_sender


@pytest.mark.asyncio
async def test_birthday_reminder_initialization(reminder_and_checker, test_config):
    """测试BirthdayReminder初始化"""
    reminder, _, _ = reminder_and_checker
    assert reminder.config == test_config
    assert isinstance(reminder.notification_senders, list)
    assert len(reminder.notification_senders) == 1


@pytest.mark.asyncio
async def test_check_birthdays_no_birthdays(reminder_and_checker, test_recipients):
    """测试没有人过生日的情况"""
    reminder, mock_checker, mock_sender = reminder_and_checker
    mock_checker.check_birthdays.return_value = [
        (recipient, False, {}) for recipient in test_recipients
    ]

    await reminder.run()

    mock_checker.check_birthdays.assert_called_once()
    mock_sender.render_content.assert_not_called()
    mock_sender.send.assert_not_called()


@pytest.mark.asyncio
async def test_check_birthdays_with_birthday(reminder_and_checker, test_recipients, mock_extra_info):
    """测试有人过生日的情况"""
    reminder, mock_checker, mock_sender = reminder_and_checker
    mock_checker.check_birthdays.return_value = [
        (test_recipients[0], True, mock_extra_info),
        (test_recipients[1], False, {})
    ]

    await reminder.run()

    mock_checker.check_birthdays.assert_called_once()
    mock_sender.render_content.assert_called_once_with(
        name=test_recipients[0].name,
        template_file=test_recipients[0].template_file,
        extra_info=mock_extra_info
    )
    mock_sender.send.assert_called_once_with(
        recipient=test_recipients[0],
        content="Test content",
        days_until=mock_extra_info['days_until'],
        age=mock_extra_info['age']
    )


@pytest.mark.asyncio
async def test_send_birthday_reminder(reminder_and_checker, test_recipients, mock_extra_info):
    """测试发送生日提醒"""
    reminder, _, mock_sender = reminder_and_checker

    await reminder.send_birthday_reminder(test_recipients[0], mock_extra_info)

    mock_sender.render_content.assert_called_once_with(
        name=test_recipients[0].name,
        template_file=test_recipients[0].template_file,
        extra_info=mock_extra_info
    )
    mock_sender.send.assert_called_once_with(
        recipient=test_recipients[0],
        content="Test content",
        days_until=mock_extra_info['days_until'],
        age=mock_extra_info['age']
    )


@pytest.mark.asyncio
async def test_error_handling_config_load():
    """测试配置加载错误处理"""
    with patch('src.main.ConfigManager') as mock_config_manager_cls:
        mock_config_manager = Mock()
        mock_config_manager.validate_config.return_value = False
        mock_config_manager_cls.return_value = mock_config_manager

        with pytest.raises(ValueError, match="Invalid configuration"):
            BirthdayReminder()


@pytest.mark.asyncio
async def test_error_handling_birthday_check(reminder_and_checker):
    """测试生日检查错误处理"""
    reminder, mock_checker, _ = reminder_and_checker
    mock_checker.check_birthdays.side_effect = Exception("Check error")

    with pytest.raises(Exception):
        await reminder.run()


@pytest.mark.asyncio
async def test_error_handling_notification_send(reminder_and_checker, test_recipients, mock_extra_info):
    """测试通知发送错误处理"""
    reminder, _, mock_sender = reminder_and_checker
    mock_sender.send.side_effect = Exception("Send error")

    # 不应抛出异常，只应记录日志
    await reminder.send_birthday_reminder(test_recipients[0], mock_extra_info)
    mock_sender.render_content.assert_called_once()
    mock_sender.send.assert_called_once()


@pytest.mark.asyncio
async def test_reload_config(reminder_and_checker, test_config):
    """测试重新加载配置"""
    reminder, _, _ = reminder_and_checker

    # 保存原始配置
    original_config = reminder.config

    # 重新加载配置
    reminder.reload_config()

    # 验证配置被重新加载（应该还是原来的配置，因为我们mock了ConfigManager）
    assert reminder.config == original_config


def test_check_birthdays_method(reminder_and_checker, test_recipients):
    """测试check_birthdays方法"""
    reminder, mock_checker, _ = reminder_and_checker

    expected_results = [
        (test_recipients[0], True, {'days_until': 0, 'age': 25}),
        (test_recipients[1], False, {})
    ]
    mock_checker.check_birthdays.return_value = expected_results

    results = reminder.check_birthdays()

    assert results == expected_results
    mock_checker.check_birthdays.assert_called_once_with(test_recipients)
