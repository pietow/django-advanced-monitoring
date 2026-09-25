from rest_framework import serializers

from monitoring.models import Sensor, Station, StationMetadata, Tag
from django.contrib.auth import get_user_model
from django.db import transaction


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

class StationWriteSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Station
        fields = [
            "id", "code", "name", "latitude",
            "longitude", "active", "owner",
        ]

    def validate_code(self, value):
        if " " in value:
            raise serializers.ValidationError(
                "Station codes must not contain spaces."
            )
        return value

    def validate(self, data):
        latitude = data.get(
            "latitude", getattr(self.instance, "latitude", None),
        )
        longitude = data.get(
            "longitude", getattr(self.instance, "longitude", None),
        )
        if latitude == 0 and longitude == 0:
            raise serializers.ValidationError(
                "Latitude and longitude must not both be zero."
            )
        return data

class MetadataInputDemoSerializer(serializers.Serializer):
    operator = serializers.CharField(required=True)
    maintenance_note = serializers.CharField(write_only=True)
    elevation_m = serializers.FloatField(read_only=True)

class TagWritePlainSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)

    def create(self, validated_data):
        return Tag.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance

class StationMetadataWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = StationMetadata
        fields = [
            "elevation_m", "installation_date", "operator",
            "description", "maintenance_note",
        ]


class StationNestedWriteSerializer(StationWriteSerializer):
    metadata = StationMetadataWriteSerializer(required=False)

    class Meta(StationWriteSerializer.Meta):
        fields = StationWriteSerializer.Meta.fields + ["metadata"]

    @transaction.atomic
    def create(self, validated_data):
        metadata_data = validated_data.pop("metadata", None)
        station = Station.objects.create(**validated_data)
        if metadata_data is not None:
            StationMetadata.objects.create(station=station, **metadata_data)
        return station
    
    @transaction.atomic
    def update(self, instance, validated_data):
        metadata_data = validated_data.pop("metadata", None)
        instance = super().update(instance, validated_data)
        if metadata_data is not None:
            metadata, _ = StationMetadata.objects.get_or_create(
                station=instance,
            )
            for field, value in metadata_data.items():
                setattr(metadata, field, value)
            metadata.save()
        return instance


