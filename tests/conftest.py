"""
测试配置文件
"""
import pytest
from pathlib import Path
import yaml
from src.core.config import Config, Recipient, SMTPConfig


@pytest.fixture
def test_config():
    """从示例配置文件加载测试配置"""
    config_path = Path(__file__).parent.parent / "config.example.yml"
    return Config.from_yaml(str(config_path))


@pytest.fixture
def test_recipients(test_config):
    """从测试配置中获取收件人列表"""
    return test_config.recipients


@pytest.fixture
def test_templates_dir():
    """获取模板目录路径"""
    return str(Path(__file__).parent.parent / "templates")
