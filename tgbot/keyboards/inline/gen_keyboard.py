from decimal import Decimal

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.keyboards.inline.callback_datas import gen_buy_callback, liked_product, navigate_callback, gen_edit_callback,\
    gen_pag_edit_call, gen_pagination_callback
from tgbot.utils.db_api import quick_commands

# class ProductInlineKeyboard:
#     def __init__(self):
#         self.keyboard = InlineKeyboardMarkup(row_width=3)
#
#     def add(self, part: InlineKeyboardButton) -> None:
#         self.keyboard.add(part)
#
#     def insert(self, part: InlineKeyboardButton) -> None:
#         self.keyboard.insert(part)
#
#     def get_keyboard(self) -> InlineKeyboardMarkup:
#         return self.keyboard
#
#
# class Builder(ABC):
#
#     @property
#     @abstractproperty
#     def product(self) -> None:
#         pass
#
#     @abstractmethod
#     def set_data(self, data: dict) -> None:
#         pass
#
#     @abstractmethod
#     def produce_buy_button(self) -> None:
#         pass
#
#     @abstractmethod
#     def produce_edit_button(self) -> None:
#         pass
#
#     @abstractmethod
#     def produce_like_button(self) -> None:
#         pass
#
#     @abstractmethod
#     def produce_cart_button(self) -> None:
#         pass
#
#     @abstractmethod
#     def produce_back_button(self) -> None:
#         pass
#
#     @abstractmethod
#     def produce_again_button(self) -> None:
#         pass
#
#
# class KeyboardBuilder(Builder):
#     def __init__(self):
#         self.reset()
#
#     def reset(self) -> None:
#         self._inlinekb = ProductInlineKeyboard()
#
#     @property
#     def product(self) -> ProductInlineKeyboard:
#         inline_kb = self._inlinekb
#         self.reset()
#         return inline_kb
#
#     def set_data(self, data: dict):
#         self._data = data
#         self.product_id = str(data["product_info"].pop("product_id"))
#         self.product_title = data["product_info"].pop("product_title")
#         self.product_price = data["product_info"].pop("product_price")
#         self.category_id = data["product_info"].pop("category_id")
#         self.subcategory_name = data["product_info"].pop("subcategory_name")
#         self.liked_product = data["product_info"]["is_liked"]
#
#     def cart_total_price(self, product_list: dict):
#         total = 0
#         for key in product_list.keys():
#             price = product_list[key]["price"]
#             quantity = product_list[key]["quantity"]
#             total += Decimal(price) * quantity
#         return total
#
#     def produce_buy_button(self) -> None:
#         callback_data = gen_buy_callback(product_id=self.product_id, product_price=self.product_price,
#                                          category_id=self.category_id)
#         if self.product_id not in self._data["products"].keys() or \
#                 self._data['products'][self.product_id]["quantity"] == 0:
#             product_name = "Купить " + f'"{self.product_title}"' + "  " + self.product_price + "$"
#         else:
#             quantity = self._data["products"][self.product_id]["quantity"]
#             product_name = f"{quantity} шт. | " + "Купить " + f'"{self.product_title}"' + "  " + self.product_price + "$"
#         self._inlinekb.insert(InlineKeyboardButton(text=product_name, callback_data=callback_data))
#
#     def produce_edit_button(self) -> None:
#         quantity = self._data["products"][self.product_id]["quantity"]
#         self._inlinekb.add(InlineKeyboardButton(text="-1", callback_data=gen_edit_callback(product_id=self.product_id,
#                                                                                            reduce=True, edit=True)))
#         self._inlinekb.insert(InlineKeyboardButton(text="✏" + str(quantity) + "шт.",
#                                                    callback_data=gen_edit_callback(product_id=self.product_id,
#                                                                                    edit=True)))
#         self._inlinekb.insert(
#             InlineKeyboardButton(text="+1", callback_data=gen_edit_callback(product_id=self.product_id,
#                                                                             add=True, edit=True)))
#
#     def produce_like_button(self) -> None:
#         if self.product_id not in self._data['liked_products']:
#             text = "❤"
#             liked_callback = liked_product.new(add=True, delete=False, product_id=self.product_id)
#         else:
#             text = "💘"
#             liked_callback = liked_product.new(add=False, delete=True, product_id=self.product_id)
#         self._inlinekb.add(InlineKeyboardButton(text=text, callback_data=liked_callback))
#
#     def produce_cart_button(self) -> None:
#         self._inlinekb.insert(
#             InlineKeyboardButton(text="🛒 " + str(self.cart_total_price(self._data["products"])) + "$",
#                                  callback_data="show_cart"))
#
#     def produce_again_button(self) -> None:
#         again_text = self.subcategory_name if not bool(self.liked_product) else "💘 Избранное"
#         self._inlinekb.insert(InlineKeyboardButton(text="Еще " + again_text,
#                                                    switch_inline_query_current_chat=again_text))
#
#     def produce_back_button(self) -> None:
#         self._inlinekb.add(InlineKeyboardButton(text="◀ Назад",
#                                                 callback_data=navigate_callback(level=1, category_id=self.category_id)))
#
#
# class Director:
#     def __init__(self) -> None:
#         self._builder = None
#
#     @property
#     def builder(self) -> Builder:
#         return self._builder
#
#     @builder.setter
#     def builder(self, main_builder: Builder) -> None:
#         self._builder = main_builder
#
#     def build_product_kb(self, data: dict) -> None:
#         self.builder.set_data(data=data)
#         self.builder.produce_buy_button()
#         self.builder.produce_like_button()
#         self.builder.produce_cart_button()
#         self.builder.produce_back_button()
#         self.builder.produce_again_button()
#
#     def build_edit_kb(self, data: dict) -> None:
#         self.builder.set_data(data=data)
#         self.builder.produce_edit_button()
#         self.builder.produce_like_button()
#         self.builder.produce_cart_button()
#         self.builder.produce_back_button()
#         self.builder.produce_again_button()
#
#
# director = Director()
# builder = KeyboardBuilder()
# director.builder = builder

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
    def __init__(self,  data: dict, page: int = 1):
        self.keyboard = InlineKeyboardMarkup(row_width=3)
        self.data = data
        self.page = page
        self.max_page = len(data['products'].keys())
        self.idx_product_ids = dict(enumerate(data['products'].keys(), start=1))
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
                                                                                             edit=True, page=self.page)))
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
        self.keyboard.add(InlineKeyboardButton(text="✅ Завершить редактирование", callback_data="test"))

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
        x = cls(product=product, data=data)
        return x

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
        if str(self.product.id) not in self.data["products"].keys() or \
                self.data['products'][str(self.product.id)]["quantity"] == 0:
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
