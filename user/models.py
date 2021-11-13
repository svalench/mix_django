import os

from django.contrib.auth.models import AbstractUser
from django.core.files import File
from django.db import models

from product.models import Product


class User(AbstractUser):
    """
        Расширение стандартного класа пользовтаеля своим

     Attributes
    =======
    - sex - пол
    - location - место проживания
    - birth_date - дата рождения
    - img - изображение, загруженное пользователем

     Methods
    ==========

    -

    """
    SEX_CHOICE = (
        (0, "Неопределен"),
        (1, "Мужской"),
        (2, "Женский"),
    )
    email = models.EmailField(unique=True, db_index=True)
    username = models.CharField(max_length=40, unique=False, default='', db_index=True)
    sex = models.IntegerField('пол', null=True, default=0, choices=SEX_CHOICE)
    location = models.CharField("адрес", max_length=30, null=True, blank=True, db_index=True)
    city = models.CharField("город", max_length=150, null=True, blank=True, db_index=True)
    country = models.CharField("страна", max_length=150, default='Беларусь', null=True, blank=True, db_index=True)
    region = models.CharField("регино", max_length=150, null=True, blank=True, db_index=True)
    birth_date = models.DateField("дата рождения", null=True, blank=True)
    img = models.ImageField(max_length=25500, null=True, blank=True, upload_to='user_images')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        if self.first_name != "":
            result = "{} {}".format(self.first_name, self.last_name)
        else:
            result = self.username
        return result

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'пользователи'

    def get_remote_image(self, url):
        """сохраняет фотку по url"""
        img = NamedTemporaryFile(delete=True)
        img.write(urlopen(url).read())
        img.flush()
        filename, file_extension = os.path.splitext(url)
        if file_extension != '.com':
            self.img.save(f"user_{self.pk}{file_extension}", File(img))
            self.save()


class ProductCounts(models.Model):
    product = models.ForeignKey(Product, verbose_name='продукт', null=True, on_delete=models.SET_NULL)
    count = models.IntegerField('количество продуктов', db_index=True, null=True, default=0, blank=True)
    date_add = models.DateTimeField('дата добавления', auto_now_add=True)
    date_upd = models.DateTimeField('дата обновления', auto_now=True)


class Carts(models.Model):
    """Корзина заказов"""
    user_name = models.CharField('название', max_length=255, db_index=True)
    user_email = models.CharField('почта', max_length=255, db_index=True)
    user_phone = models.CharField('телефон', max_length=255, db_index=True)
    date_add = models.DateTimeField('дата добавления', auto_now_add=True)
    date_upd = models.DateTimeField('дата обновления', auto_now=True)
    products = models.ManyToManyField(Product)
    list_products = models.ManyToManyField(ProductCounts, verbose_name='список продукт')


