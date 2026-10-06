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
        "measurements/latest/",
        views.LatestMeasurementsView.as_view(),
        name="latest-measurements",
    ),
]