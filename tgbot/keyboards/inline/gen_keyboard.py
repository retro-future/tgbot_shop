from abc import ABC, abstractmethod, abstractproperty
from decimal import Decimal

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.keyboards.inline.callback_datas import gen_buy_callback, liked_product, navigate_callback, gen_edit_callback


class ProductInlineKeyboard:
    def __init__(self):
        self.keyboard = InlineKeyboardMarkup(row_width=3)

    def add(self, part: InlineKeyboardButton) -> None:
        self.keyboard.add(part)

    def insert(self, part: InlineKeyboardButton) -> None:
        self.keyboard.insert(part)

    def get_keyboard(self) -> InlineKeyboardMarkup:
        return self.keyboard


class Builder(ABC):

    @property
    @abstractproperty
    def product(self) -> None:
        pass

    @abstractmethod
    def set_data(self, data: dict) -> None:
        pass

    @abstractmethod
    def produce_buy_button(self) -> None:
        pass

    @abstractmethod
    def produce_edit_button(self) -> None:
        pass

    @abstractmethod
    def produce_like_button(self) -> None:
        pass

    @abstractmethod
    def produce_cart_button(self) -> None:
        pass

    @abstractmethod
    def produce_back_button(self) -> None:
        pass

    @abstractmethod
    def produce_again_button(self) -> None:
        pass


class KeyboardBuilder(Builder):
    def __init__(self):
        self.reset()

    def reset(self) -> None:
        self._inlinekb = ProductInlineKeyboard()

    @property
    def product(self) -> ProductInlineKeyboard:
        inline_kb = self._inlinekb
        self.reset()
        return inline_kb

    def set_data(self, data: dict):
        self._data = data
        self.product_id = str(data["product_info"]["product_id"])
        self.product_title = data["product_info"]["product_title"]
        self.product_price = data["product_info"]["product_price"]
        self.category_id = data["product_info"]["category_id"]
        self.subcategory_name = data["product_info"]["subcategory_name"]
        self.liked_product = data["product_info"]["is_liked"]

    def total_func(self, product_list: dict):
        total = 0
        for key in product_list.keys():
            price = product_list[key]["price"]
            quantity = product_list[key]["quantity"]
            total += (Decimal(price) * quantity)
        return total

    def produce_buy_button(self) -> None:
        callback_data = gen_buy_callback(product_id=self.product_id, product_price=self.product_price,
                                         category_id=self.category_id)
        if self.product_id not in self._data["products"].keys():
            product_name = "Купить " + f'"{self.product_title}"' + "  " + str(self.product_price) + "$"
        else:
            quantity = self._data["products"][self.product_id]["quantity"]
            product_name = f"{quantity} шт. | " + "Купить " + f'"{self.product_title}"' + "  " + str(
                self.product_price) + "$"
        self._inlinekb.insert(InlineKeyboardButton(text=product_name, callback_data=callback_data))

    def produce_edit_button(self) -> None:
        quantity = self._data["products"][self.product_id]["quantity"]
        self._inlinekb.add(InlineKeyboardButton(text="-1", callback_data=gen_edit_callback(product_id=self.product_id,
                                                                                           reduce=True, edit=True)))
        self._inlinekb.insert(InlineKeyboardButton(text="✏" + str(quantity) + "шт.",
                                                   callback_data=gen_edit_callback(product_id=self.product_id,
                                                                                   edit=True)))
        self._inlinekb.insert(InlineKeyboardButton(text="+1", callback_data=gen_edit_callback(product_id=self.product_id,
                                                                                              add=True, edit=True)))

    def produce_like_button(self) -> None:
        if self.product_id not in self._data['liked_products']:
            text = "❤"
            liked_callback = liked_product.new(add=True, delete=False, product_id=self.product_id)
        else:
            text = "💘"
            liked_callback = liked_product.new(add=False, delete=True, product_id=self.product_id)
        self._inlinekb.add(InlineKeyboardButton(text=text, callback_data=liked_callback))

    def produce_cart_button(self) -> None:
        self._inlinekb.insert(InlineKeyboardButton(text="🛒 " + str(self.total_func(self._data["products"])) + "$",
                                                   callback_data="show_cart"))

    def produce_again_button(self) -> None:
        again_text = self.subcategory_name if not bool(self.liked_product) else "💘 Избранное"
        self._inlinekb.insert(InlineKeyboardButton(text="Еще " + again_text,
                                                   switch_inline_query_current_chat=again_text))

    def produce_back_button(self) -> None:
        self._inlinekb.add(InlineKeyboardButton(text="◀ Назад",
                                                callback_data=navigate_callback(level=1, category_id=self.category_id)))


class Director:
    def __init__(self) -> None:
        self._builder = None

    @property
    def builder(self) -> Builder:
        return self._builder

    @builder.setter
    def builder(self, main_builder: Builder) -> None:
        self._builder = main_builder

    def build_product_kb(self, data: dict) -> None:
        self.builder.set_data(data=data)
        self.builder.produce_buy_button()
        self.builder.produce_like_button()
        self.builder.produce_cart_button()
        self.builder.produce_back_button()
        self.builder.produce_again_button()

    def build_edit_kb(self, data: dict) -> None:
        self.builder.set_data(data=data)
        self.builder.produce_edit_button()
        self.builder.produce_like_button()
        self.builder.produce_cart_button()
        self.builder.produce_back_button()
        self.builder.produce_again_button()


director = Director()
builder = KeyboardBuilder()
director.builder = builder
