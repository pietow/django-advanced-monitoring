from monitoring.models import Station, Sensor, StationMetadata, Tag
from monitoring.api import serializers as demo
from importlib import reload


station = Station.objects.get(code="DEMO-ALPINE-01")
sensor = station.sensors.get(name="Air temperature")
owner = station.owner
print(station.code, station.pk, sensor.pk, owner.pk)

# reload(demo)