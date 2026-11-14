# Übung 1 – Beziehungen mit DRF serialisieren


Erstellen Sie in

```text
monitoring/api/serializers.py
```

einen `SensorSerializer` und einen `StationSerializer`.

## Aufgabe

Der `StationSerializer` soll ungefähr folgende Struktur erzeugen:

```json
{
  "id": 1,
  "code": "DEMO-ALPINE-01",
  "name": "Alpine Ridge",
  "owner": 1,
  "elevation_m": 1840.0,
  "tags": [
    "alpine",
    "research"
  ],
  "sensors": [
    {
      "id": 1,
      "name": "Air temperature",
      "sensor_type": "temperature",
      "unit": "°C",
      "active": true
    }
  ]
}
```

Verwenden Sie dabei:

- `ModelSerializer`
- `PrimaryKeyRelatedField` für `owner`
- `SlugRelatedField` für `tags`
- einen verschachtelten `SensorSerializer` für `sensors`
- `source` für `elevation_m`

Die Relationsfelder können zunächst **read-only** sein.

## Testen

Öffnen Sie die Django-Shell:

```bash
python manage.py shell
```

und testen Sie Ihren Serializer:

```python
from monitoring.models import Station
from monitoring.api.serializers import StationSerializer

station = Station.objects.get(code="DEMO-ALPINE-01")

StationSerializer(station).data
```

## Bonus

Der Kernauftrag ist ohne diesen Zusatz
vollständig. Die benötigte Feldmethode wurde vor der Übung eingeführt.

Ergänzen Sie den `SensorSerializer` um das Feld:

```text
measurement_count
```

Verwenden Sie dafür ein `SerializerMethodField`.

Die Anzahl der Messungen können Sie zunächst mit

```python
obj.measurements.count()
```

ermitteln.

## Challenge

**Optional, aufbauend auf dem Übungsbonus.** Benennen und begründen Sie nur
mögliche zusätzliche Datenbankzugriffe. Queryzahlen müssen nicht gemessen und
QuerySets nicht optimiert werden.

Serialisieren Sie anschließend alle Stationen:

```python
stations = Station.objects.all()

StationSerializer(
    stations,
    many=True,
).data
```

Überlegen Sie:

> Welches Performanceproblem könnte bei dieser Implementierung entstehen?

Optimieren Sie die Abfrage noch nicht. Identifizieren Sie nur die Ursache.
