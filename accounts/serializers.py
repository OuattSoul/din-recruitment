from rest_framework import serializers
from .models import Account

class AccountRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer pour l'inscription d'un nouveau compte
    """
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone', 'password', 'password_confirm', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'required': False}  # Le rôle est optionnel, par défaut "candidate"
        }

    def validate_email(self, value):
        """Vérifier que l'email n'existe pas déjà"""
        if Account.objects.filter(email=value).exists():
            raise serializers.ValidationError("Un compte avec cet email existe déjà.")
        return value

    def validate(self, attrs):
        """Vérifier que les mots de passe correspondent"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                "password": "Les mots de passe ne correspondent pas."
            })
        return attrs

    def create(self, validated_data):
        """Créer un nouveau compte"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')

        # Utiliser create_user pour hasher correctement le mot de passe
        account = Account.objects.create_user(
            password=password,
            **validated_data
        )
        return account


class AccountSerializer(serializers.ModelSerializer):
    """
    Serializer pour afficher les informations du compte
    """
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'role', 'role_display', 'created_at']
        read_only_fields = ['id', 'created_at']


class AccountUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer pour la mise à jour d'un compte
    """
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone', 'role', 'password']
        extra_kwargs = {
            'email': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def validate_email(self, value):
        """Vérifier que l'email n'est pas déjà utilisé par un autre compte"""
        instance = self.instance
        if instance and Account.objects.filter(email=value).exclude(id=instance.id).exists():
            raise serializers.ValidationError("Un compte avec cet email existe déjà.")
        return value

    def update(self, instance, validated_data):
        """Mettre à jour le compte"""
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance
