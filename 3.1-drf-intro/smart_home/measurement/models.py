from django.db import models


class Sensor(models.Model):
    """Имя датчика и описание"""
    name = models.CharField(max_length=50)
    description  = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Measurement(models.Model):
    """Измерение датчика"""
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements')
    temperature = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sensor.name} - {self.temperature}°C at {self.created_at}"
