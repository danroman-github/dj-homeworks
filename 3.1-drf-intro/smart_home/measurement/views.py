from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    CreateAPIView
)
from rest_framework.response import Response
from rest_framework import status
from .models import Sensor, Measurement
from .serializers import MeasurementSerializer, SensorSerializer
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser


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
    # queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def create(self, request, *args, **kwargs):
        try:
            # Проверка существования датчика
            sensor_id = request.data.get('sensor')
            if not sensor_id:
                return Response(
                    {'error': 'ID датчика обязательно'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            Sensor.objects.get(pk=sensor_id)

            # Обработка файла
            if 'image' in request.FILES:
                image = request.FILES['image']
                if image.size > 2 * 1024 * 1024:  # 2MB лимит
                    return Response(
                        {'error': 'Файл слишком большой (макс. 2MB)'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            return super().create(request, *args, **kwargs)

        except Sensor.DoesNotExist:
            return Response(
                {'error': f'Датчик с ID={sensor_id} не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return super().create(request, *args, **kwargs)
