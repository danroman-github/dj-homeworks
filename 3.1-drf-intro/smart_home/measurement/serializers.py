from rest_framework import serializers
from .models import Sensor, Measurement


class MeasurementSerializer(serializers.ModelSerializer):
    """Сериализатор для измерений температуры"""
    sensor = serializers.PrimaryKeyRelatedField(queryset=Sensor.objects.all())
    image_url = serializers.SerializerMethodField(read_only=True)
    image = serializers.ImageField(
        required=False,
        allow_null=True,
        max_length=None,
        use_url=False
    )

    class Meta:
        model = Measurement
        fields = ['sensor', 'temperature', 'created_at', 'image_url', 'image']
        read_only_fields = ['created_at']
        extra_kwargs = {
            'temperature': {
                'error_messages': {
                    'invalid': 'Температура должна быть числом',
                    'max_digits': 'Температура не может превышать 5 цифр',
                    'max_decimal_places': 'Не более 2 знаков после запятой'
                }
            }
        }

    def get_image_url(self, obj):
        """Динамически генерируем URL изображения с префиксом /api"""
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(f'/api{obj.image.url}') if request else None
        return None

    def to_internal_value(self, data):
        """Обрабатываем загрузку файла перед валидацией"""
        if hasattr(data, 'getlist'):  # Для MultiPartParser
            if 'image' in data:
                data = data.copy()
                data['image'] = data.getlist('image')[0]
        return super().to_internal_value(data)


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
