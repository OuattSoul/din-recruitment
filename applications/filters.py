from django_filters import rest_framework as filters
from .models import Application


class ApplicationFilter(filters.FilterSet):
    """
    Filtres pour les candidatures
    """
    # Filtre par nom de candidat (insensible à la casse)
    first_name = filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = filters.CharFilter(field_name='last_name', lookup_expr='icontains')

    # Filtre par email
    email = filters.CharFilter(field_name='email', lookup_expr='icontains')

    # Filtre par type de contrat
    contract_type_sought = filters.ChoiceFilter(
        field_name='contract_type_sought',
        choices=Application.CONTRACT_TYPE_CHOICES
    )

    # Filtre par poste (titre de l'offre)
    job_title = filters.CharFilter(field_name='job__title', lookup_expr='icontains')

    # Filtre par type de candidature (spontanée ou sur offre)
    is_spontaneous = filters.BooleanFilter(field_name='is_spontaneous')

    # Filtre par statut de candidature
    status = filters.ChoiceFilter(
        field_name='status',
        choices=Application.STATUS_CHOICES
    )

    # Filtre personnalisé pour "complétées" vs "manquantes"
    # Basé sur le statut: complétées = reviewed/accepted/rejected, manquantes = pending
    application_status = filters.ChoiceFilter(
        method='filter_application_status',
        choices=[
            ('completed', 'Complétées'),
            ('incomplete', 'Manquantes'),
        ]
    )

    def filter_application_status(self, queryset, name, value):
        """
        Filtre personnalisé pour les candidatures complétées/manquantes
        - Complétées: status in [reviewed, accepted, rejected]
        - Manquantes: status = pending
        """
        if value == 'completed':
            return queryset.filter(status__in=['reviewed', 'accepted', 'rejected'])
        elif value == 'incomplete':
            return queryset.filter(status='pending')
        return queryset

    class Meta:
        model = Application
        fields = [
            'first_name',
            'last_name',
            'email',
            'contract_type_sought',
            'job_title',
            'is_spontaneous',
            'status',
        ]
