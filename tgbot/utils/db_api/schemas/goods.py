from sqlalchemy import Column, Integer, String, Text, sql, ForeignKey

from tgbot.utils.db_api.db_gino import BaseModel


class Category(BaseModel):
    __tablename__ = 'tgbot_category'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), index=True)
    description = Column(Text)
    slug = Column(String(160), unique=True)

    query: sql.Select


class Subcategory(BaseModel):
    __tablename__ = 'tgbot_subcategory'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), index=True)
    description = Column(Text)
    slug = Column(String(160), unique=True)
    category_id = Column(Integer, ForeignKey('tgbot_category.id'))

