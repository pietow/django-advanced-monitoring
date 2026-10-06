from django.db import connection


def dictfetchall(cursor) -> list[dict[str, object]]:
    columns = [column[0] for column in cursor.description]
    return [
        dict(zip(columns, row, strict=True))
        for row in cursor
    ]


def fetch_latest_measurements() -> list[dict[str, object]]:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            WITH ranked_measurements AS (
                SELECT
                    measurement.id,
                    measurement.sensor_id,
                    sensor.name AS sensor_name,
                    sensor.unit,
                    station.code AS station_code,
                    measurement.timestamp,
                    measurement.value,
                    measurement.quality_flag,
                    ROW_NUMBER() OVER (
                        PARTITION BY measurement.sensor_id
                        ORDER BY
                            measurement.timestamp DESC,
                            measurement.id DESC
                    ) AS row_number
                FROM monitoring_measurement AS measurement
                INNER JOIN monitoring_sensor AS sensor
                    ON sensor.id = measurement.sensor_id
                INNER JOIN monitoring_station AS station
                    ON station.id = sensor.station_id
            )
            SELECT
                sensor_id,
                sensor_name,
                unit,
                station_code,
                timestamp,
                value,
                quality_flag
            FROM ranked_measurements
            WHERE row_number = 1
            ORDER BY station_code, sensor_name
            """
        )
        return dictfetchall(cursor)