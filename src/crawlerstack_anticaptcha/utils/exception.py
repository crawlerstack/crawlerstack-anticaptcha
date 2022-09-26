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
