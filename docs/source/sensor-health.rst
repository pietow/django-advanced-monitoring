.. _sensor-health-report:

Sensor-Health-Report verwenden
==============================

Vorbereitung
------------

Zuerst :ref:`installation` abschließen.

Zeitfenster
-----------

Der Start gehört zum Intervall, das Ende nicht: ``start <= timestamp < end``.
Benachbarte Zeitfenster zählen eine Messung an der gemeinsamen Grenze deshalb
nicht doppelt.

.. code-block:: python

   from datetime import datetime, timezone
   from monitoring.reports import get_sensor_health

   rows = get_sensor_health(
       "DEMO-STATION-01",
       datetime(2025, 1, 1, tzinfo=timezone.utc),
       datetime(2025, 1, 2, tzinfo=timezone.utc),
   )

   for row in rows:
       print(row["sensor_name"], row["measurement_count"])

Das Beispiel ist eine Leseabfrage auf der konfigurierten Datenbank.
Passende Messungen müssen dort vorhanden sein.

Ergebnis
--------

* Eine Ergebniszeile je Sensor mit Messungen im Zeitfenster.
* Schlüssel: ``station_code``, ``sensor_id``, ``sensor_name``,
  ``measurement_count``, ``average_value``, ``last_value``,
  ``last_measurement``.
* Sensoren ohne Messungen im Intervall fehlen im Ergebnis.
* Ohne Treffer kommt eine leere Liste zurück.

Grenzen
-------

* Der Aufrufer muss ``start < end`` sicherstellen.
* Die Funktion führt keine Berechtigungsprüfung aus.
* Alle Qualitätskennzeichen werden berücksichtigt.
* Im Python-Aufruf ergibt ein unbekannter Stationscode eine leere Liste.
  Der HTTP-Endpunkt kann stattdessen bereits vor dem Report mit 404 antworten.

.. autofunction:: monitoring.reports.get_sensor_health
