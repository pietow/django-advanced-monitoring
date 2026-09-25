from rest_framework import serializers

from monitoring.models import Sensor, Station, StationMetadata, Tag


class StationPlainSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=30)
    name = serializers.CharField(max_length=120)
    active = serializers.BooleanField()

class StationBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ["id", "code", "name", "active"]

