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
    station = serializers.PrimaryKeyRelatedField(queryset=Station.objects.all())
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

        