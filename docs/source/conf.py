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

