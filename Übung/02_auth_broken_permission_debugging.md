# Übung – Broken Permission Debugging

In der API gilt folgende fachliche Regel:

- anonyme Benutzer dürfen nicht auf die Stations-API zugreifen,
- authentifizierte Benutzer dürfen alle Stationen lesen,
- nur der verantwortliche Benutzer einer Station darf sie ändern oder löschen,
- Admins dürfen jede Station ändern oder löschen.

Die folgende Permission soll genau diese Regeln umsetzen, enthält aber mehrere Fehler:

```python
from rest_framework import permissions


class IsStationOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
```

## Aufgabe

Finden und beheben Sie die Fehler so, dass die Permission die oben beschriebenen Regeln korrekt umsetzt.

Testen Sie Ihre Lösung mindestens mit diesen Fällen:

| Benutzer | Request | Erwartung |
|---|---|---|
| anonym | `GET` | ❌ |
| authentifiziert, nicht Owner | `GET` | ✅ |
| authentifiziert, nicht Owner | `PATCH` | ❌ |
| Owner | `PATCH` | ✅ |
| Admin | `PATCH` auf fremde Station | ✅ |

> Denken Sie insbesondere darüber nach, wann `has_permission()` und wann `has_object_permission()` ausgeführt werden.
