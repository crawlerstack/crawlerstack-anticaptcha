"""Models"""
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base

BaseModel = declarative_base()


class CaptchaCategoryModel(BaseModel):
    """
    验证码类型表

    记录每个验证码的名称以及对应的id
    """
    __tablename__ = 'captcha_category'
    id = Column(Integer, primary_key=True)
    # category_id = Column(Integer, primary_key=True, comment='Captcha category id')
    name = Column(String(255), unique=True)
    update_time = Column(DateTime, onupdate=datetime.now(), default=datetime.now(), comment='Update time')
    create_time = Column(DateTime, default=datetime.now(), comment='Create time')

    def __repr__(self):
        return f'<CaptchaCategory(category_type="{self.name}",' \
               f'create_time="{self.create_time}",update_time="{self.update_time}")>'


class StorageModel(BaseModel):
    """
    文件存储表

    存放验证码存储路径
    """
    __tablename__ = "storage"
    id = Column(Integer, primary_key=True)
    uri = Column(String(255), comment='Save the location.')
    name = Column(String(255), comment='Name of storage mode.')
    default = Column(Boolean, comment='Default opening mode.')
    update_time = Column(DateTime, onupdate=datetime.now(), default=datetime.now(), comment='Update time.')
    create_time = Column(DateTime, default=datetime.now(), comment='Create time.')


class CaptchaRecordModel(BaseModel):
    """
    验证码记录表

    记录每次上传的验证码识别结果、识别成功与否、删除状态等
    """
    __tablename__ = 'captcha_record'
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, comment='Captcha type id.')
    content = Column(String(255), default=None, comment='Extra content.')
    result = Column(String(255), comment='Identification result.')
    success = Column(Boolean, default=None, comment='Whether the parsing was successful.')
    deleted = Column(Boolean, default=False, comment='Delete status.')
    update_time = Column(DateTime, onupdate=datetime.now(), default=datetime.now(), comment='Update time.')
    create_time = Column(DateTime, default=datetime.now(), comment='Create time.')


class CaptchaFileModel(BaseModel):
    """
    验证码图像文件表

    记录每张验证码图像文件的存储位、存储方式、文件类型等
    """
    __tablename__ = 'captcha_file'
    id = Column(Integer, primary_key=True)
    record_id = Column(Integer, comment='Id used for event logging.')
    filename = Column(String(255), comment='Id generated from filename.')
    file_type = Column(String(255), comment='Image file type.')
    storage_id = Column(ForeignKey('storage.id'), comment='Storage mode id.')
    file_mark = Column(String(255), default=None, comment='Image mark.(foreground or background image)')
    update_time = Column(DateTime, onupdate=datetime.now(), default=datetime.now(), comment='Update time.')
    create_time = Column(DateTime, default=datetime.now(), comment='Create time.')
