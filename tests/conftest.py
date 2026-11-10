import pytest
from decimal import Decimal
from django.contrib.auth.models import User
from monitoring.models import Station
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()


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


    
@pytest.fixture
def other_user(db):
    return User.objects.create_user(
        username="bob",
        password="test-password",
    )

@pytest.fixture
def staff_user(db):
    return User.objects.create_user(
        username="admin",
        password="test-password",
        is_staff= True
    )


@pytest.fixture
def other_station(other_user):
    return Station.objects.create(
        owner=user,
        code="TEST-STATION-02",
        name="Second Test Station",
        latitude=Decimal("52.100000"),
        longitude=Decimal("8.100000"),
    )    

@pytest.fixture(autouse=True)
def fast_password_hasher(settings):
    settings.PASSWORD_HASHERS = [
        "django.contrib.auth.hashers.MD5PasswordHasher"
    ]