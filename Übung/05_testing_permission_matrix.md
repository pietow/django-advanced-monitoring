# Übung – Permission-Matrix mit pytest parametrisieren

## Ausgangslage

Für Stationen gelten im Workshop:

```text
anonymous
    → kein Zugriff

authenticated user
    → lesen erlaubt

owner
    → eigene Station ändern/löschen

staff
    → jede Station ändern/löschen
```

Eine parametrized Test-Matrix deckt bereits GET- und PATCH-Fälle ab.

## Dateien und Arbeitsordner

Aufgabenblatt im Kursunterlagen-Repository:

```text
docs/exercises/05_testing_permission_matrix.md
```

Im Livecode-Projekt `django-advanced-monitoring` die vorhandene Datei
`tests/api/test_station_permissions.py` ergänzen. Sie enthält bereits die
GET-/PATCH-Matrix; die DELETE-Fälle werden dort hinzugefügt.
Die benötigten Fixtures aus `tests/conftest.py` weiterverwenden.

## Auftrag

Erweitern Sie die Parametertabelle und die Request-Verzweigung um die DELETE-Fälle:

```text
other user + DELETE → 403
owner      + DELETE → 204
staff      + DELETE → 204
```

## Anforderungen

- `pytest.mark.parametrize` verwenden.
- Kein separater Test pro Rolle.
- Produktionscode nicht ändern.
- DRFs `APIClient` weiterverwenden.
- Jeder Parametersatz muss isoliert ausführbar sein.
- Kein Test darf vom Datenbankzustand eines vorherigen Parametersatzes abhängen.
- GET, PATCH und DELETE jeweils ausdrücklich behandeln.
- Unbekannte Methoden müssen mit `pytest.fail(...)` zum Fehlschlag führen; keinen unterstützten Request als pauschalen `else`-Fallback verwenden.

## Denkfrage

Warum beeinflussen sich erfolgreiche DELETE-Fälle nicht, obwohl die Station dabei gelöscht wird?

## Ausführen

```powershell
pytest tests\api\test_station_permissions.py -q
```
