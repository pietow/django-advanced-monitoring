# Übung 2 – Nested Update implementieren und den PATCH-Vertrag prüfen


Ein Client möchte den Betreiber einer Station ändern und die hinterlegte Höhe
beibehalten. Implementieren Sie dafür die verschachtelte Update-Logik und prüfen
Sie anschließend die HTTP-Antworten und den gespeicherten Zustand.

## Vorbereitung

- Arbeiten Sie im Livecode-Projekt auf dem bereitgestellten Übungsstand nach
  dem Nested-`create()`.
- POST und PATCH verwenden bereits `StationNestedWriteSerializer`. Der
  Serializer erbt von `StationWriteSerializer` und bindet
  `StationMetadataWriteSerializer` ein. PATCH verwendet `partial=True`.
- Die eigene Methode `create()` ist vorhanden; eine eigene Methode `update()`
  fehlt noch in `StationNestedWriteSerializer`. Genau diese Methode ist Ihr
  Implementierungsauftrag.
- Der lokale Django-Server läuft. Wählen Sie in Postman für die Request-Bodies
  **raw → JSON** und verwenden Sie `Content-Type: application/json`.
- Verwenden Sie pro Paar einen eigenen Stationscode und bei einem erneuten POST
  einen weiteren freien Code.

## 1. Nested Update implementieren

Ergänzen Sie in `monitoring/api/serializers.py` innerhalb von
`StationNestedWriteSerializer` unter `create()` die Methode
`update(self, instance, validated_data)`. Geben Sie die aktualisierte
Stationsinstanz zurück.

Setzen Sie folgenden Vertrag um:

| Eingabe im PATCH | Gewünschtes Verhalten |
| --- | --- |
| Stationsfelder, beispielsweise `active` | Nur die gelieferten Stationsfelder aktualisieren. |
| `metadata` fehlt | Vorhandene Metadaten unverändert lassen; kein fehlendes Child anlegen. |
| `metadata` enthält einzelne Felder | Nur diese Metadatenfelder ändern; alle anderen erhalten. Falls das Child fehlt, es anlegen. |
| `metadata: {}` | Vorhandene Metadaten unverändert lassen; ein fehlendes Child mit Model-Defaults anlegen. |
| `metadata: null` oder ungültige Metadatenwerte | Die bereits vorhandene Validierung lehnt die Eingabe ab; auch gültige Stationsänderungen aus demselben Request dürfen nicht gespeichert werden. |

Nutzen Sie nur `validated_data` für die Schreiblogik. Trennen Sie die
Metadaten von den Stationsfeldern, bevor Sie die Aktualisierung der Station an
die geerbte Methode delegieren. Eine Station darf ohne Metadatensatz existieren.

Ändern Sie nur `StationNestedWriteSerializer.update()` und ergänzen Sie bei
Bedarf den Modellimport für `StationMetadata`. Die vorhandenen Validatoren,
`create()`, Models und Views werden für diese Aufgabe nicht geändert.

**Hinweise:** `super().update()` übernimmt die
Stationsfelder. `get_or_create()` kann ein vorhandenes Child laden oder ein
fehlendes anlegen. Mit `setattr()` lassen sich die gelieferten Child-Felder setzen.

## 2. Station anlegen

Speichern Sie Ihre Implementierung und prüfen Sie, ob der Server ohne
Import- oder Syntaxfehler neu geladen hat.

Senden Sie `POST /api/stations/`. Ersetzen Sie `PATCH-TEAM-01` durch Ihren eigenen
Stationscode und notieren Sie die `id` aus der Antwort.

```json
{
  "code": "PATCH-TEAM-01",
  "name": "Übungsstation",
  "latitude": "47.421000",
  "longitude": "11.231000",
  "active": true,
  "metadata": {
    "operator": "Messnetz Nord",
    "elevation_m": 1840.0
  }
}
```

## 3. Zwei gültige Änderungen prüfen

