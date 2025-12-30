from rest_framework import serializers
from .models import JobOffer


class JobOfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobOffer
        fields = "__all__"

    def validate_description(self, value):
        if len(value) < 50:
            raise serializers.ValidationError(
                "La description doit contenir au moins 50 caractères."
            )
        return value

    def validate_skills(self, value):
        if not isinstance(value, list) or len(value) == 0:
            raise serializers.ValidationError(
                "Les compétences doivent être une liste non vide."
            )
        return value
