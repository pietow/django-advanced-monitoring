from rest_framework import serializers

from monitoring.models import Sensor, Station, StationMetadata, Tag

class StationPlainSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=30)
    name = serializers.CharField(max_length=120)
    active = serializers.BooleanField()


class StationBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ["id", "code", "name", "name"]


class SensorPkDemoSerializer(serializers.ModelSerializer):
    # station = serializers.PrimaryKeyRelatedField(queryset=Station.objects.all())
    station = serializers.PrimaryKeyRelatedField(queryset=Station.objects.all()) # leeres queryset
    # mit read_only werden das Feld station bei POST request ignoriert
    # bei get Req. sehen wir aber den Feldwert als ganzzahligen PK-Wert
    class Meta:
        model = Sensor
        fields = ["id", "name", "station"]
    

class MetaDataReadDemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StationMetadata
        fields = ["operator", "installation_date"]


class StationMetadataReadDemoSerializer(serializers.ModelSerializer):
    metadata = MetaDataReadDemoSerializer(read_only=True)                # es soll das operator und installation_date als dict angezeigt werden

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

class SensorLinkDemoSerializer(serializers.ModelSerializer):
    station = serializers.HyperlinkedRelatedField(
        read_only=True, view_name="station-detail",
    ) # d.h. wir brauch noch den view; demo kommt später, da in der shell etwas umständlich

    class Meta:
        model = Sensor
        fields = ["id", "station"]

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

    def get_measurement_count(self, obj)->int:
        return obj.measurements.count()


class StationSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name",
    )

    sensors = SensorSerializer(
        many=True,
        read_only=True,
    )

    elevation_m = serializers.FloatField(
        source="metadata.elevation_m",
        read_only=True,
        allow_null=True,
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
    owner = serializers.PrimaryKeyRelatedField(read_only=True) # owner wird beim schreiben ignoriert

    class Meta:
        model = Station
        fields = [
            "id", "code", "name", "latitude",
            "longitude", "active", "owner",
        ]

    def validate_code(self, value):
        if " " in value:
                raise serializers.ValidationError(
                    "Stationscode darf keine Leerzeichen enthalten"
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
        instance.name = validated_data.get('name', instance.name)
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

    def create(self, validated_data):
        # Es soll sowohl in Station gespeichert werden, als auch in StationMetaData
        metadata_data = validated_data.pop("metadata", None)
        station = Station.objects.create(**validated_data)
        if metadata_data is not None:
            StationMetadata.objects.create(station=station,**metadata_data)
        return station