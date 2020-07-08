
from django.contrib.gis.geos import Point
from rest_framework import serializers
from rest_framework_gis.fields import GeometryField

from .models import Transport, TransportData

class TransportSerializer(serializers.ModelSerializer):
    """
    id_user_transport = serializers.IntegerField()
    # id_user = serializers.IntegerField()
    name = serializers.CharField(max_length=120)
    info = serializers.CharField()
    imei = serializers.CharField(max_length=20)
    licenseplate = serializers.CharField(max_length=20)
    """
    class Meta:
        model = Transport
        fields = ('id_user_transport', 'id_user', 'name', 'info', 'imei', 'licenseplate',)


class TransportDataSerializer(serializers.ModelSerializer):
    """
    # id_user_transport_data = serializers.IntegerField()
    id = serializers.IntegerField()
    id_user_transport = serializers.RelatedField(read_only=True)
    altitude = serializers.IntegerField()
    when_added = serializers.DateTimeField()
    speed = serializers.DecimalField(max_digits=7, decimal_places=2)
    satellite = serializers.IntegerField()
    flags1 = serializers.IntegerField()
    point = GeometryField()
    """

    point = GeometryField()

    class Meta:
        model = TransportData
        fields = ['id', 'id_user_transport', 'altitude', 'when_added', 'speed', 'point', 'satellite', ]


class TrackDataSerializer(serializers.ModelSerializer):

    point = GeometryField()

    class Meta:
        model = TransportData
        fields = ['id', 'id_user_transport', 'altitude', 'when_added', 'speed', 'point', 'satellite', ]
