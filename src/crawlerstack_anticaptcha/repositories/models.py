"""Models"""
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class CategoryModel(Base):  # pylint:disable=R0903
    """CategoryModel"""
    __tablename__ = 'category'
    category_id = Column(Integer, primary_key=True)
    category = Column(String)

    def __repr__(self):
        return f'<Category(category_id="{self.category_id}",category="{self.category}")>'


class CaptchaModel(Base):  # pylint:disable=R0903
    """CaptchaModel"""
    __tablename__ = 'captcha'
    file_id = Column(String, comment='Id generated from filename')
    category_id = Column(Integer, primary_key=True, comment='Captcha type id')
    file_path = Column(String, comment='The local save path of the image file')
    file_type = Column(String, comment='Image file type')
    creation_time = Column(DateTime, default=datetime.now, comment='Creation time')
    success = Column(Boolean, comment='Explain success')

    def __repr__(self):
        return f'<CaptchaModel(file_id="{self.file_id}",category_id="{self.category_id}",' \
               f'file_type="{self.file_type}",success="{self.success}")>'
