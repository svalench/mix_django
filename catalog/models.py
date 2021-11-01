from django.db import models


class BaseModel(models.Model):
    """Базовая модель для сущностей"""
    name = models.CharField('название', max_length=255, db_index=True)
    img = models.ImageField('картинка', default='/img/noimg.png', blank=True)
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


class FirstCategory(BaseModel):
    """модель главной категории"""
    weight_in_menu = models.IntegerField('Вес меню', default=0, null=True, blank=True)
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class SecondCategory(BaseModel):
    """модель вторичной категории"""
    parent = models.ForeignKey(FirstCategory, related_name='child', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class DocumentsCard(models.Model):
    """модель для сертификатов"""
    name = models.CharField('название', max_length=255, db_index=True)
    parent = models.ForeignKey(FirstCategory, on_delete=models.SET_NULL, null=True, blank=True)
    doc = models.FileField('Сертификат', upload_to='certificates', blank=True)
    date_add = models.DateTimeField('дата добавления', auto_now_add=True)
    date_upd = models.DateTimeField('дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Сертификат'
        verbose_name_plural = 'Сертификаты'
