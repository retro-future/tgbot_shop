from django.contrib import admin

from tgbot.models import Category, Subcategory, Product, TgUser, Orders, OrderProduct, UserAddresses


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    list_display_links = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    list_display_links = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "available",)
    list_display_links = ("title",)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "name", "created_at", "updated_at")
    list_display_links = ("user_id", "name")


class OrderProductTabular(admin.TabularInline):
    model = OrderProduct


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ("id", "tg_user", "order_number", "total_price", "is_paid", "created_at", "updated_at")
    list_display_links = ("id", "order_number")
    inlines = [OrderProductTabular]


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "single_price")
    list_display_links = ("order", "product")


@admin.register(UserAddresses)
class UserAddressesAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "address")
    list_display_links = ("user", "address")
