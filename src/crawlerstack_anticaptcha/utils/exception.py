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

    def __init__(self, content: str, media_type: str):
        self.content = content
        self.media_type = media_type


class ParsingFailed(CrawlerStackAnticaptcha):
    """
    Parsing failed
    """

    def __init__(self):
        self.content = 'Parsing failed, Please upload again'


class ObjectIndexError(CrawlerStackAnticaptcha):
    """
    object index error
    """
    def __init__(self):
        self.content = 'List multiple objects'