Senden Sie beide Requests nacheinander an dieselbe Station
(`PATCH /api/stations/<id>/`). Prüfen Sie, ob Ihre Implementierung den Vertrag
aus Aufgabe 1 erfüllt: Beide Requests müssen HTTP **200 OK** liefern.
Notieren Sie nach jedem Request den tatsächlichen HTTP-Status und die frisch
geladenen Werte für `active`, `operator` und `elevation_m`. Vergleichen Sie
diesen Istzustand mit dem vorgegebenen Sollverhalten. Bei Abweichungen
korrigieren Sie Ihre Implementierung und wiederholen die Prüfung mit einem
eindeutig bekannten Ausgangszustand.

| Fall | JSON-Body | Prüfkriterium aus dem Vertrag |
| --- | --- | --- |
| Nur den Betreiber ändern | `{"metadata": {"operator": "Feldteam Süd"}}` | Der Betreiber ändert sich; Höhe und Aktivstatus bleiben erhalten. |
| Die Station deaktivieren und `metadata` weglassen | `{"active": false}` | Die Station wird deaktiviert; beide Metadatenwerte bleiben erhalten. |

Lesen Sie nach jedem Request die Station frisch aus der Datenbank. Öffnen Sie
dafür `python manage.py shell -i ipython` im Livecode-Projekt. Ersetzen Sie das
Code-Feld durch Ihren eigenen und führen Sie den Zugriff bei jeder Kontrolle erneut aus.

```python
from monitoring.models import Station

station = Station.objects.get(code="PATCH-TEAM-01")
print(station.active, station.metadata.operator, station.metadata.elevation_m)
```

## 4. Einen Fehlerfall selbst entwerfen

1. Lesen Sie die aktuellen Werte der Station und ihrer Metadaten aus der Datenbank.
2. Entwerfen Sie einen PATCH, der `active` auf einen anderen Wert setzt und
   gleichzeitig eine ungültige Eingabe für `metadata`, `operator` oder
   `elevation_m` enthält. Stellen Sie sicher, dass die Änderung an `active`
   tatsächlich vom zuvor ausgelesenen Wert abweicht.
3. Senden Sie den Request und prüfen Sie, ob die API mit HTTP **400 Bad Request**
   und einem Fehler am ungültigen Feld antwortet. Lesen Sie Station und Metadaten
   erneut aus der Datenbank. Weisen Sie durch den Vorher-nachher-Vergleich nach,
   dass auch die gültige Änderung an `active` nicht gespeichert wurde.

Dokumentieren Sie für die beiden gültigen Requests und Ihren Fehlerfall jeweils:

- die geprüfte Regel aus Aufgabe 1,
- den tatsächlichen HTTP-Status und die relevanten Datenbankwerte,
- ob die Regel erfüllt ist oder welche Abweichung Sie korrigiert haben.

## Bonus: Fehlendes Child und leeres Objekt nachweisen

Die Behandlung dieser Fälle gehört zum Implementierungsauftrag. Prüfen Sie
zusätzlich per HTTP und Datenbank, ob Ihre Lösung beide korrekt unterscheidet:

Legen Sie eine zweite Station ohne Metadaten an. Senden Sie zuerst einen PATCH
ohne `metadata` und anschließend einen PATCH mit `{"metadata": {}}`.
Weisen Sie nach, dass der erste Request keinen Metadatensatz anlegt und der
zweite einen Metadatensatz mit Model-Defaults erzeugt.

Importieren Sie `StationMetadata` aus `monitoring.models`. Prüfen Sie vor dem
ersten Request und nach jedem der beiden Requests mit
`StationMetadata.objects.filter(station_id=...).exists()`, ob ein
Metadatensatz vorhanden ist. Ersetzen Sie `...` durch die ID der zweiten Station.

Erklären Sie anhand Ihrer Methode `update()`, weshalb die Unterscheidung zwischen
fehlendem Schlüssel und leerem Dictionary wichtig ist. Falls Sie
`if metadata_data is not None:` verwenden: Wie würde sich `if metadata_data:`
auf Ihren zweiten Request auswirken?
