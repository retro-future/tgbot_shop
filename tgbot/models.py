from django.db import models
from tgbot.utils.get_link_or_id import get_photo_link


class TimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


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


class TgUser(TimeModel):
    user_id = models.IntegerField(db_index=True, unique=True)
    name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return str(self.user_id)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Orders(TimeModel):
    is_paid = models.BooleanField(default=False)
    tg_user = models.ForeignKey(TgUser, related_name="orders", on_delete=models.PROTECT)
    order_number = models.CharField("Номер Заказа", max_length=25, db_index=True, unique=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderProduct(TimeModel):
    order = models.ForeignKey(Orders, related_name="order_product", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="order_product", on_delete=models.PROTECT)
    quantity = models.IntegerField("quantity", default=0)
    single_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Заказанный продукт"
        verbose_name_plural = "Заказанные продукты"


class UserAddresses(TimeModel):
    user = models.ForeignKey(TgUser, on_delete=models.CASCADE)
    address = models.TextField("Адрес доставки", max_length=150)

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"
