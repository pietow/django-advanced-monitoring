import pytest

from decimal import Decimal

from django.contrib.auth.models import User

from monitoring.models import Station

@pytest.mark.django_db
def test_station_is_persisted():
    user = User.objects.create_user( 
        username="db-owner",
        password="test-password",
    )

    Station.objects.create(
        owner=user,
        code="TEST-DB-01",
        name="Database Test Station",
        latitude=Decimal("52.000000"),
        longitude=Decimal("8.000000"),
    )

    assert Station.objects.filter(
        code="TEST-DB-01",
    ).exists()

@pytest.mark.django_db
def test_previous_station_is_not_visible():
    assert not Station.objects.filter(
        code="TEST-DB-01",
    ).exists()
