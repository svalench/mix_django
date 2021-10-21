from django.db import models

from catalog.models import SecondCategory


class BaseModel(models.Model):
    """Базовая модель для сущностей"""
    name = models.CharField('название', max_length=255, db_index=True)
    description = models.TextField('комментарий', max_length=12000, blank=True, default='', null=True, db_index=True)
    date_add = models.DateTimeField('дата добавления', auto_now_add=True)
    date_upd = models.DateTimeField('дата обновления', auto_now=True)

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "name__icontains", "description__icontains",)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Units(BaseModel):
    """единицы измерения"""

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'


class Characteristics(BaseModel):
    """Характеристика товара"""
    weight_in_menu = models.IntegerField('Вес для сортировки', default=0, null=True, blank=True)
    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'


class CharacteristicValue(models.Model):
    """модель значений характеристик"""
    parent = models.ForeignKey(Characteristics, related_name='charac_value', on_delete=models.CASCADE, verbose_name="название характеристики")
    value = models.CharField('значение', max_length=255, db_index=True)
    units = models.ForeignKey(Units, on_delete=models.CASCADE, verbose_name="единицы измерения")
    date_add = models.DateTimeField('дата добавления', auto_now_add=True)
    date_upd = models.DateTimeField('дата обновления', auto_now=True)

    def __str__(self):
        return f'{self.value}   {self.units.name}  {self.parent.name}'

    class Meta:
        verbose_name = 'Значение характеристики'
        verbose_name_plural = 'Значения характеристик'

class Filters(BaseModel):
    """модель фильтров для карточек товара"""
    class Meta:
        verbose_name = 'Фильтр'
        verbose_name_plural = 'Фильтра'


class FiltersValue(models.Model):
    """модель значений фильтров"""
    parent = models.ForeignKey(Filters, related_name='filter_value', on_delete=models.CASCADE, verbose_name="название фильтра")
    value = models.CharField('значение', max_length=255, db_index=True)
    units = models.ForeignKey(Units, on_delete=models.CASCADE, verbose_name="единицы измерения")
    date_add = models.DateTimeField('дата добавления', auto_now_add=True)
    date_upd = models.DateTimeField('дата обновления', auto_now=True)

    def __str__(self):
        return f'{self.parent.name} = {self.value}  {self.units.name}  {self.parent.name}'

    class Meta:
        verbose_name = 'Значение фильтра'
        verbose_name_plural = 'Значения фильтров'


class ProductsImages(models.Model):
    """модель изображения продукта"""
    img = models.ImageField('картинка')
    product = models.ForeignKey('CardProduct', related_name='images', on_delete=models.CASCADE, verbose_name="продукт")
    date_add = models.DateTimeField('дата добавления', auto_now_add=True)
    date_upd = models.DateTimeField('дата обновления', auto_now=True)

    def __str__(self):
        return f'{self.product.name} {self.id}'

    class Meta:
        verbose_name = 'Изображение продукта'
        verbose_name_plural = 'Изображения продуктов'


class CardProduct(BaseModel):
    """модель карточки товара"""
    img = models.ImageField( default='/img/noimg.png', blank=True, verbose_name="изображение")
    filters = models.ManyToManyField(FiltersValue, related_name='filter', blank=True, null=True, verbose_name="фильтр")
    category = models.ForeignKey(SecondCategory, related_name='category', on_delete=models.SET_NULL, verbose_name="категория", blank=True, null=True)
    class Meta:
        verbose_name = 'Карточка продукта'
        verbose_name_plural = 'Карточки продукта'

    def related_label(self):
        return "%s (%s)" % (self.name, self.id)


class Product(BaseModel):
    """модель товара"""
    parent = models.ForeignKey(CardProduct, related_name='child', verbose_name="карточка продукта", on_delete=models.CASCADE, blank=True, null=True)
    article = models.CharField('артикль', max_length=255, db_index=True)
    characteristics = models.ManyToManyField(CharacteristicValue, related_name='characteristic', verbose_name="характеристики", blank=True, null=True)
    count = models.IntegerField('количество', default=0, blank=True)
    weight = models.DecimalField('вес', null=True, default=0.0, db_index=True, blank=True,
                                 max_digits=12, decimal_places=2)
    price = models.DecimalField('цена', blank=True, default=0.0, max_digits=32,
                                decimal_places=2, null=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

