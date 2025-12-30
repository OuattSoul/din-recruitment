from rest_framework import serializers
from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    """
    Serializer pour les candidatures
    """
    candidate_name = serializers.SerializerMethodField(read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    civility_display = serializers.CharField(source='get_civility_display', read_only=True)
    contract_type_display = serializers.CharField(source='get_contract_type_sought_display', read_only=True)

    class Meta:
        model = Application
        fields = [
            'id',
            'candidate',
            'candidate_name',
            'job',
            'job_title',
            'is_spontaneous',
            # Informations personnelles
            'civility',
            'civility_display',
            'first_name',
            'last_name',
            'email',
            'phone',
            'country',
            'address',
            # Informations professionnelles
            'contract_type_sought',
            'contract_type_display',
            'experience',
            'education_level',
            'current_salary',
            'expected_salary',
            # Statut et dates
            'status',
            'status_display',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'candidate', 'created_at', 'updated_at']

    def get_candidate_name(self, obj):
        """Retourner le nom complet du candidat"""
        return f"{obj.candidate.first_name} {obj.candidate.last_name}"

    def validate_experience(self, value):
        """Valider que l'expérience est une liste"""
        if not isinstance(value, list):
            raise serializers.ValidationError("L'expérience doit être une liste")
        return value

    def validate_expected_salary(self, value):
        """Valider que la prétention salariale est positive"""
        if value <= 0:
            raise serializers.ValidationError("La prétention salariale doit être supérieure à 0")
        return value

    def validate_current_salary(self, value):
        """Valider que le salaire actuel est positif s'il est fourni"""
        if value is not None and value <= 0:
            raise serializers.ValidationError("Le salaire actuel doit être supérieur à 0")
        return value
