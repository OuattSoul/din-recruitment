from rest_framework import viewsets
from .models import JobOffer
from .serializers import JobOfferSerializer

class JobOfferViewSet(viewsets.ModelViewSet):
    queryset = JobOffer.objects.all()
    serializer_class = JobOfferSerializer
