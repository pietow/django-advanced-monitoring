from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from monitoring.models import Sensor, Station
from monitoring.api.serializers import (
    SensorLinkDemoSerializer,
    StationSerializer,
    StationNestedWriteSerializer,
)


class StationListView(APIView):
    def get(self, request):
        stations = Station.objects.order_by("code")
        serializer = StationSerializer(stations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StationNestedWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        demo_station = get_object_or_404(Station, code="DEMO-ALPINE-01")
        serializer.save(owner=demo_station.owner)
        return Response(serializer.data, status=201)


class StationDetailView(APIView):
    def get(self, request, pk):
        station = get_object_or_404(Station, pk=pk)
        serializer = StationSerializer(station)
        return Response(serializer.data)

    def patch(self, request, pk):
        station = get_object_or_404(Station, pk=pk)
        serializer = StationNestedWriteSerializer(
            station, data=request.data, partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class SensorLinkDetailView(APIView):
    def get(self, request, pk):
        sensor = get_object_or_404(Sensor, pk=pk)
        serializer = SensorLinkDemoSerializer(
            sensor, context={"request": request},
        )
        return Response(serializer.data)