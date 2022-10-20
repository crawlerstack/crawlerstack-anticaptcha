"""test preprocessing"""

from crawlerstack_anticaptcha.captcha.numerical.preprocessing import take_first


def test_take_first():
    """test take first"""
    result = take_first([[1, 2, 3], [4, 5, 6]])
    assert result == 1
