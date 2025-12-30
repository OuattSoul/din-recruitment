from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    ROLE_CHOICES = [
        ("superadmin", "Super Admin"),
        ("admin", "Admin"),
        ("candidate", "Candidate"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="candidate")
    phone = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)

    # Champs spécifiques aux candidats
    resume = models.FileField(upload_to="resumes/", null=True, blank=True)
    linkedin_url = models.URLField(max_length=255, blank=True)
    portfolio_url = models.URLField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    skills = models.JSONField(default=list, blank=True)

    # Champs pour tous
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_superadmin(self):
        return self.role == "superadmin"

    @property
    def is_admin(self):
        return self.role in ["admin", "superadmin"]

    @property
    def is_candidate(self):
        return self.role == "candidate"
