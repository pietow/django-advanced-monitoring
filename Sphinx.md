# Sphinx: Projekt anlegen und erste Seite bauen

Ziel dieses Abschnitts: Wir richten eine kleine Sphinx-Dokumentation im Projekt `django-advanced-monitoring` ein und erzeugen die erste HTML-Seite.

Dauer: ca. 8 Minuten.

---

## 1. Grundgerüst erzeugen

Wir legen mit einem Befehl den Grundaufbau der Dokumentation an. Sphinx erstellt dabei den Ordner `docs/` mit den Unterordnern `source/` (Quellen) und `build/` (fertige Ausgabe).

```powershell
python -m sphinx.cmd.quickstart -q -p "Monitoring" -a "Workshop-Team" --sep --no-makefile --no-batchfile docs
```

Was die Optionen bewirken:

- `--sep`: Quellen und Build-Ausgabe werden getrennt. Die Quellen liegen in `docs/source/`, die Ausgabe in `docs/build/`.
- `-q`: Sphinx stellt keine Rückfragen und verwendet die angegebenen Werte.
- `--no-makefile` und `--no-batchfile`: Wir bauen direkt mit Python. Makefiles brauchen wir dafür nicht.

Der Befehl erzeugt unter anderem `docs/source/conf.py` und `docs/source/index.rst`. Die generierte `conf.py` ersetzen wir im nächsten Schritt.

---

## 2. Konfiguration

Datei: `docs/source/conf.py`

Den generierten Inhalt ersetzen wir durch die folgende Konfiguration. Sie legt Pfad, Projektname und HTML-Theme fest. Die Zeilen zu `autodoc` und zum Django-Setup kommen in Abschnitt 4 genauer zur Sprache. 

```python
from pathlib import Path
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

project = "Monitoring"  # Projektname in Titel, Kopfzeile und Fußzeile
author = "Workshop-Team"  # Erscheint im Copyright-Hinweis
pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))  # Paket-Metadaten aus dem Packaging-Block
release = pyproject["project"]["version"]  # Version nur in pyproject.toml pflegen
language = "de"
extensions = ["sphinx.ext.autodoc"]  # Liest Docstrings direkt aus dem Code
html_theme = "alabaster"  # Standard-Theme von Sphinx, braucht kein Zusatzpaket
exclude_patterns = []  # Dateien, die Sphinx beim Einlesen ignoriert; aktuell keine
autodoc_typehints = "none"  # Type Hints weder in Signaturen noch in Beschreibungen anzeigen

# Eigene Dokumentations-Konfiguration. Keine produktiven Settings laden.
import django
from django.conf import settings

settings.configure(  # Minimale Settings nur für den Sphinx-Build, ohne DJANGO_SETTINGS_MODULE
    INSTALLED_APPS=[  # Nur die Apps, die zum Importieren der Monitoring-Module nötig sind
        "django.contrib.auth",  # Damit Station.owner auf das echte User-Model zeigt
        "django.contrib.contenttypes",  # Voraussetzung für auth (Permissions)
        "monitoring.apps.MonitoringConfig",  # Die zu dokumentierende App
    ],
)
django.setup()  # Lädt die App-Registry, damit autodoc die Models importieren kann
```

Wichtige Punkte zur Konfiguration:

- `ROOT` zeigt auf das Projektverzeichnis. Sphinx findet so das Paket `monitoring`.
- Die Dokumentation liest den aktuellen Quellcode. Ein Wheel-Installationsnachweis ist dafür nicht nötig.
- `release` wird aus `pyproject.toml` gelesen. Eine Versionsnummer pflegen wir nur an dieser Stelle.
- Im geprüften Stand steht dort noch `0.1.0rc1`. Benennen Sie die Version bitte nicht von Hand um.

**Denkanstoß:**

- Üblicher ist `importlib.metadata.version("<paketname>")`.
- Das funktioniert aber nur, wenn das Paket installiert ist, zum Beispiel mit `pip install -e .`.
- Wer `pyproject.toml` direkt liest, braucht das nicht, geht dafür aber vom Aufbau des Repositorys aus.
- Überlegen Sie: Welchen Weg würden Sie für ein Projekt wählen, und warum?

---

## 3. Erste Seite

Datei: `docs/source/index.rst`

Für den ersten Build verwenden wir nur diesen Inhalt:

```rst
Monitoring
==========

Dokumentation für Teams, die unsere Django-App verwenden.
```

Jetzt bauen wir die HTML-Dokumentation:

```powershell
python -m sphinx -b html -W --keep-going -n -E docs/source docs/build/html
```

Anschließend öffnen wir die Seite im Browser:

```powershell
Start-Process docs/build/html/index.html
```

**Erwartung:**

- Der Build endet mit Rückgabecode 0.
- Im Browser erscheint die erste Seite.

Die Optionen des Build-Befehls im Überblick:

| Option | Bedeutung |
| --- | --- |
| `-b html` | HTML erzeugen |
| `-W` | Warnungen führen zu einem fehlgeschlagenen Build |
| `--keep-going` | Weitere Probleme ebenfalls anzeigen |
| `-n` | Fehlende Querverweisziele melden |
| `-E` | Quellen vollständig neu einlesen |

Die Build-Ausgabe unter `docs/build/` gehört nicht ins Repository. Dafür ergänzen wir die `.gitignore`:

```gitignore
/docs/build/
```

---

## Checkliste

- [ ] `docs/source/conf.py` ist durch die Konfiguration ersetzt.
- [ ] `docs/source/index.rst` enthält nur den Titel und den Einleitungssatz.
- [ ] Der Build endet mit Rückgabecode 0.
- [ ] Die erste Seite erscheint im Browser.
- [ ] `/docs/build/` steht in der `.gitignore`.
