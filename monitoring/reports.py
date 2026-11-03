from importlib.resources import files

from django.db import connection

from monitoring.queries import dictfetchall


SENSOR_HEALTH_SQL = (
    files("monitoring")
    .joinpath("sql/sensor_health.sql")
    .read_text(encoding="utf-8")
)


def get_sensor_health(station_code, start, end):
    """Liefere aggregierte Messwerte einer Station im Zeitfenster.

    :param station_code: Code der Station.
    :param start: Inklusive Untergrenze als zeitzonenbewusster datetime-Wert.
    :param end: Exklusive Obergrenze als zeitzonenbewusster datetime-Wert.
    :returns: Eine Liste von Dictionaries, eine Zeile je Sensor mit Messungen
        im Zeitfenster. Ohne passende Messungen ist die Liste leer.

    Voraussetzung: ``start < end``. Die Funktion prüft dies nicht selbst.
    Alle Qualitätskennzeichen fließen in die Auswertung ein.
    Die Funktion liest Daten aus PostgreSQL und führt keine Berechtigungsprüfung
    durch. Die aufrufende Schicht muss den Zugriff absichern.
    """
    with connection.cursor() as cursor:
        cursor.execute(
            SENSOR_HEALTH_SQL,
            [station_code, start, end],
        )

        return dictfetchall(cursor)
