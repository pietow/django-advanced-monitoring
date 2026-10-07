from importlib.resources import files

from django.db import connection

from monitoring.queries import dictfetchall


SENSOR_HEALTH_SQL = (
    files("monitoring")
    .joinpath("sql/sensor_health.sql")
    .read_text(encoding="utf-8")
)


def get_sensor_health(station_code, start, end):
    with connection.cursor() as cursor:
        cursor.execute(
            SENSOR_HEALTH_SQL,
            [station_code, start, end],
        )

        return dictfetchall(cursor)
