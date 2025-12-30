from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("api/auth/login/", TokenObtainPairView.as_view()),
    path("api/auth/refresh/", TokenRefreshView.as_view()),
    path("api/accounts/", include("accounts.urls")),
    path("api/jobs/", include("jobs.urls")),
    path("api/applications/", include("applications.urls")),
]
