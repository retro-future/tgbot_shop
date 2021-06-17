from aiogram import types
from aiogram.dispatcher import FSMContext
from tgbot.keyboards.inline.gen_keyboard import KeyboardGen
from tgbot.utils.db_api.db_gino import db
from tgbot.utils.db_api.schemas.goods import SubcategoryGino, CategoryGino, ProductGino, TgUserGino


async def get_parent_child():  # get child model with children attribute
    query = SubcategoryGino.outerjoin(CategoryGino).select()
    parent = await query.gino.load(CategoryGino.distinct(CategoryGino.id).load(children=SubcategoryGino)).all()
    return parent


async def get_child_parent(category_id: int):
    async with db.transaction():
        query = SubcategoryGino.load(parent=CategoryGino).where(CategoryGino.id == category_id)
        result = await query.gino.all()
    return result


async def get_product(product_id: int):
    async with db.transaction():
        product = ProductGino.load(parent=SubcategoryGino)
        result = await product.where(ProductGino.id == product_id).gino.first()
    return result


async def get_liked_product(liked_products_id: list, state: FSMContext):
    query_answer = []
    async with db.transaction():
        for product_id in liked_products_id:
            db_query = ProductGino.load(parent=SubcategoryGino)
            product = await db_query.where(ProductGino.id == product_id).gino.first()
            async with state.proxy() as state_data:
                state_data["product_info"] = {"is_liked": 1}
                markup = KeyboardGen(product=product, data=state_data).build_product_kb()
            query_answer.append(
                types.InlineQueryResultArticle(
                    id=str(product.id),
                    title=product.title,
                    input_message_content=types.InputTextMessageContent(
                        message_text=f"<a href='{product.image}'>{product.title}</a>", parse_mode="HTML"
                    ),
                    reply_markup=markup,
                    description=str(product.price),
                    thumb_url=product.image,
                )
            )
    return query_answer


async def show_products_inline(subcategory_title: str, state: FSMContext, offset: int):
    start = offset
    end = offset + 25
    query_answer = []
    async with db.transaction():
        query = ProductGino.load(parent=SubcategoryGino).where(SubcategoryGino.tg_name == subcategory_title)
        result = await query.gino.all()
    for product in result[start:end]:
        async with state.proxy() as state_data:
            state_data["product_info"] = {"is_liked": 0}
            keyboard = KeyboardGen(product=product, data=state_data)
            markup = keyboard.build_product_kb()
        query_answer.append(
            types.InlineQueryResultArticle(
                id=str(product.id),
                title=product.title,
                input_message_content=types.InputTextMessageContent(
                    message_text=f"<a href='{product.image}'>{product.title}</a>", parse_mode="HTML"
                ),
                reply_markup=markup,
                description=str(product.price) + "$",
                thumb_url=product.image,
            )
        )
    return query_answer


async def get_user(user_id: int):
    result = await TgUserGino.query.where(TgUserGino.user_id == user_id).gino.first()
    return result


async def show_all_subcategory():
    subcategories = await SubcategoryGino.query.gino.all()
    return subcategories
