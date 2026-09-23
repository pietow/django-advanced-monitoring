from django.contrib import admin

from .models import Measurement, Sensor, Station, StationMetadata, Tag

admin.site.register([Station, StationMetadata, Sensor, Measurement, Tag])
