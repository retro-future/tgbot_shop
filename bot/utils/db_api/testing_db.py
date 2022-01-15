import asyncio
import gino
from bot.utils.db_api.db_gino import db
from bot.data import config
from bot.utils.db_api.quick_commands import get_user
from bot.utils.db_api.schemas.db_tables import ProductGino


async def test():
    engine = await gino.create_engine(config.POSTGRES_URI)
    db.bind = engine
    # result = await get_parent_child()
    # for i in result:
    #     print(i.children)
    # user = await TgUserGino.get(4)
    # await user.update(name="Ilona").apply()
    product = await ProductGino.query.where(ProductGino.title.ilike("%xiaomi%")).gino.all()
    user = await get_user(92613407)
    for i in product:
        print(i.title)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
