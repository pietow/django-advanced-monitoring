# Fortgeschrittener Django-Workshop: Monitoring

Ausgangsprojekt für den zweitägigen Workshop.
Python 3.14, Django 5.2, Django REST Framework und PostgreSQL.

## Lokal starten

Django läuft in einer lokalen `venv`; Docker Compose stellt PostgreSQL 17 bereit.
In PowerShell:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
docker compose up -d --wait db
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Unter Linux/macOS stattdessen `python3.14 -m venv .venv` und `source .venv/bin/activate` verwenden.
Die Admin-Oberfläche ist unter <http://127.0.0.1:8000/admin/> erreichbar. API-Endpunkte gibt es noch nicht.

Die Konfiguration liegt in `.env`. Die Vorlage `.env.example` enthält Werte für
den lokalen Workshop; unter Linux/macOS mit `cp .env.example .env` kopieren.
Eine vorhandene `.env` beim erneuten Setup beibehalten.
Django und Docker Compose laden diese Datei automatisch. Bereits gesetzte
Umgebungsvariablen in der Shell haben Vorrang. Fehlende oder leere Pflichtwerte
führen zu einem Fehler; in den Einstellungen gibt es keine Ersatzwerte.
Die lokale `.env` ist von Git ausgeschlossen.

`DJANGO_DEBUG` verwendet `1` oder `0`, `DJANGO_ALLOWED_HOSTS` eine durch Kommas
getrennte Liste. Zugangsdaten und Schlüssel in der Vorlage sind ausschließlich
für die lokale Entwicklung vorgesehen.

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
```

Mit `docker compose stop` wird PostgreSQL gestoppt; die Daten bleiben im benannten Volume erhalten.

## Demo-Daten

Der Seeder erzeugt einen deterministischen Datensatz für den Workshop. Er kann nur
bei `DJANGO_DEBUG=1` ausgeführt werden:

```powershell
python manage.py seed_demo_data
```

Wenn Demo-Stationen bereits vorhanden sind, bricht der Befehl ohne Änderungen ab.
Mit `--reset` werden ausschließlich Stationen mit dem reservierten `DEMO-`-Präfix
und deren abhängige Daten ersetzt; Benutzer und Tags werden nicht gelöscht:

```powershell
python manage.py seed_demo_data --reset
```

Für Abfragen und Performance-Übungen kann der Seeder etwa 1.000 Messungen pro
messendem Sensor erzeugen:

```powershell
python manage.py seed_demo_data --reset --large
```

## Struktur und Umfang

- `config/`: Einstellungen, URL-Konfiguration sowie ASGI- und WSGI-Einstiegspunkte.
- `monitoring/`: die fünf Domänenmodelle, Registrierung in der Admin-Oberfläche,
  initiale Migration.
- `compose.yaml`: lokaler PostgreSQL-Dienst.

## Modelle und Beziehungen

Eine `Station` ist eine Messstation mit Standort und Besitzer (`User`).
`StationMetadata` ergänzt optionale Angaben wie Höhe, Betreiber und Installationsdatum.
Ein `Sensor` gehört zu einer Station und erfasst Messwerte (`Measurement`) mit
Zeitstempel und Qualitätskennzeichnung. `Tag` dient zur Einordnung von Stationen.

| Modell | Beziehung | Zielmodell | Django-Feld |
| --- | --- | --- | --- |
| `Station` | N:1 | `User` | `ForeignKey` |
| `StationMetadata` | 1:1 | `Station` | `OneToOneField` |
| `Station` | M:N | `Tag` | `ManyToManyField` |
| `Sensor` | N:1 | `Station` | `ForeignKey` |
| `Measurement` | N:1 | `Sensor` | `ForeignKey` |

**N:1** bedeutet: Mehrere Datensätze können demselben Zielobjekt zugeordnet sein.
**1:1** bedeutet hier: Jede Station kann höchstens einen Metadatensatz haben.
**M:N** bedeutet: Eine Station kann mehrere Tags haben, und ein Tag kann mehreren
Stationen zugeordnet sein.

