import pytest
import asyncio
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock

from src.main import BirthdayReminder
from src.core.config import Config
from src.core.checker import BirthdayChecker
from src.notification.sender import NotificationSender


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
def mock_components():
    """模拟组件"""
    return {
        'notification_sender': Mock(spec=NotificationSender),
        'birthday_checker': Mock(spec=BirthdayChecker)
    }


@pytest.fixture
def reminder(test_config, mock_components):
    """创建测试用的BirthdayReminder实例"""
    with patch('src.main.Config.from_yaml', return_value=test_config), \
            patch('src.main.NotificationSender', return_value=mock_components['notification_sender']), \
            patch('src.main.BirthdayChecker', return_value=mock_components['birthday_checker']):
        return BirthdayReminder()


@pytest.mark.asyncio
async def test_birthday_reminder_initialization(reminder, test_config):
    """测试BirthdayReminder初始化"""
    assert reminder.config == test_config
    assert isinstance(reminder.root_dir, Path)


@pytest.mark.asyncio
async def test_check_birthdays_no_birthdays(reminder, mock_components, test_recipients):
    """测试没有人过生日的情况"""
    mock_components['birthday_checker'].check_birthdays.return_value = [
        (recipient, False, {}) for recipient in test_recipients
    ]

    await reminder.run()

    mock_components['birthday_checker'].check_birthdays.assert_called_once()
    mock_components['notification_sender'].send_birthday_reminder.assert_not_called()
    mock_components['notification_sender'].render_birthday_email.assert_not_called()


@pytest.mark.asyncio
async def test_check_birthdays_with_birthday(reminder, mock_components, test_recipients, mock_extra_info):
    """测试有人过生日的情况"""
    # 设置第一个用户过生日
    mock_components['birthday_checker'].check_birthdays.return_value = [
        (test_recipients[0], True, mock_extra_info),
        (test_recipients[1], False, {})
    ]
    mock_components['notification_sender'].render_birthday_email.return_value = "Test content"
    mock_components['notification_sender'].send_birthday_reminder = AsyncMock()

    await reminder.run()

    mock_components['birthday_checker'].check_birthdays.assert_called_once()
    mock_components['notification_sender'].render_birthday_email.assert_called_once_with(
        name=test_recipients[0].name,
        template_file=test_recipients[0].template_file,
        extra_info=mock_extra_info
    )
    mock_components['notification_sender'].send_birthday_reminder.assert_called_once_with(
        recipient=test_recipients[0],
        content="Test content",
        days_until=mock_extra_info['days_until'],
        age=mock_extra_info['age']
    )


@pytest.mark.asyncio
async def test_error_handling_config_load():
    """测试配置加载错误处理"""
    with patch('src.main.Config.from_yaml', side_effect=Exception("Config error")), \
            pytest.raises(Exception):
        BirthdayReminder()


@pytest.mark.asyncio
async def test_error_handling_birthday_check(reminder, mock_components):
    """测试生日检查错误处理"""
    mock_components['birthday_checker'].check_birthdays.side_effect = Exception(
        "Check error")
    with pytest.raises(Exception):
        await reminder.run()


@pytest.mark.asyncio
async def test_error_handling_email_send(reminder, mock_components, test_recipients, mock_extra_info):
    """测试邮件发送错误处理"""
    mock_components['birthday_checker'].check_birthdays.return_value = [
        (test_recipients[0], True, mock_extra_info)
    ]
    mock_components['notification_sender'].render_birthday_email.return_value = "Test content"
    mock_components['notification_sender'].send_birthday_reminder = AsyncMock(
        side_effect=Exception("Email error")
    )

    with pytest.raises(Exception):
        await reminder.run()
