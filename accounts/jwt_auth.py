"""
Backend d'authentification JWT personnalisé pour les comptes Account
"""

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import jwt
from .models import Account


class JWTAuthentication(BaseAuthentication):
    """
    Authentification personnalisée pour vérifier les tokens JWT Bearer
    """

    def authenticate(self, request):
        """
        Vérifier le token JWT dans le header Authorization
        """
        # Récupérer le header Authorization
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')

        if not auth_header:
            return None

        # Vérifier le format Bearer
        parts = auth_header.split()

        if len(parts) != 2:
            return None

        if parts[0].lower() != 'bearer':
            return None

        token = parts[1]

        try:
            # Décoder le token JWT
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256']
            )

            # Vérifier le type de token
            if payload.get('type') != 'access':
                raise AuthenticationFailed('Type de token invalide')

            # Récupérer le compte
            account_id = payload.get('account_id')
            if not account_id:
                raise AuthenticationFailed('Token invalide')

            try:
                account = Account.objects.get(id=account_id, is_active=True)
            except Account.DoesNotExist:
                raise AuthenticationFailed('Compte introuvable ou inactif')

            # Retourner (user, auth) - user sera l'account dans ce cas
            return (account, token)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expiré')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Token invalide')

    def authenticate_header(self, request):
        """
        Retourner le format attendu pour le header WWW-Authenticate
        """
        return 'Bearer realm="api"'


def decode_jwt_token(token):
    """
    Fonction utilitaire pour décoder un token JWT
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=['HS256']
        )
        return payload
    except jwt.InvalidTokenError:
        return None
