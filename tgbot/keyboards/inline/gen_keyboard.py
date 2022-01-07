from decimal import Decimal
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.keyboards.inline.callback_datas import gen_buy_callback, liked_product, navigate_callback, gen_edit_callback, \
    gen_pag_edit_call, gen_pagination_callback
from tgbot.utils.db_api import quick_commands

#  =================Cart Edit KB ===================
cart_edit_kb = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text="✏ Редактировать", callback_data="edit_cart"),
        InlineKeyboardButton(text="❌ Очистить", callback_data="wipe_cart")
    ],
    [
        InlineKeyboardButton(text="✅  Оформить заказ", callback_data="order")
    ]
])


#  ==================================================


class CartKeyboardGen:
    def __init__(self, data: dict, page: int = 1):
        self.keyboard = InlineKeyboardMarkup(row_width=3)
        self.data = data
        # =============Paging on card edit====================#
        self.page = page
        self.max_page = len(data['products'].keys())
        self.idx_product_ids = dict(enumerate(data['products'].keys(), start=1))
        # ====================================================#
        self.product_id = self.idx_product_ids[page]
        self.product = data["products"][self.product_id]
        self.quantity = self.product['quantity']

    def produce_edit_button(self):
        text = "✏ " + str(self.quantity) + " шт. |" + self.product['price'] + " " + self.product['title']
        self.keyboard.add(InlineKeyboardButton(text=text, callback_data=gen_pagination_callback(page=self.page,
                                                                                                edit=True)))

    def produce_edit_quantity(self):
        text = "✏ " + str(self.quantity) + " шт."
        self.keyboard.add((InlineKeyboardButton(text="-1", callback_data=gen_pag_edit_call(product_id=self.product_id,
                                                                                           edit=True, reduce=True,
                                                                                           page=self.page))))

        self.keyboard.insert(InlineKeyboardButton(text=text, callback_data=gen_pag_edit_call(product_id=self.product_id,
                                                                                             edit=True,
                                                                                             page=self.page)))

        self.keyboard.insert(InlineKeyboardButton(text="+1", callback_data=gen_pag_edit_call(product_id=self.product_id,
                                                                                             edit=True, add=True,
                                                                                             page=self.page)))

    def produce_back_button(self):
        back_page = self.page - 1
        if back_page <= 0:
            button = InlineKeyboardButton(text='◀', callback_data=gen_pagination_callback(page=self.max_page))
            self.keyboard.add(button)
            return
        button = InlineKeyboardButton(text='◀', callback_data=gen_pagination_callback(page=back_page))
        self.keyboard.add(button)

    def produce_current_page(self):
        button_text = str(self.page) + "/" + str(self.max_page)
        button = InlineKeyboardButton(text=button_text, callback_data="test")
        self.keyboard.insert(button)

    def produce_next_button(self):
        next_page = self.page + 1
        if next_page > self.max_page:
            button = InlineKeyboardButton(text='➡', callback_data=gen_pagination_callback(page=1))
            self.keyboard.insert(button)
            return
        button = InlineKeyboardButton(text='➡', callback_data=gen_pagination_callback(page=next_page))
        self.keyboard.insert(button)

    def produce_end_editing(self):
        self.keyboard.add(InlineKeyboardButton(text="✅ Завершить редактирование", callback_data="end_edit"))

    def build_pagination_keyboard(self) -> InlineKeyboardMarkup:
        self.produce_edit_button()
        self.produce_back_button()
        self.produce_current_page()
        self.produce_next_button()
        self.produce_end_editing()
        return self.keyboard

    def build_edit_keyboard(self) -> InlineKeyboardMarkup:
        self.produce_edit_quantity()
        self.produce_back_button()
        self.produce_current_page()
        self.produce_next_button()
        self.produce_end_editing()
        return self.keyboard


class KeyboardGen:
    def __init__(self, product, data: dict):
        self.keyboard = InlineKeyboardMarkup(row_width=3)
        self.product = product
        self.data = data
        self.is_liked = self.data["product_info"]["is_liked"]

    @classmethod
    async def from_product_id(cls, product_id: int, data: dict):
        product = await quick_commands.get_product(product_id)
        instance = cls(product=product, data=data)
        return instance

    @staticmethod
    def cart_total_price(product_list: dict):
        total = 0
        for key in product_list.keys():
            price = product_list[key]["price"]
            quantity = product_list[key]["quantity"]
            total += Decimal(price) * quantity
        if not total:
            return "0.00"
        return total

    def produce_buy_button(self) -> None:
        callback_data = gen_buy_callback(product_id=self.product.id, product_price=str(self.product.price),
                                         category_id=self.product.parent.category_id)
        if str(self.product.id) not in self.data["products"].keys():
            product_name = "Купить " + f'"{self.product.title}"' + "  " + str(self.product.price) + "$"
        else:
            quantity = self.data["products"][str(self.product.id)]["quantity"]
            product_name = f"{quantity} шт. | " + "Купить " + f'"{self.product.title}"' + "  " + str(
                self.product.price) + "$"
        self.keyboard.insert(InlineKeyboardButton(text=product_name, callback_data=callback_data))

    def produce_edit_button(self) -> None:
        quantity = self.data["products"][str(self.product.id)]["quantity"]
        self.keyboard.add(InlineKeyboardButton(text="-1", callback_data=gen_edit_callback(product_id=self.product.id,
                                                                                          reduce=True, edit=True)))
        self.keyboard.insert(InlineKeyboardButton(text="✏" + str(quantity) + "шт.",
                                                  callback_data=gen_edit_callback(product_id=self.product.id,
                                                                                  edit=True)))
        self.keyboard.insert(
            InlineKeyboardButton(text="+1", callback_data=gen_edit_callback(product_id=self.product.id,
                                                                            add=True, edit=True)))

    def produce_like_button(self) -> None:
        if self.product.id not in self.data['liked_products']:
            text = "❤"
            liked_callback = liked_product.new(add=True, delete=False, product_id=self.product.id)
        else:
            text = "💘"
            liked_callback = liked_product.new(add=False, delete=True, product_id=self.product.id)
        self.keyboard.add(InlineKeyboardButton(text=text, callback_data=liked_callback))

    def produce_cart_button(self) -> None:
        self.keyboard.insert(
            InlineKeyboardButton(text="🛒 " + str(self.cart_total_price(self.data["products"])) + "$",
                                 callback_data="show_cart"))

    def produce_again_button(self) -> None:
        again_text = self.product.parent.tg_name if not self.is_liked else "💘 Избранное"
        self.keyboard.insert(InlineKeyboardButton(text="Еще " + again_text,
                                                  switch_inline_query_current_chat=again_text))

    def produce_back_button(self) -> None:
        self.keyboard.add(InlineKeyboardButton(text="◀ Назад",
                                               callback_data=navigate_callback(level=1,
                                                                               category_id=self.product.parent.category_id)))

    def build_product_kb(self) -> InlineKeyboardMarkup:
        self.produce_buy_button()
        self.produce_like_button()
        self.produce_cart_button()
        self.produce_back_button()
        self.produce_again_button()
        return self.keyboard

    def build_edit_kb(self) -> InlineKeyboardMarkup:
        self.produce_edit_button()
        self.produce_like_button()
        self.produce_cart_button()
        self.produce_back_button()
        self.produce_again_button()
        return self.keyboard
