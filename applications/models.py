from django.db import models
from django.conf import settings
from jobs.models import JobOffer


class Application(models.Model):
    """
    Modèle pour les candidatures
    """

    STATUS_CHOICES = [
        ("pending", "En attente"),
        ("reviewed", "Examinée"),
        ("accepted", "Acceptée"),
        ("rejected", "Rejetée"),
    ]

    CIVILITY_CHOICES = [
        ("monsieur", "Monsieur"),
        ("madame", "Madame"),
        ("mademoiselle", "Mademoiselle"),
    ]

    CONTRACT_TYPE_CHOICES = [
        ("cdi", "CDI"),
        ("cdd", "CDD"),
        ("stage", "Stage"),
        ("alternance", "Alternance"),
        ("interim", "Intérim"),
        ("freelance", "Freelance"),
        ("temps_partiel", "Temps partiel"),
    ]

    # Relation avec le candidat et l'offre
    candidate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")
    job = models.ForeignKey(JobOffer, on_delete=models.CASCADE, related_name="applications", null=True, blank=True)
    is_spontaneous = models.BooleanField(default=False, verbose_name="Candidature spontanée")

    # Informations personnelles
    civility = models.CharField(max_length=20, choices=CIVILITY_CHOICES, verbose_name="Civilité")
    first_name = models.CharField(max_length=100, verbose_name="Prénom(s)")
    last_name = models.CharField(max_length=100, verbose_name="Nom")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Téléphone")
    country = models.CharField(max_length=100, verbose_name="Pays")
    address = models.TextField(verbose_name="Adresse complète")

    # Informations professionnelles
    contract_type_sought = models.CharField(
        max_length=20,
        choices=CONTRACT_TYPE_CHOICES,
        verbose_name="Type de contrat recherché"
    )
    experience = models.JSONField(default=list, verbose_name="Expérience", help_text="Liste des expériences professionnelles")
    education_level = models.CharField(max_length=255, verbose_name="Niveau d'études")
    current_salary = models.BigIntegerField(null=True, blank=True, verbose_name="Salaire actuel (facultatif)")
    expected_salary = models.BigIntegerField(verbose_name="Prétention salariale")

    # Statut et dates
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name="Statut")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de candidature")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Candidature"
        verbose_name_plural = "Candidatures"

    def __str__(self):
        job_title = self.job.title if self.job else "Candidature spontanée"
        return f"{self.first_name} {self.last_name} - {job_title}"
