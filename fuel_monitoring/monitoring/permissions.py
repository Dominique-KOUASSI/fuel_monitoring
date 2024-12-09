from rest_framework.permissions import BasePermission

# Creation d'une permission pour les super user
class IsAdminAuthenticated(BasePermission):
 
    def has_permission(self, request, view):
    # Ne donnons l’accès qu’aux utilisateurs administrateurs authentifiés
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)

# Creation d'une permission pour les microcontroleurs
class IsIotUserAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
    
# Permission pour accéder aux données restreintes
# Cette permission permet a l'utilisateur d'acceder aux donnees pour les afficher
class HasViewRestrictedDataPermission(BasePermission):

    def has_permission(self, request, view):
        # Vérifier si l'utilisateur a la permission 'view_restricted_data'
        return request.user.has_perm('monitoring.view_restricted_data')