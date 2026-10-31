import pytest

from django.urls import reverse
from rest_framework.authtoken.models import Token


def test_station_detail_requires_authentication(
    api_client,
    station,
):
    url = reverse(
        "station-detail",
        args=[station.pk],
    )

    response = api_client.get(url)

    assert response.status_code == 401


def test_owner_can_read_station(
    api_client,
    user,
    station,
):
    api_client.force_authenticate(
        user=user,
    )
    url = reverse(
        "station-detail",
        args=[station.pk],
    )
    response = api_client.get(url)

    assert response.status_code == 200



@pytest.mark.django_db
def test_token_authentication_accepts_valid_token(
    api_client,
    user,
    station,
):
    token = Token.objects.create(
        user=user,
    )

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Token {token.key}",
    )

    url = reverse(
        "station-detail",
        args=[station.pk],
    )

    response = api_client.get(url)

    assert response.status_code == 200
