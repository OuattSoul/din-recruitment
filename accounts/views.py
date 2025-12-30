from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Account
from .serializers import AccountRegistrationSerializer, AccountSerializer, AccountUpdateSerializer
from common.permissions import IsAdmin


class AccountViewSet(ModelViewSet):
    """
    ViewSet pour la gestion des comptes

    Endpoints:
    - GET    /api/accounts/          - Liste tous les comptes
    - POST   /api/accounts/          - Créer un nouveau compte (public)
    - GET    /api/accounts/<id>/     - Récupérer un compte
    - PATCH  /api/accounts/<id>/     - Mettre à jour un compte
    - DELETE /api/accounts/<id>/     - Supprimer un compte (soft delete)

    Permissions:
    - Liste/Create: Authentifié (create aussi public via register)
    - Retrieve/Update/Delete: Propriétaire ou Admin
    """

    queryset = Account.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Utiliser le bon serializer selon l'action"""
        if self.action in ['update', 'partial_update']:
            return AccountUpdateSerializer
        elif self.action == 'create':
            return AccountRegistrationSerializer
        return AccountSerializer

    def get_permissions(self):
        """
        Permissions personnalisées selon l'action
        - create (register): Public
        - list: Authentifié
        - retrieve/update/partial_update/destroy: Propriétaire ou Admin
        """
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """
        Admins voient tous les comptes
        Utilisateurs voient uniquement leur propre compte
        """
        user = self.request.user
        if user.is_authenticated and user.role in ['admin', 'superadmin']:
            return Account.objects.filter(is_active=True)
        elif user.is_authenticated:
            return Account.objects.filter(id=user.id, is_active=True)
        return Account.objects.none()

    def create(self, request, *args, **kwargs):
        """Créer un nouveau compte (inscription publique)"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.save()

        response_serializer = AccountSerializer(account)
        return Response({
            "message": "Compte créé avec succès",
            "account": response_serializer.data
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        """Récupérer un compte par ID"""
        instance = self.get_object()

        # Vérifier les permissions
        if not self._has_permission(request.user, instance):
            raise PermissionDenied("Vous n'avez pas la permission d'accéder à ce compte")

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """Mettre à jour un compte (PUT)"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Vérifier les permissions
        if not self._has_permission(request.user, instance):
            raise PermissionDenied("Vous n'avez pas la permission de modifier ce compte")

        # Les utilisateurs non-admins ne peuvent pas modifier le rôle
        is_admin = request.user.role in ['admin', 'superadmin']
        if not is_admin and 'role' in request.data:
            raise PermissionDenied("Vous ne pouvez pas modifier votre rôle")

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_serializer = AccountSerializer(instance)
        return Response({
            "message": "Compte mis à jour avec succès",
            "account": response_serializer.data
        })

    def partial_update(self, request, *args, **kwargs):
        """Mettre à jour partiellement un compte (PATCH)"""
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Supprimer un compte (soft delete)"""
        instance = self.get_object()

        # Vérifier les permissions
        if not self._has_permission(request.user, instance):
            raise PermissionDenied("Vous n'avez pas la permission de supprimer ce compte")

        # Soft delete
        instance.is_active = False
        instance.save()

        return Response({
            "message": "Compte supprimé avec succès"
        }, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        """Lister les comptes"""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            "count": queryset.count(),
            "accounts": serializer.data
        })

    def _has_permission(self, user, account):
        """Vérifier si l'utilisateur a la permission d'accéder/modifier le compte"""
        is_admin = user.role in ['admin', 'superadmin']
        is_owner = user.id == account.id
        return is_admin or is_owner


# Garder la fonction register pour la rétrocompatibilité
@api_view(['POST'])
@permission_classes([AllowAny])
def register_account(request):
    """
    Endpoint pour créer un nouveau compte (PUBLIC) - DEPRECATED
    Utilisez POST /api/accounts/ à la place

    POST /api/accounts/register/
    """
    serializer = AccountRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        account = serializer.save()
        response_serializer = AccountSerializer(account)

        return Response({
            "message": "Compte créé avec succès",
            "account": response_serializer.data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
