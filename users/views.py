from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .models import User
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    AdminRegistrationSerializer,
    CandidateProfileSerializer
)
from common.permissions import IsSuperAdmin


class UserViewSet(ModelViewSet):
    """
    ViewSet pour la gestion des utilisateurs
    - Superadmins: gestion complète
    - Admins: lecture uniquement
    - Candidats: accès à leur propre profil
    """

    def get_serializer_class(self):
        if self.action == 'register':
            return UserRegistrationSerializer
        elif self.action == 'create_admin':
            return AdminRegistrationSerializer
        elif self.action in ['profile', 'update_profile']:
            return CandidateProfileSerializer
        return UserSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == "superadmin":
            return User.objects.all()
        elif user.role == "admin":
            return User.objects.filter(role="candidate")
        else:
            return User.objects.filter(id=user.id)

    def get_permissions(self):
        if self.action == 'register':
            return [AllowAny()]
        elif self.action in ['create_admin', 'destroy']:
            return [IsAuthenticated(), IsSuperAdmin()]
        elif self.action in ['profile', 'update_profile']:
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """Inscription publique pour les candidats"""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "Inscription réussie", "user_id": user.id},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated, IsSuperAdmin])
    def create_admin(self, request):
        """Création d'un admin/superadmin (réservé aux superadmins)"""
        serializer = AdminRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": f"{user.get_role_display()} créé avec succès", "user_id": user.id},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Récupérer le profil de l'utilisateur connecté"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """Mettre à jour le profil de l'utilisateur connecté"""
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

