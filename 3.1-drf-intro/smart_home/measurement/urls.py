from django.urls import path
from django.conf import settings
from django.conf.urls.static import static, serve
from measurement.views import (
    SensorListCreateView,
    SensorRetrieveUpdateView,
    MeasurementCreateView
)

urlpatterns = [
    path('sensors/', SensorListCreateView.as_view(), name='sensor-list-create'),
    path('sensors/<int:pk>/', SensorRetrieveUpdateView.as_view(), name='sensor-update'),
    path('measurements/', MeasurementCreateView.as_view(), name='measurement-create'),
    path('api/media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
