from django.db import models
from django.conf import settings


class JobOffer(models.Model):

    CONTRACT_CHOICES = [
        ("cdi", "CDI"),
        ("cdd", "CDD"),
        ("stage", "Stage"),
        ("alternance", "Alternance"),
        ("interim", "Intérim"),
        ("freelance", "Freelance"),
        ("temps_partiel", "Temps partiel"),
    ]

    STATUS_CHOICES = [
        ("draft", "Brouillon"),
        ("published", "Publiée"),
        ("closed", "Fermée"),
    ]

    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    contract_type = models.CharField(
        max_length=20,
        choices=CONTRACT_CHOICES
    )

    salary = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to="job_offers/", null=True, blank=True)

    application_deadline = models.DateField()

    description = models.TextField()
    skills = models.JSONField(default=list)  # liste de compétences

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="published")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="job_offers"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.company}"

    @property
    def is_active(self):
        """Vérifie si l'offre est encore active"""
        from django.utils import timezone
        return self.status == "published" and self.application_deadline >= timezone.now().date()
