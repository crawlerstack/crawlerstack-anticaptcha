"""DB"""
import logging

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from crawlerstack_anticaptcha.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=settings.SHOW_SQL, future=True)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
BaseModel = declarative_base()

logger = logging.getLogger(__name__)
