from django.contrib import admin

from tgbot.models import Category, Subcategory, Product, TgUser


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
    list_display = ("id", "user_id", "name", "phone_number", "created_at", "updated_at")
    list_display_links = ("user_id", "name")