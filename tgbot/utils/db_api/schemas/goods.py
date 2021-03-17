from sqlalchemy import Column, Integer, String, Text, sql, ForeignKey, Boolean, VARCHAR, DECIMAL
from tgbot.utils.db_api.db_gino import BaseModel


class Category(BaseModel):
    __tablename__ = 'tgbot_category'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), index=True)
    tg_name = Column(String(200))
    description = Column(Text)
    slug = Column(String(160), unique=True)

    query: sql.select

    def __init__(self, **kw):
        super().__init__(**kw)
        self._children = set()

    @property
    def children(self):
        return self._children

    @children.setter
    def add_child(self, child):
        self._children.add(child)


class Subcategory(BaseModel):
    __tablename__ = 'tgbot_subcategory'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), index=True)
    tg_name = Column(String(200))
    description = Column(Text)
    slug = Column(String(160), unique=True)
    category_id = Column(Integer, ForeignKey('tgbot_category.id'))


class Product(BaseModel):
    __tablename__ = 'tgbot_product'
    id = Column(Integer, primary_key=True)
    title = Column(VARCHAR(150), index=True)
    description = Column(Text)
    price = Column(DECIMAL(precision=2, scale=10))
    available = Column(Boolean)
    image = Column(VARCHAR(100))
    image_file_id = Column(VARCHAR(200), index=True)
    subcategory_id = Column(Integer, ForeignKey('tgbot_subcategory.id'))
