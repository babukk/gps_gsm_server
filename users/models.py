
from django.db import models

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
# from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager


class CustomCountry(models.Model):
    id_country = models.AutoField(primary_key=True)
    code_country = models.CharField('Код страны', max_length=3)

    def __str__(self):
        return self.code_country

    class Meta:
        db_table = "tbl_country"


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """  Модель 'Пользователи/Учётные записи' """

    # Добавляем поля:
    id_user = models.AutoField(primary_key=True)
    login = models.CharField('Имя пользователя', unique=True, db_index=True, max_length=100)
    password = models.CharField('Пароль', max_length=100)
    is_staff = models.BooleanField(default=True)

    # Устанавливаем USERNAME_FIELD, которое определяет уникальный идентификатор для модели User значением username:
    USERNAME_FIELD = 'login'

    # обязательные поля (их пока нет):
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.login


    class Meta:
        ordering = ['login']
        db_table = "tbl_user"
        verbose_name_plural = "Пользователи"
        verbose_name = "Пользователь"


class CustomUserInfo(models.Model):
    id_user_info = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, verbose_name="Пользователь")
    name = models.CharField('Имя/наименование', max_length=100)
    email = models.CharField('email', max_length=100)
    id_country = models.ForeignKey(CustomCountry, on_delete=models.PROTECT, verbose_name="Код страны")

    class Meta:
        db_table = "tbl_user_info"
