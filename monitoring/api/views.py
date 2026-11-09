from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from monitoring.models import Sensor, Station
from monitoring.api.serializers import (
    SensorLinkDemoSerializer,
    StationSerializer,
    StationNestedWriteSerializer,
)

from django.contrib.auth import get_user_model
User = get_user_model()


class StationListView(APIView):
    def get(self, request):
        stations = Station.objects.order_by("code")
        serializer = StationSerializer(stations, many=True)
        # user = User.objects.get(pk=1)
        # sensor = Sensor.objects.filter(station__owner=user) # Auf dieser ebene wird gefiltert
        # serializer = SensorPkDemoSerializer(sensor, many=True)    
        return Response(serializer.data)

    def post(self, request):
        serializer = StationNestedWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        demo_station = get_object_or_404(Station, code="DEMO-ALPINE-01")
        serializer.save(owner=demo_station.owner)
        return Response(serializer.data)


class StationDetailView(APIView):
    def get(self, request, pk):
        station = get_object_or_404(Station, pk=pk)
        serializer = StationSerializer(station)
        return Response(serializer.data)

    
    def patch(self, request, pk):
        station = get_object_or_404(Station, pk=pk)
        serializer = StationNestedWriteSerializer(station, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class SensorLinkDetailView(APIView):
    def get(self, request, pk):
        sensor = get_object_or_404(Sensor, pk=pk)
        serializer = SensorLinkDemoSerializer(
            sensor, context={"request": request},
        )# im req. steht schema, port-> vollständige url nur so erzeugbar
        return Response(serializer.data)
