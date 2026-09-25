from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from monitoring.models import Sensor, Station
from monitoring.api.serializers import (
    SensorLinkDemoSerializer,
    StationBasicSerializer,
)


class StationListView(APIView):
    def get(self, request):
        stations = Station.objects.order_by("code")
        serializer = StationBasicSerializer(stations, many=True)
        return Response(serializer.data)


class StationDetailView(APIView):
    def get(self, request, pk):
        station = get_object_or_404(Station, pk=pk)
        serializer = StationBasicSerializer(station)
        return Response(serializer.data)


class SensorLinkDetailView(APIView):
    def get(self, request, pk):
        sensor = get_object_or_404(Sensor, pk=pk)
        serializer = SensorLinkDemoSerializer(
            sensor, context={"request": request},
        )
        return Response(serializer.data)
