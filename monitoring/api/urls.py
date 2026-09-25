from django.urls import path

from monitoring.api import views

urlpatterns = [
    path("stations/", views.StationListView.as_view(), name="station-list"),
    path(
        "stations/<int:pk>/",
        views.StationDetailView.as_view(),
        name="station-detail",
    ),
    path(
        "sensor-links/<int:pk>/",
        views.SensorLinkDetailView.as_view(),
        name="sensor-link-detail",
    ),
]