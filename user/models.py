import os

from django.db import models
from django.core.files import File
from django.contrib.auth.models import AbstractUser

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

    def is_master(self):
        """проверяет является ли пользователь мастером"""
        return True if self.masterusermodel_set.all().first() else False

    def master_data(self):
        """данные пользователя если он мастер"""
        return self.masterusermodel_set.all()

    def get_user_activity_by_works(self, offset=0, limit=10):
        """возвращает все комментарии пользователя по работам по лимиту"""
        return self.ratingwork_set.all()[offset:limit]

    def get_user_activity_by_masters(self, offset=0, limit=10):
        """возвращает все комментарии пользователя по мастерам"""
        return self.ratingmaster_set.all()[offset:limit]
