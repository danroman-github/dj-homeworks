from rest_framework import serializers
from .models import Sensor, Measurement


class MeasurementSerializer(serializers.ModelSerializer):
    """Сериализатор для измерений температуры"""
    sensor = serializers.PrimaryKeyRelatedField(queryset=Sensor.objects.all())

    class Meta:
        model = Measurement
        fields = ['sensor', 'temperature', 'created_at']


class SensorSerializer(serializers.ModelSerializer):
    """Сериализатор для датчиков с измерениями"""
    measurements = MeasurementSerializer(
        read_only=True,
        many=True,
        source='measurements.all',
        help_text='Список измерений для этого датчика'
    )

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description', 'measurements']
