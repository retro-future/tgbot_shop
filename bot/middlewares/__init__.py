from bot.loader import dp
from .state_check import CheckState, ProductInfo
from .sentinel import IsRegistered
from .throttling import ThrottlingMiddleware

if __name__ == "bot.middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(CheckState())
    dp.middleware.setup(ProductInfo())
    dp.middleware.setup(IsRegistered())
