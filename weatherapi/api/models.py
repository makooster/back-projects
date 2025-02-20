from django.db import models
from cities.models import City

class Weather(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    temperature = models.FloatField()
    description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.city.name}: {self.temperature}°C, {self.description}"
