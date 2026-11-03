from django.contrib.auth.models import AbstractUser
from rest_framework import permissions

class IsStationOwnerOrReadOnly(permissions.BasePermission):
    """Erlaube angemeldeten Benutzern das Lesen von Stationen.

    Anonyme Requests werden abgewiesen.
    Ändern und Löschen sind dem Besitzer und Staff vorbehalten.
    Die View muss die Objektberechtigungen tatsächlich aufrufen.
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if isinstance(request.user, AbstractUser) and request.user.is_staff:
            return True
        return obj.owner == request.user