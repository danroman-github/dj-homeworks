from django.contrib import admin
from django.urls import path
from measurement.views import (
    SensorListCreateView,
    SensorRetrieveUpdateView,
    MeasurementCreateView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sensors/', SensorListCreateView.as_view(), name='sensor-list-create'),
    path('sensors/<int:pk>/', SensorRetrieveUpdateView.as_view(), name='sensor-update'),
    path('measurements/', MeasurementCreateView.as_view(), name='measurement-create'),
]
