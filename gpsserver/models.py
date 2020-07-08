
from django.db import models
from django.contrib.gis.db import models as gis_models
from django.utils import timezone

from users.models import CustomUser


class Transport(models.Model):
    """ модель 'Транспортное средство'/'Терминал' """

    id_user_transport = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, verbose_name="Пользователь")
    name = models.TextField(verbose_name="Наименование")
    info = models.TextField(verbose_name="Информация")
    licenseplate = models.CharField(max_length=20)
    imei = models.CharField(max_length=20)

    class Meta:
        db_table = "tbl_user_transport"
        verbose_name_plural = "Транспортные средства"
        verbose_name = "Транспортное средство"


class TransportData(models.Model):
    """ модель 'Данные Транспортного средства'/'Терминала' """

    # id_user_transport_data = models.AutoField(primary_key=True)
    id = models.AutoField(primary_key=True)
    id_user_transport = models.ForeignKey(Transport, on_delete=models.PROTECT, verbose_name="Транспортное средство")
    point = gis_models.GeometryField(geography=True, verbose_name="Точка на карте", blank=True, null=True, default=None)
    altitude = models.IntegerField(verbose_name="Высота над уровнем моря", blank=True, null=True, default=None)
    when_added = models.DateTimeField(default=timezone.now, verbose_name="Дата-время добавления записи")
    speed = models.DecimalField(verbose_name="Скорость", max_digits=7, decimal_places=2, blank=True, null=True, default=None)
    satellite = models.IntegerField(verbose_name="Спутники", blank=True, null=True, default=None)
    flags1 = models.IntegerField(verbose_name="Флаги 1", blank=True, null=True, default=None)

    class Meta:
        db_table = "tbl_data"
        verbose_name_plural = "Данные транспортных средств"
        verbose_name = "Данные транспортного средства"
