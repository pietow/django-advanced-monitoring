from rest_framework import serializers

from monitoring.models import Sensor, Station, StationMetadata, Tag
from django.contrib.auth import get_user_model


class StationPlainSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=30)
    name = serializers.CharField(max_length=120)
    active = serializers.BooleanField()

class StationBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ["id", "code", "name", "active"]



class SensorPkDemoSerializer(serializers.ModelSerializer):
    station = serializers.PrimaryKeyRelatedField(queryset=Station.objects.all())
    class Meta:
        model = Sensor
        fields = ["id", "name", "station"]

class SensorStringDemoSerializer(serializers.ModelSerializer):
    station = serializers.StringRelatedField()

    class Meta:
        model = Sensor
        fields = ["id", "station"]

class SensorSlugDemoSerializer(serializers.ModelSerializer):
    station = serializers.SlugRelatedField(slug_field="code", read_only=True)

    class Meta:
        model = Sensor
        fields = ["id", "station"]


class TagStationsDemoSerializer(serializers.ModelSerializer):
    stations = serializers.SlugRelatedField(
        many=True, slug_field="code", read_only=True,
    )

    class Meta:
        model = Tag
        fields = ["name", "stations"]

class SensorLinkDemoSerializer(serializers.ModelSerializer):
    station = serializers.HyperlinkedRelatedField(
        read_only=True, view_name="station-detail",
    )

    class Meta:
        model = Sensor
        fields = ["id", "station"]

class MetadataReadDemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StationMetadata
        fields = ["operator", "installation_date"]


class StationMetadataReadDemoSerializer(serializers.ModelSerializer):
    metadata = MetadataReadDemoSerializer(read_only=True)

    class Meta:
        model = Station
        fields = ["code", "metadata"]

class SensorSourceDemoSerializer(serializers.ModelSerializer):
    station_name = serializers.CharField(source="station.name", read_only=True)

    class Meta:
        model = Sensor
        fields = ["id", "name", "station_name"]
        

class SensorLabelDemoSerializer(serializers.ModelSerializer):
    status_label = serializers.SerializerMethodField()

    class Meta:
        model = Sensor
        fields = ["id", "status_label"]

    def get_status_label(self, obj):
        return "enabled" if obj.active else "disabled"

class SensorSerializer(serializers.ModelSerializer):
    measurement_count = serializers.SerializerMethodField()
    class Meta:
        model = Sensor
        fields = ['id', 'name', 'sensor_type', 'unit', 'active', 'measurement_count']

    def get_measurement_count(self, obj):
        return obj.measurements.count()

User = get_user_model()

class StationSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    tags = serializers.SlugRelatedField(many=True, slug_field='name', read_only=True)
    sensors = SensorSerializer(many=True)
    elevation_m = serializers.FloatField(source='metadata.elevation_m')

    class Meta:
        model = Station
        fields = [
            'id', 'code', 'name', 'owner', 
            'elevation_m',
            'tags', 'sensors'
        ]