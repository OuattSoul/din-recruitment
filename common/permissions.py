from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSuperAdmin(BasePermission):
    """
    Permission pour les super admins uniquement
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == "superadmin"

class IsAdmin(BasePermission):
    """
    Permission pour les admins et super admins
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role in ["admin", "superadmin"]

class IsCandidate(BasePermission):
    """
    Permission pour les candidats uniquement
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == "candidate"

class IsAdminOrReadOnly(BasePermission):
    """
    Les admins peuvent tout faire, les autres peuvent seulement lire
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        return request.user.role in ["admin", "superadmin"]

class IsOwnerOrAdmin(BasePermission):
    """
    L'utilisateur doit être propriétaire de l'objet ou admin
    """
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        # Les admins ont tous les droits
        if request.user.role in ["admin", "superadmin"]:
            return True

        # Vérifier si l'objet a un attribut 'candidate' ou 'user'
        if hasattr(obj, 'candidate'):
            return obj.candidate == request.user
        if hasattr(obj, 'user'):
            return obj.user == request.user

        return obj == request.user
