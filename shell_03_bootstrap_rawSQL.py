from django.db import connection, transaction
from django.db.models import FloatField
from django.db.models.expressions import RawSQL
from django.test.utils import CaptureQueriesContext

from monitoring.models import Measurement, Sensor, Station

station = Station.objects.get(code="DEMO-ALPINE-01")
sensor = station.sensors.get(name="Air temperature") # type: ignore

print(station.pk, station.code, station.active)
print(sensor.pk, sensor.name)