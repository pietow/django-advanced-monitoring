# Übung 04 – Migration Incident vor dem Release

## Szenario

Kurz vor einem Release schlägt die CI-Pipeline des Monitoring-Projekts fehl.

Zwei Feature-Branches wurden parallel auf demselben Migrationsstand entwickelt
und anschließend zusammengeführt. Zusätzlich enthält der Release eine Data
Migration sowie eine PostgreSQL-View.

Die Migrationen ab `0007` wurden **noch nicht in Produktion angewendet**.

Der Stand im Repository ist absichtlich konfliktbehaftet:

```text
monitoring/migrations/
    0007_station_region.py
    0007_sensor_calibration_offset.py
    0008_initialize_regional_calibration.py
    0009_active_calibrated_sensors_view.py
```

Die Datenbank selbst steht noch sauber auf:

```text
0006_active_station_codes_view
```

`models.py` enthält bereits den gewünschten fachlichen Endzustand.

Ihre Aufgabe ist es, den Release wieder migrationsfähig zu machen.

---

## Auftrag

Analysieren und reparieren Sie den vorhandenen Migrationsstand so, dass er als
Release Candidate akzeptiert werden kann.

Dabei sollen **keine neuen Fachfeatures** implementiert werden.

Sie dürfen bestehende Migrationen ab `0007` direkt verändern, umbenennen oder
zusammenführen. Das ist hier ausnahmsweise erlaubt, weil diese Migrationen
noch auf keinem anderen System angewendet wurden: Keine Datenbank hat sie in
`django_migrations` registriert.

Migrationen bis einschließlich `0006` bleiben unverändert. Sie sind bereits in diesem Szenario
produktiv angewendet.

Der reparierte Stand muss folgende Probleme lösen:

- Der Migration Graph besitzt nach dem Merge einen fachlich korrekten Pfad.
- Die Data Migration arbeitet mit dem historischen Model-State.
- Die Data Migration besitzt einen sinnvollen Rückwärtsweg.
- Die PostgreSQL-View und das dazugehörige unmanaged Model führen nicht zu
  einem Unterschied zwischen Database State und Project State.

---

## Ausgangspunkt

```bash
git switch exercise/migration-incident

python manage.py showmigrations monitoring
python manage.py migrate monitoring --plan
```

Analysieren Sie anschließend die neuen Migration Files selbst.

Hilfreiche Werkzeuge:

```bash
python manage.py showmigrations monitoring --plan
python manage.py migrate monitoring --plan
python manage.py sqlmigrate monitoring <migration>
python manage.py makemigrations --check --dry-run
```

> **Hinweis**
>
> Die Nummer einer Migration bestimmt nicht allein ihre Reihenfolge.
> Entscheidend ist, welchen State eine Migration benötigt.

---

## Fachliche Randbedingungen

`0008_initialize_regional_calibration` verwendet Daten aus:

```text
Station.region
Sensor.calibration_offset
```

Die beiden Felder wurden in den beiden parallelen `0007`-Migrationen
eingeführt.

Die Data Migration soll vorhandene Daten fachlich initialisieren.

Die PostgreSQL-View aus `0009_active_calibrated_sensors_view` soll weiterhin
durch `RunSQL` erstellt und beim Rollback wieder entfernt werden.

Im aktuellen Model-Code existiert bereits ein unmanaged Model für diese View:

```text
ActiveCalibratedSensor
```

---

## Abnahmekriterien

Der Release Candidate gilt als repariert, wenn alle folgenden Prüfungen
erfolgreich sind:

```bash
python manage.py showmigrations monitoring --plan
python manage.py migrate monitoring --plan
python manage.py makemigrations --check --dry-run
```

Danach müssen auch die Migrationen selbst funktionieren:

```bash
python manage.py migrate monitoring
python manage.py check
```

Erwartung:

```text
- alle neuen Migrationen wurden angewendet,
- Station.region ist für vorhandene Daten befüllt,
- Sensor.calibration_offset wurde initialisiert,
- ActiveCalibratedSensor ist über das ORM lesbar,
- makemigrations --check --dry-run meldet keine Änderung.
```

Prüfen Sie anschließend noch den Rückweg:

```bash
python manage.py migrate monitoring 0006 --plan
```

Sie müssen den Rollback nicht ausführen, aber der Plan muss plausibel sein.

---

## Review-Frage

Sie haben die fehlerhaften Migrationen in dieser Übung direkt korrigiert.

Warum wäre dieses Vorgehen problematisch, wenn `0007` oder spätere
Migrationen bereits auf Produktionssystemen angewendet worden wären?

