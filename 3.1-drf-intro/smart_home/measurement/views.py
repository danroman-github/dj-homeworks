from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    CreateAPIView
)
from rest_framework.response import Response
from rest_framework import status
from .models import Sensor
from .serializers import MeasurementSerializer, SensorSerializer


class SensorListCreateView(ListCreateAPIView):
    """Получение списка датчиков и создание нового датчика"""
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class SensorRetrieveUpdateView(RetrieveUpdateAPIView):
    """Получение информации о датчике и его обновление"""
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    lookup_field = 'pk'


class MeasurementCreateView(CreateAPIView):
    """Добавление нового измерения температуры"""
    serializer_class = MeasurementSerializer

    def create(self, request, *args, **kwargs):
        # Проверяем существование датчика
        sensor_id = request.data.get('sensor')
        if not sensor_id:
            return Response(
                {'ошибка': 'Не указан ID датчика'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            sensor = Sensor.objects.get(pk=sensor_id)
        except Sensor.DoesNotExist:
            return Response(
                {'ошибка': f'Датчик с ID={sensor_id} не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Добавляем sensor_id в данные перед валидацией
        data = request.data.copy()
        data['sensor_id'] = sensor.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
