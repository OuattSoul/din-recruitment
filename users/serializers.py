from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer de base pour les utilisateurs"""

    class Meta:
        model = User
        exclude = ["password", "groups", "user_permissions"]
        read_only_fields = ["id", "created_at", "updated_at"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer pour l'inscription des candidats"""

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "username", "email", "password", "password_confirm",
            "first_name", "last_name", "phone", "country",
            "linkedin_url", "portfolio_url", "bio"
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            role='candidate',
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone', ''),
            country=validated_data.get('country', ''),
            linkedin_url=validated_data.get('linkedin_url', ''),
            portfolio_url=validated_data.get('portfolio_url', ''),
            bio=validated_data.get('bio', '')
        )
        return user


class AdminRegistrationSerializer(serializers.ModelSerializer):
    """Serializer pour l'inscription des admins (par superadmin uniquement)"""

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name", "role"]

    def validate_role(self, value):
        if value not in ["admin", "superadmin"]:
            raise serializers.ValidationError("Le rôle doit être 'admin' ou 'superadmin'")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            role=validated_data['role'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class CandidateProfileSerializer(serializers.ModelSerializer):
    """Serializer pour le profil complet du candidat"""

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "first_name", "last_name",
            "phone", "country", "resume", "linkedin_url", "portfolio_url",
            "bio", "skills", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "username", "created_at", "updated_at"]
