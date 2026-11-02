# django-workshop-monitoring

Django-App `monitoring` für Messstationen, Sensoren und Messwerte mit REST-API.

- Distribution: `django-workshop-monitoring`
- Importpaket: `monitoring`

## Voraussetzungen

- Python 3.14, Django 5.2, Django REST Framework 3.17
- PostgreSQL (die Reports verwenden PostgreSQL-spezifisches SQL)

## Installation

```bash
pip install "django-workshop-monitoring[postgres]"
```

`[postgres]` installiert den Treiber psycopg.

## Einbinden

`settings.py`:

```python
INSTALLED_APPS += [
    "rest_framework",
    "rest_framework.authtoken",  # nur bei Token-Authentifizierung; z.b. unnötig bei SessionAuthentication oder JWT
    "monitoring.apps.MonitoringConfig",
]
```

Authentifizierung und Permissions in `REST_FRAMEWORK` selbst festlegen. Die App bringt keine Projekt-Settings mit.

`urls.py`:

```python
path("api/", include("monitoring.api.urls")),
```

## Datenbank

```bash
python manage.py migrate
```

Die Installation legt keine Tabellen an. Datenbank und Zugangsdaten stellt das Projekt.

## Demo-Daten (optional)

```bash
python manage.py seed_demo_data
```

Nur bei `DEBUG = True`. Nicht Teil der Installation.

## Lizenz

Siehe `LICENSE`.
