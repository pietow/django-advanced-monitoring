# Übung – Django-Datenbanktests und pytest-Fixtures

## Ausgangslage

Im Workshop existieren bereits die Fixtures:

```text
user
station
```

Die Tests laufen mit pytest und pytest-django.

## Dateien und Arbeitsordner

Aufgabenblatt im Kursunterlagen-Repository:

```text
docs/exercises/05_testing_db_fixtures.md
```

Die folgenden Python-Pfade beziehen sich auf den Projektordner
`django-advanced-monitoring` mit `manage.py`:

| Datei | Aufgabe |
| --- | --- |
| `tests/conftest.py` | Bestehende Datei um `other_user` und `other_station` ergänzen. |
| `tests/integration/test_station_fixtures.py` | Bestehende Datei um den DB-Test für beide Stationen ergänzen. |

Vorgesehener Git-Ausgangsstand vor dieser Übung: `11-testing-fixtures`.

## Auftrag

Ergänzen Sie:

1. eine Fixture `other_user`,
2. eine Fixture `other_station`, deren Owner `other_user` ist,
3. einen Integrationstest, der nachweist:
   - beide Stationen existieren in der Testdatenbank,
   - sie gehören unterschiedlichen Benutzern,
   - ihre Stationscodes unterscheiden sich.

## Regeln

- Verwenden Sie echte Django-Models und die Testdatenbank.
- Verwenden Sie keine Daten aus `seed_demo_data`.
- Der Test muss unabhängig von anderen Tests laufen.

## Start

```powershell
pytest tests\integration -q
```

## Ziel

```text
Fixture-Komposition
+
Django ORM
+
isolierte Testdatenbank
```
