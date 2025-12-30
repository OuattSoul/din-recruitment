from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import JobOffer
from .serializers import JobOfferSerializer
from common.permissions import IsAdminOrReadOnly, IsAdmin


class JobOfferViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les offres d'emploi
    - GET: Tout le monde peut voir les offres publiées
    - POST/PUT/PATCH/DELETE: Seuls les admins
    """

    serializer_class = JobOfferSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]

    def get_queryset(self):
        """
        Les admins voient toutes les offres
        Les autres ne voient que les offres publiées
        """
        user = self.request.user
        if user.is_authenticated and user.role in ["admin", "superadmin"]:
            return JobOffer.objects.all()
        return JobOffer.objects.filter(status="published")

    def perform_create(self, serializer):
        """Enregistrer l'admin qui crée l'offre"""
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[IsAdmin])
    def my_offers(self, request):
        """Liste des offres créées par l'admin connecté"""
        offers = JobOffer.objects.filter(created_by=request.user)
        serializer = self.get_serializer(offers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def publish(self, request, pk=None):
        """Publier une offre"""
        offer = self.get_object()
        offer.status = "published"
        offer.save()
        return Response({"status": "Offre publiée"})

    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def close(self, request, pk=None):
        """Fermer une offre"""
        offer = self.get_object()
        offer.status = "closed"
        offer.save()
        return Response({"status": "Offre fermée"})
