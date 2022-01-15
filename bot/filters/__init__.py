from bot.loader import dp
# from .is_admin import AdminFilter
from .inline_text_filter import IsSubcategoryName

if __name__ == "bot.filters":
    dp.filters_factory.bind(IsSubcategoryName)
