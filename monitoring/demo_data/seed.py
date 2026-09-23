from dataclasses import dataclass
from datetime import datetime, timedelta, timezone as dt_timezone

from django.contrib.auth import get_user_model
from django.db import transaction

from monitoring.demo_data.definitions import (
    DEMO_CODE_PREFIX,
    DEMO_PASSWORD,
    DEMO_STATIONS,
    DEMO_TAGS,
    DEMO_USERS,
)
from monitoring.models import Measurement, Sensor, Station, StationMetadata, Tag


REFERENCE_DATETIME = datetime(2025, 1, 1, 0, 0, tzinfo=dt_timezone.utc)
QUALITY_FLAGS = (
    Measurement.QualityFlag.VALID,
    Measurement.QualityFlag.VALID,
    Measurement.QualityFlag.SUSPECT,
    Measurement.QualityFlag.VALID,
    Measurement.QualityFlag.INVALID,
    Measurement.QualityFlag.VALID,
)


class DemoDataError(Exception):
    """Raised when seeding would conflict with existing demo data."""


@dataclass(frozen=True)
class SeedResult:
    users: int
    stations: int
    sensors: int
    measurements: int


def seed_demo_data(*, reset: bool = False, large: bool = False) -> SeedResult:
    """Create the deterministic workshop dataset in one transaction."""
    with transaction.atomic():
        existing_demo_stations = Station.objects.filter(code__startswith=DEMO_CODE_PREFIX)
        if existing_demo_stations.exists() and not reset:
            raise DemoDataError(
                "Demo stations already exist. Re-run with --reset to replace workshop demo data."
            )

        if reset:
            existing_demo_stations.delete()

        users = _create_users()
        tags = _create_tags()
        stations = _create_stations(users, tags)
        sensors = _create_sensors(stations)
        measurement_count = _create_measurements(sensors, large=large)

    return SeedResult(
        users=len(users),
        stations=len(stations),
        sensors=len(sensors),
        measurements=measurement_count,
    )


def _create_users():
    user_model = get_user_model()
    users = {}
    for definition in DEMO_USERS:
        user, created = user_model.objects.get_or_create(
            username=definition.username,
            defaults={
                "email": definition.email,
                "first_name": definition.first_name,
                "last_name": definition.last_name,
            },
        )
        if created:
            user.set_password(DEMO_PASSWORD)
            user.save(update_fields=["password"])
        users[definition.username] = user
    return users


def _create_tags():
    return {
        name: Tag.objects.get_or_create(name=name)[0]
        for name in DEMO_TAGS
    }


def _create_stations(users, tags):
    stations = [
        Station(
            code=definition.code,
            name=definition.name,
            latitude=definition.latitude,
            longitude=definition.longitude,
            owner=users[definition.owner_username],
            active=definition.active,
        )
        for definition in DEMO_STATIONS
    ]
    Station.objects.bulk_create(stations, batch_size=100)
    stations_by_code = {station.code: station for station in stations}

    metadata = [
        StationMetadata(
            station=stations_by_code[definition.code],
            elevation_m=definition.elevation_m,
            installation_date=definition.installation_date,
            operator=definition.operator,
            description=definition.description,
            maintenance_note=definition.maintenance_note,
        )
        for definition in DEMO_STATIONS
    ]
    StationMetadata.objects.bulk_create(metadata, batch_size=100)

    for definition in DEMO_STATIONS:
        stations_by_code[definition.code].tags.set(
            [tags[tag_name] for tag_name in definition.tags]
        )
    return stations


def _create_sensors(stations):
    stations_by_code = {station.code: station for station in stations}
    sensors = [
        Sensor(
            station=stations_by_code[definition.code],
            name=sensor_definition.name,
            sensor_type=sensor_definition.sensor_type,
            unit=sensor_definition.unit,
            active=sensor_definition.active,
            installed_at=definition.installation_date,
        )
        for definition in DEMO_STATIONS
        for sensor_definition in definition.sensors
    ]
    Sensor.objects.bulk_create(sensors, batch_size=100)
    return sensors


def _create_measurements(sensors, *, large: bool) -> int:
    measurements_per_sensor = 1000 if large else 48
    measurements = []
    sensor_definitions = {
        (station_definition.code, sensor_definition.name): sensor_definition
        for station_definition in DEMO_STATIONS
        for sensor_definition in station_definition.sensors
    }

    for sensor in sensors:
        sensor_definition = sensor_definitions[(sensor.station.code, sensor.name)]
        if not sensor_definition.has_measurements:
            continue
        for index in range(measurements_per_sensor):
            measurements.append(
                Measurement(
                    sensor=sensor,
                    timestamp=REFERENCE_DATETIME + timedelta(hours=index),
                    value=round(
                        sensor_definition.base_value
                        + sensor_definition.step * (index % 24),
                        4,
                    ),
                    quality_flag=QUALITY_FLAGS[index % len(QUALITY_FLAGS)],
                )
            )

    Measurement.objects.bulk_create(measurements, batch_size=1000)
    return len(measurements)