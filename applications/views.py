from django.shortcuts import render
from django.db.models import Q, Count, Case, When, IntegerField
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Application
from .serializers import ApplicationSerializer
from .filters import ApplicationFilter
from common.permissions import IsAdmin, IsOwnerOrAdmin


class ApplicationViewSet(ModelViewSet):
    """
    ViewSet pour les candidatures
    - Candidats: peuvent créer et voir leurs propres candidatures
    - Admins: peuvent voir toutes les candidatures et modifier les statuts
    """

    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ApplicationFilter
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = ['created_at', 'updated_at', 'status']

    def get_queryset(self):
        """
        Admins voient toutes les candidatures
        Candidats voient uniquement leurs candidatures
        """
        user = self.request.user
        if user.role in ["admin", "superadmin"]:
            return Application.objects.all().select_related('candidate', 'job')
        return Application.objects.filter(candidate=user).select_related('job')

    def get_permissions(self):
        """
        - create: Seulement les candidats
        - update/partial_update: Admins ou propriétaire
        - destroy: Admins ou propriétaire (si status=pending)
        """
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """Associer la candidature au candidat connecté"""
        if self.request.user.role != "candidate":
            raise PermissionDenied("Seuls les candidats peuvent postuler")
        serializer.save(candidate=self.request.user)

    def perform_update(self, serializer):
        """
        Les candidats ne peuvent modifier que certains champs
        Les admins peuvent modifier le statut
        """
        user = self.request.user
        if user.role in ["admin", "superadmin"]:
            serializer.save()
        else:
            # Les candidats ne peuvent modifier que si status=pending
            instance = self.get_object()
            if instance.status != "pending":
                raise PermissionDenied("Vous ne pouvez plus modifier cette candidature")
            # Empêcher la modification du statut
            serializer.save(status=instance.status)

    def perform_destroy(self, instance):
        """
        Les candidats peuvent supprimer uniquement si status=pending
        """
        user = self.request.user
        if user.role not in ["admin", "superadmin"]:
            if instance.status != "pending":
                raise PermissionDenied("Vous ne pouvez supprimer que les candidatures en attente")
        instance.delete()

    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def review(self, request, pk=None):
        """Marquer une candidature comme revue"""
        application = self.get_object()
        application.status = "reviewed"
        application.save()
        return Response({"status": "Candidature marquée comme revue"})

    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def accept(self, request, pk=None):
        """Accepter une candidature"""
        application = self.get_object()
        application.status = "accepted"
        application.save()
        return Response({"status": "Candidature acceptée"})

    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def reject(self, request, pk=None):
        """Rejeter une candidature"""
        application = self.get_object()
        application.status = "rejected"
        application.save()
        return Response({"status": "Candidature rejetée"})

    @action(detail=False, methods=['get'], permission_classes=[IsAdmin])
    def dashboard_stats(self, request):
        """
        Statistiques pour le dashboard admin
        - total: nombre total de candidatures
        - spontanées: nombre de candidatures spontanées
        - sur_offres: nombre de candidatures sur les offres d'emploi
        - interim: nombre de candidatures pour contrat intérim
        - evaluations: nombre de candidatures en évaluation (status=reviewed)
        """
        queryset = Application.objects.all()

        stats = {
            'total': queryset.count(),
            'spontanees': queryset.filter(is_spontaneous=True).count(),
            'sur_offres': queryset.filter(is_spontaneous=False).count(),
            'interim': queryset.filter(contract_type_sought='interim').count(),
            'evaluations': queryset.filter(status='reviewed').count(),
        }

        return Response(stats)

