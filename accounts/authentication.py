from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Account
import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings


def generate_jwt_tokens_for_account(account):
    """
    Générer de vrais tokens JWT pour un compte Account
    Compatible avec le format Bearer Token standard
    """
    # Utiliser timezone.utc au lieu de utcnow() (deprecated)
    now = datetime.now(timezone.utc)

    # Créer le payload pour le token
    access_payload = {
        'account_id': account.id,
        'email': account.email,
        'first_name': account.first_name,
        'last_name': account.last_name,
        'role': account.role,
        'type': 'access',
        'exp': now + timedelta(hours=1),  # Expire dans 1 heure
        'iat': now
    }

    refresh_payload = {
        'account_id': account.id,
        'email': account.email,
        'role': account.role,
        'type': 'refresh',
        'exp': now + timedelta(days=7),  # Expire dans 7 jours
        'iat': now
    }

    # Générer les tokens JWT
    secret_key = settings.SECRET_KEY
    access_token = jwt.encode(access_payload, secret_key, algorithm='HS256')
    refresh_token = jwt.encode(refresh_payload, secret_key, algorithm='HS256')

    return {
        'access': access_token,
        'refresh': refresh_token,
        'token_type': 'Bearer',
        'expires_in': 3600,  # 1 heure en secondes
        'account': {
            'id': account.id,
            'email': account.email,
            'first_name': account.first_name,
            'last_name': account.last_name,
            'role': account.role,
        }
    }


@api_view(['POST'])
@permission_classes([AllowAny])
def login_with_email(request):
    """
    Endpoint pour se connecter avec email et mot de passe

    POST /api/accounts/login/
    Body:
    {
        "email": "user@example.com",
        "password": "password123"
    }

    Réponse:
    {
        "access": "token...",
        "refresh": "token...",
        "account": {
            "id": 1,
            "email": "user@example.com",
            "first_name": "John",
            "last_name": "Doe"
        }
    }
    """
    email = request.data.get('email')
    password = request.data.get('password')

    # Validation des champs
    if not email or not password:
        return Response({
            'error': 'Email et mot de passe requis'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Chercher le compte
    try:
        account = Account.objects.get(email=email, is_active=True)
    except Account.DoesNotExist:
        return Response({
            'error': 'Email ou mot de passe incorrect'
        }, status=status.HTTP_401_UNAUTHORIZED)

    # Vérifier le mot de passe
    if not check_password(password, account.password):
        return Response({
            'error': 'Email ou mot de passe incorrect'
        }, status=status.HTTP_401_UNAUTHORIZED)

    # Générer les tokens JWT
    tokens = generate_jwt_tokens_for_account(account)

    return Response(tokens, status=status.HTTP_200_OK)
