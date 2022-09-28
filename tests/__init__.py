"""Test package"""
from pathlib import Path

from crawlerstack_anticaptcha.config import settings


def update_test_settings():
    """
    更新测试配置
    :return:
    """
    test_config_path = Path(__file__).parent
    settings.load_file(test_config_path / 'settings.yml')
    settings.load_file(test_config_path / 'settings.local.yml')


# 重置测试数据库
update_test_settings()
