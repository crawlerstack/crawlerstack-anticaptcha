"""Models"""
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base

BaseModel = declarative_base()


class CategoryModel(BaseModel):
    """CategoryModel"""
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    path = Column(String(255))

    def __repr__(self):
        return f'<Category(category_id="{self.id}",category_type="{self.name}",path="{self.path}")>'


class CaptchaModel(BaseModel):
    """CaptchaModel"""
    __tablename__ = 'captcha'
    id = Column(Integer, primary_key=True)
    file_id = Column(String(255), comment='Id generated from filename', unique=True)
    category_id = Column(ForeignKey('category.id'), comment='Captcha type id')
    file_type = Column(String(255), comment='Image file type')
    create_time = Column(DateTime, default=datetime.now, comment='Creation time')
    success = Column(Boolean, comment='Explain success')

    def __repr__(self):
        return f'<CaptchaModel(file_id="{self.file_id}",category_id="{self.category_id}",' \
               f'file_type="{self.file_type}",success="{self.success}")>'
