# Sphinx: Report-Vertrag dokumentieren


## Auftrag

- Ein anderes Team möchte `get_sensor_health` tageweise verwenden.
- Es möchte benachbarte Zeitfenster auswerten.
- Dokumentieren Sie den Vertrag anhand des vorhandenen Codes.
- Begründen Sie Ihre Aussagen mit konkreten Stellen im Python-Code oder SQL.

## Arbeitsdateien im Livecode-Projekt

| Datei | Aufgabe |
| --- | --- |
| `monitoring/reports.py` | Docstring zu `get_sensor_health` ergänzen |
| `monitoring/sql/sensor_health.sql` | Verhalten nachlesen, nicht ändern |
| `docs/source/sensor-health.rst` | Kurze Nutzungsanleitung schreiben |
| `docs/source/index.rst` | Neue Seite im toctree eintragen |

## Core

- Zweck der Funktion in eigenen Worten beschreiben.
- Bedeutung der Argumente erklären.
- Zeitfenster anhand des SQL ableiten.
- Kurzes Beispiel mit zeitzonenbewussten Datumswerten schreiben.
- Ergebnis und mindestens eine fachliche Grenze erklären.
- Docstring mit `autofunction` auf der Seite einbinden.
- Mit `:ref:` auf die bereits gelabelte Installationsseite verweisen.
  Zum Nachschlagen: [Sphinx: Querverweise mit `:ref:`](https://www.sphinx-doc.org/en/master/usage/referencing.html#role-ref).
- Strengen HTML-Build ausführen.
- Seite im Browser über die Navigation aufrufen.
- Fachlogik und SQL erhalten.



## Ausführen

Im Livecode-Projekt mit aktivierter virtueller Umgebung:

```powershell
python -m sphinx -b html -W --keep-going -n -E docs/source docs/build/html
```

- Erwartung: Rückgabecode 0, keine Warnungen.
- Zusätzlich die fachlichen Aussagen und die Navigation selbst prüfen.
- Codeblöcke auf der Seite werden nicht ausgeführt.

