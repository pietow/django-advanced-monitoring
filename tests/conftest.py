import pytest
from decimal import Decimal
from django.contrib.auth.models import User
from monitoring.models import Station


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="alice",
        password="test-password",
    )


@pytest.fixture
def station(user):
    return Station.objects.create(
        owner=user,
        code="TEST-STATION-01",
        name="Test Station",
        latitude=Decimal("52.000000"),
        longitude=Decimal("8.000000"),
    )    
    