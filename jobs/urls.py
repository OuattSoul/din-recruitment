from rest_framework.routers import DefaultRouter
from .views import JobOfferViewSet
from django.urls import path, include
router = DefaultRouter()
router.register(r"joboffers", JobOfferViewSet, basename="joboffers")

#urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
]