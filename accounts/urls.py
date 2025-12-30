from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .authentication import login_with_email

# Router pour les endpoints RESTful
router = DefaultRouter()
router.register('', views.AccountViewSet, basename='accounts')

urlpatterns = [
    # Endpoint de login (custom)
    path('login/', login_with_email, name='login_account'),

    # Endpoint de register (rétrocompatibilité - DEPRECATED)
    path('register/', views.register_account, name='register_account'),

    # Routes RESTful générées par le router
    # GET    /api/accounts/       -> list
    # POST   /api/accounts/       -> create
    # GET    /api/accounts/<id>/  -> retrieve
    # PUT    /api/accounts/<id>/  -> update
    # PATCH  /api/accounts/<id>/  -> partial_update
    # DELETE /api/accounts/<id>/  -> destroy
    path('', include(router.urls)),
]
