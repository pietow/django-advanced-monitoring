from rest_framework import serializers

from monitoring.models import Sensor, Station


class SensorSerializer(serializers.ModelSerializer):
    measurement_count = serializers.SerializerMethodField()

    class Meta:
        model = Sensor
        fields = [
            "id",
            "name",
            "sensor_type",
            "unit",
            "active",
            "measurement_count",
        ]

    def get_measurement_count(self, obj):
        return obj.measurements.count()


class StationSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    tags = serializers.SlugRelatedField(
        many=True,
        slug_field="name",
        read_only=True,
    )
    sensors = SensorSerializer(many=True, read_only=True)
    elevation_m = serializers.FloatField(
        source="metadata.elevation_m",
        allow_null=True,
        read_only=True,
    )

    class Meta:
        model = Station
        fields = [
            "id",
            "code",
            "name",
            "owner",
            "elevation_m",
            "tags",
            "sensors",
        ]


class StationWriteSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Station
        fields = [
            "id",
            "code",
            "name",
            "latitude",
            "longitude",
            "active",
            "owner",
        ]

    def validate_code(self, value):
        if " " in value:
            raise serializers.ValidationError(
                "Station codes must not contain spaces."
            )
        return value

    def validate(self, data):
        latitude = data.get(
            "latitude",
            getattr(self.instance, "latitude", None),
        )
        longitude = data.get(
            "longitude",
            getattr(self.instance, "longitude", None),
        )
        if latitude == 0 and longitude == 0:
            raise serializers.ValidationError(
                "Latitude and longitude must not both be zero."
            )
        return data
    

class SensorHealthQuerySerializer(serializers.Serializer):
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()

    def validate(self, attrs):
        if attrs["start"] >= attrs["end"]:
            raise serializers.ValidationError(
                "start muss vor end liegen."
            )
        return attrs