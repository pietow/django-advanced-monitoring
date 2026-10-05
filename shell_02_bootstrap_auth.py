from django.contrib.auth import get_user_model
from monitoring.models import Station
from monitoring.api import serializers as demo
from importlib import reload

User = get_user_model()
alice = User.objects.get(username="workshop_alice")
bob = User.objects.get(username="workshop_bob")
station = Station.objects.get(code="DEMO-ALPINE-01")
assert station.owner_id == alice.pk
assert alice.is_active and bob.is_active
assert not alice.is_staff and not bob.is_staff
print(station.pk, station.code, alice.pk, bob.pk, station.active)

# reload(demo)
