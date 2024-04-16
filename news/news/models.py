from scrapy.utils.project import get_project_settings
from sqlalchemy import (
    create_engine,
    Column,
    BigInteger,
    Integer,
    String,
    DateTime,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class News(Base):
    __tablename__ = "news"

    id = Column(BigInteger, primary_key=True)
    title = Column(String(255))
    author = Column(String(255))
    published_at = Column(DateTime)
    clicks = Column(Integer)
    content = Column(Text)
    image_urls = Column(Text)


engine = create_engine(get_project_settings().get("DATABASE_URL"))
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
