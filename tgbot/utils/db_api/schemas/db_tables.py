from sqlalchemy import Column, Integer, String, Text, sql, ForeignKey, Boolean, VARCHAR, DECIMAL, DateTime
from tgbot.utils.db_api.db_gino import BaseModel, TimedBaseModel
from sqlalchemy.sql import func


class CategoryGino(BaseModel):
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
    def children(self, child):
        self._children.add(child)


class SubcategoryGino(BaseModel):
    __tablename__ = 'tgbot_subcategory'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), index=True)
    tg_name = Column(String(200))
    description = Column(Text)
    slug = Column(String(160), unique=True)
    category_id = Column(Integer, ForeignKey('tgbot_category.id'))


class ProductGino(BaseModel):
    __tablename__ = 'tgbot_product'
    id = Column(Integer, primary_key=True)
    title = Column(VARCHAR(150), index=True)
    description = Column(Text)
    price = Column(DECIMAL(precision=2, scale=10))
    available = Column(Boolean)
    image = Column(VARCHAR(100))
    image_file_id = Column(VARCHAR(200), index=True)
    subcategory_id = Column(Integer, ForeignKey('tgbot_subcategory.id'))


class TgUserGino(TimedBaseModel):
    __tablename__ = 'tgbot_tguser'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True, unique=True)
    name = Column(VARCHAR(50))


class OrdersGino(TimedBaseModel):
    __tablename__ = 'tgbot_orders'
    id = Column(Integer, primary_key=True)
    is_paid = Column(Boolean, default=False)
    tg_user_id = Column(Integer, ForeignKey('tgbot_tguser.id'))
    order_number = Column(VARCHAR(25), index=True, unique=True)
    total_price = Column(DECIMAL(precision=2, scale=10))


class OrderProductGino(TimedBaseModel):
    __tablename__ = 'tgbot_orderproduct'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("tgbot_orders.id"))
    product_id = Column(Integer, ForeignKey("tgbot_product.id"))
    quantity = Column(Integer, default=0)
    single_price = Column(DECIMAL(precision=2, scale=10))


class UserAddresses(TimedBaseModel):
    __tablename__ = 'tgbot_useraddresses'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('tgbot_tguser.id'))
    address = Column(VARCHAR(150))
