"""test log"""
from crawlerstack_anticaptcha.utils.log import mkdir


def test_mkdir(mock_path):
    """test mkdir"""
    test_path = mock_path / 'test'
    mkdir(test_path)
    assert test_path.exists()
