import pytest
import asyncio
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock

from src.main import BirthdayReminder
from src.core.config import Config


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
    with patch('src.main.Config.from_yaml', return_value=test_config), \
         patch('src.main.BirthdayChecker') as mock_checker_cls, \
         patch('src.notification.sender_email.EmailSender') as mock_email_sender, \
         patch('src.notification.sender_serverchan.ServerChanSender') as mock_serverchan_sender:
        # mock sender 实例
        mock_email = Mock()
        mock_email.render_content.return_value = "Test content"
        mock_email.send = AsyncMock()
        mock_email_sender.return_value = mock_email
        mock_serverchan = Mock()
        mock_serverchan.render_content.return_value = "Test content"
        mock_serverchan.send = AsyncMock()
        mock_serverchan_sender.return_value = mock_serverchan
        # mock checker 实例
        mock_checker = Mock()
        mock_checker_cls.return_value = mock_checker
        reminder = BirthdayReminder()
        return reminder, mock_checker


@pytest.mark.asyncio
async def test_birthday_reminder_initialization(reminder_and_checker, test_config):
    """测试BirthdayReminder初始化"""
    reminder, _ = reminder_and_checker
    assert reminder.config == test_config
    assert isinstance(reminder.root_dir, Path)
    assert isinstance(reminder.notification_senders, list)


@pytest.mark.asyncio
async def test_check_birthdays_no_birthdays(reminder_and_checker, test_recipients):
    """测试没有人过生日的情况"""
    reminder, mock_checker = reminder_and_checker
    mock_checker.check_birthdays.return_value = [
        (recipient, False, {}) for recipient in test_recipients
    ]

    await reminder.run()

    mock_checker.check_birthdays.assert_called_once()
    for sender in reminder.notification_senders:
        sender.render_content.assert_not_called()
        sender.send.assert_not_called()


@pytest.mark.asyncio
async def test_check_birthdays_with_birthday(reminder_and_checker, test_recipients, mock_extra_info):
    """测试有人过生日的情况"""
    reminder, mock_checker = reminder_and_checker
    mock_checker.check_birthdays.return_value = [
        (test_recipients[0], True, mock_extra_info),
        (test_recipients[1], False, {})
    ]
    for sender in reminder.notification_senders:
        sender.render_content.return_value = "Test content"
        sender.send = AsyncMock()

    await reminder.run()

    mock_checker.check_birthdays.assert_called_once()
    for sender in reminder.notification_senders:
        sender.render_content.assert_called_once_with(
            name=test_recipients[0].name,
            template_file=test_recipients[0].template_file,
            extra_info=mock_extra_info
        )
        sender.send.assert_called_once_with(
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
async def test_error_handling_birthday_check(reminder_and_checker):
    """测试生日检查错误处理"""
    reminder, mock_checker = reminder_and_checker
    mock_checker.check_birthdays.side_effect = Exception("Check error")
    with pytest.raises(Exception):
        await reminder.run()
