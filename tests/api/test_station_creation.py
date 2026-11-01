import pytest
from django.urls import reverse

from monitoring.models import Station


pytestmark = pytest.mark.django_db


@pytest.fixture
def station_payload():
    return {
        "code": "TEST-CREATE-01",
        "name": "Neue Messstation",
        "latitude": "52.100000",
        "longitude": "8.100000",
    }


def test_authenticated_user_can_create_station(api_client, user, station_payload):
    api_client.force_authenticate(user=user)
    count_before = Station.objects.count()

    response = api_client.post(
        reverse("station-list"),
        station_payload,
        format="json",
    )

    assert response.status_code == 201, response.data
    assert Station.objects.count() == count_before + 1
    station = Station.objects.get(pk=response.data["id"])
    assert station.code == station_payload["code"]
    assert station.owner_id == user.pk
    assert response.data["owner"] == user.pk


def test_submitted_foreign_owner_is_ignored(
    api_client, user, other_user, station_payload
):
    api_client.force_authenticate(user=user)
    station_payload["owner"] = other_user.pk

    response = api_client.post(
        reverse("station-list"),
        station_payload,
        format="json",
    )

    assert response.status_code == 201, response.data
    station = Station.objects.get(pk=response.data["id"])
    assert station.owner_id == user.pk
    assert response.data["owner"] == user.pk


def test_anonymous_user_cannot_create_station(api_client, station_payload):
    count_before = Station.objects.count()

    response = api_client.post(
        reverse("station-list"),
        station_payload,
        format="json",
    )

    assert response.status_code == 401, response.data
    assert Station.objects.count() == count_before


def test_station_code_with_spaces_is_rejected(api_client, user, station_payload):
    api_client.force_authenticate(user=user)
    station_payload["code"] = "INVALID CODE"
    count_before = Station.objects.count()

    response = api_client.post(
        reverse("station-list"),
        station_payload,
        format="json",
    )

    assert response.status_code == 400, response.data
    assert "code" in response.data
    assert Station.objects.count() == count_before
