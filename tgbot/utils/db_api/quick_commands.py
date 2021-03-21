import gino

from tgbot.data import config
import asyncio

from tgbot.utils.db_api.db_gino import db
from tgbot.utils.db_api.schemas.goods import Subcategory, Category, Product


async def get_parent_child():  # get child model with children attribute
    query = Subcategory.outerjoin(Category).select()
    parent = await query.gino.load(Category.distinct(Category.id).load(add_child=Subcategory)).all()
    return parent


async def get_child_parent(category_id: int):
    async with db.transaction():
        query = Subcategory.load(parent=Category).where(Category.id == category_id)
        result = await query.gino.all()
    return result


async def show_all_products(subcategory_id: int):
    async with db.transaction():
        query = Product.load(parent=Subcategory).where(Subcategory.id == subcategory_id)
        result = await query.gino.all()
    return result


async def show_product():
    products = await Product.query.gino.all()
    return products


async def show_products_inline(subcategory_title: str):
    async with db.transaction():
        query = Product.load(parent=Subcategory).where(Subcategory.tg_name == subcategory_title)
        result = await query.gino.all()
    return result


async def show_all_subcategory():
    subcategories = await Subcategory.query.gino.all()
    return subcategories


async def test():
    engine = await gino.create_engine(config.POSTGRES_URI)
    db.bind = engine
    result = await show_all_subcategory()
    for i in result:
        print(i.tg_name)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
