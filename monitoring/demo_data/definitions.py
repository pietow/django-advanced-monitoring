from dataclasses import dataclass
from datetime import date


DEMO_PASSWORD = "Workshop-Demo-2026!"
DEMO_CODE_PREFIX = "DEMO-"


@dataclass(frozen=True)
class DemoUserDefinition:
    username: str
    email: str
    first_name: str
    last_name: str


@dataclass(frozen=True)
class SensorDefinition:
    name: str
    sensor_type: str
    unit: str
    base_value: float
    step: float
    active: bool = True
    has_measurements: bool = True


@dataclass(frozen=True)
class StationDefinition:
    code: str
    name: str
    latitude: str
    longitude: str
    owner_username: str
    tags: tuple[str, ...]
    sensors: tuple[SensorDefinition, ...]
    active: bool = True
    elevation_m: float | None = 100.0
    installation_date: date = date(2024, 5, 15)
    operator: str = "Workshop Monitoring Team"
    description: str = "Deterministic workshop monitoring station."
    maintenance_note: str = ""


DEMO_USERS = (
    DemoUserDefinition("workshop_alice", "alice@example.test", "Alice", "Albrecht"),
    DemoUserDefinition("workshop_bob", "bob@example.test", "Bob", "Bergmann"),
    DemoUserDefinition("workshop_carol", "carol@example.test", "Carol", "Chen"),
)

DEMO_TAGS = (
    "alpine",
    "coastal",
    "urban",
    "research",
    "high-priority",
)

DEMO_STATIONS = (
    StationDefinition(
        code="DEMO-ALPINE-01",
        name="Alpine Ridge",
        latitude="47.269212",
        longitude="11.404102",
        owner_username="workshop_alice",
        tags=("alpine", "research"),
        sensors=(
            SensorDefinition("Air temperature", "temperature", "°C", 12.5, 0.2),
            SensorDefinition("Relative humidity", "humidity", "%", 64.0, 0.5),
            SensorDefinition("Air pressure", "pressure", "hPa", 920.0, 0.8),
        ),
        elevation_m=1840.0,
    ),
    StationDefinition(
        code="DEMO-ALPINE-02",
        name="Valley Pass",
        latitude="47.224510",
        longitude="11.390210",
        owner_username="workshop_bob",
        tags=("alpine",),
        sensors=(
            SensorDefinition("Air temperature", "temperature", "°C", 15.0, 0.15),
            SensorDefinition("Rain gauge", "precipitation", "mm", 0.4, 0.1),
        ),
        elevation_m=920.0,
    ),
    StationDefinition(
        code="DEMO-LAKE-01",
        name="Lake Shore",
        latitude="47.856320",
        longitude="12.104450",
        owner_username="workshop_carol",
        tags=("research", "high-priority"),
        sensors=(
            SensorDefinition("Water temperature", "temperature", "°C", 9.5, 0.1),
            SensorDefinition("Relative humidity", "humidity", "%", 71.0, 0.4),
            SensorDefinition("Air pressure", "pressure", "hPa", 1008.0, 0.6),
        ),
        elevation_m=None,
    ),
    StationDefinition(
        code="DEMO-COAST-01",
        name="North Pier",
        latitude="53.548800",
        longitude="9.987170",
        owner_username="workshop_alice",
        tags=("coastal", "high-priority"),
        sensors=(
            SensorDefinition("Air temperature", "temperature", "°C", 8.0, 0.25),
            SensorDefinition("Wind pressure", "pressure", "hPa", 1015.0, 0.7),
            SensorDefinition("Rain gauge", "precipitation", "mm", 1.2, 0.2),
        ),
        elevation_m=4.0,
    ),
    StationDefinition(
        code="DEMO-COAST-02",
        name="Harbor Weather",
        latitude="54.092440",
        longitude="12.099150",
        owner_username="workshop_bob",
        tags=("coastal",),
        sensors=(
            SensorDefinition("Air temperature", "temperature", "°C", 7.5, 0.2),
            SensorDefinition("Relative humidity", "humidity", "%", 79.0, 0.3),
        ),
        elevation_m=7.0,
        maintenance_note="Anemometer inspection due after the next storm.",
    ),
    StationDefinition(
        code="DEMO-URBAN-01",
        name="City Center",
        latitude="52.520008",
        longitude="13.404954",
        owner_username="workshop_carol",
        tags=("urban", "high-priority"),
        sensors=(
            SensorDefinition("Air temperature", "temperature", "°C", 18.0, 0.3),
            SensorDefinition("Particulate proxy", "pressure", "hPa", 1002.0, 0.5),
            SensorDefinition("Relative humidity", "humidity", "%", 58.0, 0.6),
        ),
        elevation_m=34.0,
    ),
    StationDefinition(
        code="DEMO-URBAN-02",
        name="West Industrial Park",
        latitude="52.496700",
        longitude="13.365900",
        owner_username="workshop_alice",
        tags=("urban", "research"),
        sensors=(
            SensorDefinition("Air temperature", "temperature", "°C", 19.0, 0.25),
            SensorDefinition("Relative humidity", "humidity", "%", 55.0, 0.5, active=False),
            SensorDefinition("Air pressure", "pressure", "hPa", 1004.0, 0.4),
        ),
        elevation_m=41.0,
    ),
    StationDefinition(
        code="DEMO-FOREST-01",
        name="Forest Clearing",
        latitude="51.173900",
        longitude="10.455900",
        owner_username="workshop_bob",
        tags=("research",),
        sensors=(
            SensorDefinition("Air temperature", "temperature", "°C", 13.0, 0.18),
            SensorDefinition("Relative humidity", "humidity", "%", 83.0, 0.25),
            SensorDefinition("Rain gauge", "precipitation", "mm", 0.8, 0.15, has_measurements=False),
        ),
        elevation_m=510.0,
    ),
    StationDefinition(
        code="DEMO-RIVER-01",
        name="River Bend",
        latitude="50.937500",
        longitude="6.960300",
        owner_username="workshop_carol",
        tags=("research", "high-priority"),
        sensors=(
            SensorDefinition("Water temperature", "temperature", "°C", 11.0, 0.12),
            SensorDefinition("Water pressure", "pressure", "hPa", 1012.0, 0.35),
        ),
        elevation_m=48.0,
    ),
    StationDefinition(
        code="DEMO-REMOTE-01",
        name="Remote Outpost",
        latitude="48.135100",
        longitude="11.582000",
        owner_username="workshop_alice",
        tags=("alpine", "research"),
        sensors=(
            SensorDefinition("Air temperature", "temperature", "°C", 10.0, 0.22),
            SensorDefinition("Relative humidity", "humidity", "%", 68.0, 0.45),
            SensorDefinition("Air pressure", "pressure", "hPa", 970.0, 0.55),
        ),
        active=False,
        elevation_m=760.0,
    ),
)