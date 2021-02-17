from tgbot.utils.db_api.db_gino import db
from tgbot.utils.db_api.schemas.goods import Category, Subcategory


async def show_category():
    categories = await Category.query.gino.all()
    return categories


async def show_subcategory():
    subcategories = await Subcategory.query.gino.all()
    return subcategories
