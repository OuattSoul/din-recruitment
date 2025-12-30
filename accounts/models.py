from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class AccountManager(BaseUserManager):
    """Manager personnalisé pour le modèle Account"""

    def create_user(self, email, password=None, **extra_fields):
        """Créer et retourner un utilisateur normal"""
        if not email:
            raise ValueError("L'email est obligatoire")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Créer et retourner un superutilisateur"""
        extra_fields.setdefault('role', 'superadmin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    """
    Modèle pour les comptes utilisateurs
    """
    ROLE_CHOICES = [
        ("superadmin", "Super Admin"),
        ("admin", "Admin"),
        ("candidate", "Candidate"),
    ]

    first_name = models.CharField(max_length=100, verbose_name="Prénom(s)")
    last_name = models.CharField(max_length=100, verbose_name="Nom")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Téléphone", blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="candidate", verbose_name="Rôle")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Compte"
        verbose_name_plural = "Comptes"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    def get_full_name(self):
        """Retourner le nom complet"""
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        """Retourner le prénom"""
        return self.first_name

    @property
    def is_superadmin(self):
        """Vérifier si l'utilisateur est un super admin"""
        return self.role == "superadmin"

    @property
    def is_admin(self):
        """Vérifier si l'utilisateur est un admin ou super admin"""
        return self.role in ["admin", "superadmin"]

    @property
    def is_candidate(self):
        """Vérifier si l'utilisateur est un candidat"""
        return self.role == "candidate"
