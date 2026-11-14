# Übung: Package





## Arbeitsauftrag

> Ein anderes Team hat unser Wheel `0.1.0rc1` installiert und in sein Django-Projekt eingebunden. Bei `python manage.py check` erhält es die Fehlermeldung unten. Im Quellprojekt sind alle Tests grün.
>
> Findet die Ursache, korrigiert die Auslieferung und weist am neuen Wheel nach, dass der Fehler behoben ist.

Fehlermeldung des anderen Teams (gekürzt):

```text
> python manage.py check
Traceback (most recent call last):
  ...
  File "...\.venv\Lib\site-packages\monitoring\api\views.py", line …, in <module>
    from monitoring.reports import get_sensor_health
  File "...\.venv\Lib\site-packages\monitoring\reports.py", line …, in <module>
  ...
FileNotFoundError: [Errno 2] No such file or directory
```

**Wichtig: Kein Verbraucherprojekt anlegen und das Wheel nicht installieren.** Die Ursache lässt sich allein aus der Fehlermeldung, dem Quellcode und dem Wheel-Inhalt finden. Das Verbraucherprojekt bauen wir nach der Übung gemeinsam auf.

## Arbeitsorte und Rahmenbedingungen

- Nur im Quellprojekt `django-advanced-monitoring` arbeiten, `.venv` aktiv.
- Erlaubte Befehle: `python -m pytest -q`, `python -m build`, `python -m zipfile -l <wheel>`.
- Keine editable Installation und keine absoluten Pfade ins Quellprojekt als vermeintliche Reparatur.
- Fachlogik, API-Vertrag und Migrationen nicht ändern.


1. **Ursache finden – nur durch Lesen:**
    - Welches Modul scheitert laut Fehlermeldung?
    - Welche Datei liest dieses Modul beim Import? (Quellcode öffnen.)
    - Ist diese Datei im Wheel `0.1.0rc1`? (`python -m zipfile -l`)
2. **Korrigieren:** `pyproject.toml` anpassen, Version auf `0.1.0` setzen, Tests ausführen, neu bauen.
    - Die Syntax steht in der setuptools-Doku: [Data Files Support](https://setuptools.pypa.io/en/latest/userguide/datafiles.html). Nachschlagen ist ausdrücklich erlaubt.
3. **Nachweisen:** Inhalt des neuen Wheels `0.1.0` mit `python -m zipfile -l` prüfen. Die fehlende Datei muss jetzt enthalten sein.

## Hilfen

1. „Öffnet `monitoring/reports.py`. Was passiert dort beim Import?“
2. „Vergleicht die Liste aus `python -m zipfile -l` mit dem Ordner `monitoring/` im Quellprojekt. Welche Dateien fehlen?“
3. „Wer entscheidet, welche Dateien in ein Wheel gelangen? Welche Rolle spielt die Endung der Datei?“
4. Für die Syntax, nur wenn die Ursache schon klar ist – Gerüst ohne Werte:

```toml
[tool.setuptools.package-data]
<importpaket> = ["<pfad/muster>"]
```

„Der Pfad ist relativ zum Paketordner, Platzhalter wie `*` sind erlaubt.“


