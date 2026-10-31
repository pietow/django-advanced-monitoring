import pytest
from django.contrib.auth.models import User
from decimal import Decimal
from rest_framework.test import APIClient

from monitoring.models import Station


# autouse=True: pytest wendet diese Fixture automatisch auf jeden Test an,
# ohne dass ein Test sie als Parameter anfordern muss.
# Der Standard-Hasher (PBKDF2, 1 Mio. Iterationen) braucht pro create_user()
# ca. 1-2 s. MD5 ist unsicher, für Testdaten aber ausreichend und schnell.
# Die settings-Fixture von pytest-django setzt den Wert nach jedem Test zurück.
@pytest.fixture(autouse=True)
def fast_password_hasher(settings):
    settings.PASSWORD_HASHERS = [
        "django.contrib.auth.hashers.MD5PasswordHasher",
    ]


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
def other_station(other_user):
    return Station.objects.create(
        owner=other_user,
        code="TEST-STATION-02",
        name="Second Test Station",
        latitude=Decimal("52.100000"),
        longitude=Decimal("8.100000"),
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def staff_user(db):
    return User.objects.create_user(
        username="admin",
        password="test-password",
        is_staff=True,
    )
