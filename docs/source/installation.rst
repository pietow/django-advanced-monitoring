.. _installation:

Installation und Einbindung
===========================

Voraussetzungen
---------------

* Python 3.14, Django 5.2 und DRF 3.17.
* PostgreSQL für den Betrieb der App.
* Ein geprüftes Wheel aus dem Packaging-Block.

Paket installieren
------------------

Den Platzhalter durch den Pfad zum geprüften Wheel ersetzen:

.. code-block:: powershell

   python -m pip install "<Pfad-zum-geprueften-Wheel>"

Für PostgreSQL benötigt das Projekt zusätzlich den Treiber psycopg.

App einbinden
-------------

Im betreibenden Projekt bleiben die vorhandenen Django-Apps erhalten.
Die Monitoring-App und die benötigten DRF-Apps ergänzen:

.. code-block:: python

   INSTALLED_APPS += [
       "rest_framework",
       "rest_framework.authtoken",
       "monitoring.apps.MonitoringConfig",
   ]

Die Token-App gehört zur hier verwendeten Authentifizierung.

Authentifizierung festlegen
---------------------------

Im betreibenden Projekt ergänzen:

.. code-block:: python

   REST_FRAMEWORK = {
       "DEFAULT_AUTHENTICATION_CLASSES": [
           "rest_framework.authentication.TokenAuthentication",
           "rest_framework.authentication.SessionAuthentication",
       ],
       "DEFAULT_PERMISSION_CLASSES": [
           "rest_framework.permissions.IsAuthenticated",
       ],
   }

API-URLs einbinden
------------------

In der URL-Konfiguration des betreibenden Projekts:

.. code-block:: python

   from django.urls import include, path

   urlpatterns += [
       path("api/", include("monitoring.api.urls")),
   ]

Datenbank vorbereiten
---------------------

Das Projekt stellt Datenbank und Zugangsdaten bereit.
Die Installation des Wheels legt noch keine Tabellen an.

Nach Konfiguration der Zieldatenbank:

.. code-block:: powershell

   python manage.py migrate

.. note::

   Die Projekt-Settings und Zugangsdaten gehören nicht zum Paket.
   Demo-Daten sind optional und gehören nicht zur Installation.
