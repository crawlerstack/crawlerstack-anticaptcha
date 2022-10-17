"""exception"""


class CrawlerStackAnticaptcha(Exception):
    """
    异常基类
    """


class ObjectDoesNotExist(CrawlerStackAnticaptcha):
    """
    object does not exist.
    """

    def __init__(self, content: str):
        self.content = content


class UnsupportedMediaType(CrawlerStackAnticaptcha):
    """
    unsupported media type
    """

    def __init__(self, content: str):
        self.content = content


class SliderCaptchaParseFailed(CrawlerStackAnticaptcha):
    """
    SliderCaptchaParseFailed
    """

    def __init__(self):
        self.content = 'Parsing failed, please upload again.'


class NumericalCaptchaParseFailed(CrawlerStackAnticaptcha):
    """
    NumericalCaptchaParseFailed
    """

    def __init__(self):
        self.content = 'Parse failed.'
