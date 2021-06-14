from django.db import models
from tgbot.utils.get_link_or_id import get_photo_link


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    tg_name = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    slug = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Subcategory(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    tg_name = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    slug = models.SlugField(max_length=160, unique=True)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"


class Product(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    slug = models.SlugField(max_length=160, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    image_file_id = models.CharField(max_length=200, db_index=True, blank=True)
    subcategory = models.ForeignKey(Subcategory, related_name='products', on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        try:
            image_bytes = self.image.read()
            link = get_photo_link(image_bytes)
            self.image = link
            super(Product, self).save(*args, **kwargs)
        except Exception:
            super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class TgUser(models.Model):
    user_id = models.IntegerField(db_index=True, unique=True)
    name = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=60, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user_id)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


# class Orders(models.Model):
#     is_paid = models.BooleanField(default=False)
#     user_id = models.ForeignKey(TgUser, related_name="orders", on_delete=models.PROTECT)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#
# class OrderProduct(models.Model):
#     order_id = models.ForeignKey(Orders, related_name="order_product", on_delete=models.CASCADE)
#     product_id = models.ForeignKey(Product, related_name="order_product", on_delete=models.PROTECT)
#     quantity = models.IntegerField("quantity", default=0)
#     single_price = models.DecimalField(max_digits=10, decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
