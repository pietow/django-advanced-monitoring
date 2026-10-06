from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from monitoring.api.serializers import (
    StationSerializer,
    StationWriteSerializer,
)
from monitoring.models import Station
from monitoring.api.permissions import IsStationOwnerOrReadOnly
from monitoring.queries import fetch_latest_measurements 


class StationListView(APIView):
    permission_classes = [IsStationOwnerOrReadOnly]
    def get(self, request):
        stations = Station.objects.order_by("code")
        serializer = StationSerializer(stations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StationWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response(serializer.data, status=201)


class StationDetailView(APIView):
    permission_classes = [IsStationOwnerOrReadOnly]
    def get_object(self, request, pk):
        station = get_object_or_404(Station, pk=pk)
        self.check_object_permissions(request, station)
        return station
    
    def get(self, request, pk):
        station = self.get_object(request, pk=pk)
        serializer = StationSerializer(station)
        return Response(serializer.data)

    def patch(self, request, pk):
        station = self.get_object(request, pk=pk)
        print('request.user ', request.user)
        serializer = StationWriteSerializer(
            station, data=request.data, partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        station = self.get_object(request, pk)
        station.delete()
        return Response(status=204)

class LatestMeasurementsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rows = fetch_latest_measurements()
        return Response(rows)