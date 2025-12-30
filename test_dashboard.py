"""
Script pour tester le dashboard admin
"""
import os
import sys
import django

# Fix encoding for Windows
sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import Account
from jobs.models import JobOffer
from applications.models import Application
from datetime import date, timedelta


def create_test_data():
    """Créer des données de test"""

    # Créer un admin si non existant
    admin, created = Account.objects.get_or_create(
        email='admin@example.com',
        defaults={
            'first_name': 'Admin',
            'last_name': 'Test',
            'role': 'admin',
            'is_staff': True
        }
    )
    if created:
        admin.set_password('admin123')
        admin.save()
        print(f"✓ Admin créé: {admin.email}")
    else:
        print(f"✓ Admin existant: {admin.email}")

    # Créer un candidat
    candidate, created = Account.objects.get_or_create(
        email='candidat@example.com',
        defaults={
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'role': 'candidate',
            'phone': '0123456789'
        }
    )
    if created:
        candidate.set_password('candidat123')
        candidate.save()
        print(f"✓ Candidat créé: {candidate.email}")
    else:
        print(f"✓ Candidat existant: {candidate.email}")

    # Créer des offres d'emploi
    job1, created = JobOffer.objects.get_or_create(
        title="Développeur Python",
        defaults={
            'company': 'Tech Corp',
            'location': 'Paris',
            'contract_type': 'cdi',
            'salary': '40000-50000',
            'application_deadline': date.today() + timedelta(days=30),
            'description': 'Recherche développeur Python expérimenté',
            'skills': ['Python', 'Django', 'REST API'],
            'status': 'published',
            'created_by': admin
        }
    )
    if created:
        print(f"✓ Offre créée: {job1.title}")

    job2, created = JobOffer.objects.get_or_create(
        title="Chef de projet",
        defaults={
            'company': 'Consulting Inc',
            'location': 'Lyon',
            'contract_type': 'cdi',
            'salary': '50000-60000',
            'application_deadline': date.today() + timedelta(days=45),
            'description': 'Chef de projet expérimenté',
            'skills': ['Gestion de projet', 'Agile', 'Scrum'],
            'status': 'published',
            'created_by': admin
        }
    )
    if created:
        print(f"✓ Offre créée: {job2.title}")

    # Créer des candidatures
    # Candidature sur offre - CDI
    app1, created = Application.objects.get_or_create(
        candidate=candidate,
        job=job1,
        email='jean.dupont@example.com',
        defaults={
            'civility': 'monsieur',
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'phone': '0123456789',
            'country': 'France',
            'address': '123 Rue de Paris, 75001 Paris',
            'contract_type_sought': 'cdi',
            'experience': [
                {'title': 'Dev Python', 'company': 'ABC', 'duration': '2 ans'}
            ],
            'education_level': 'Master',
            'expected_salary': 45000,
            'status': 'reviewed',
            'is_spontaneous': False
        }
    )
    if created:
        print(f"✓ Candidature créée: {app1}")

    # Candidature spontanée - Intérim
    candidate2, _ = Account.objects.get_or_create(
        email='marie@example.com',
        defaults={
            'first_name': 'Marie',
            'last_name': 'Martin',
            'role': 'candidate',
            'phone': '0987654321'
        }
    )
    if _:
        candidate2.set_password('marie123')
        candidate2.save()

    app2, created = Application.objects.get_or_create(
        candidate=candidate2,
        email='marie.martin@example.com',
        defaults={
            'job': None,
            'civility': 'madame',
            'first_name': 'Marie',
            'last_name': 'Martin',
            'phone': '0987654321',
            'country': 'France',
            'address': '456 Avenue de Lyon, 69001 Lyon',
            'contract_type_sought': 'interim',
            'experience': [
                {'title': 'Assistante', 'company': 'XYZ', 'duration': '1 an'}
            ],
            'education_level': 'Licence',
            'expected_salary': 30000,
            'status': 'pending',
            'is_spontaneous': True
        }
    )
    if created:
        print(f"✓ Candidature spontanée créée: {app2}")

    # Candidature sur offre - Stage
    candidate3, _ = Account.objects.get_or_create(
        email='paul@example.com',
        defaults={
            'first_name': 'Paul',
            'last_name': 'Bernard',
            'role': 'candidate',
            'phone': '0111222333'
        }
    )
    if _:
        candidate3.set_password('paul123')
        candidate3.save()

    app3, created = Application.objects.get_or_create(
        candidate=candidate3,
        job=job2,
        email='paul.bernard@example.com',
        defaults={
            'civility': 'monsieur',
            'first_name': 'Paul',
            'last_name': 'Bernard',
            'phone': '0111222333',
            'country': 'France',
            'address': '789 Boulevard de Marseille, 13001 Marseille',
            'contract_type_sought': 'stage',
            'experience': [],
            'education_level': 'Licence',
            'expected_salary': 15000,
            'status': 'pending',
            'is_spontaneous': False
        }
    )
    if created:
        print(f"✓ Candidature stage créée: {app3}")

    print("\n" + "="*60)
    print("STATISTIQUES DU DASHBOARD")
    print("="*60)

    total = Application.objects.count()
    spontanees = Application.objects.filter(is_spontaneous=True).count()
    sur_offres = Application.objects.filter(is_spontaneous=False).count()
    interim = Application.objects.filter(contract_type_sought='interim').count()
    evaluations = Application.objects.filter(status='reviewed').count()

    print(f"Total de candidatures: {total}")
    print(f"Candidatures spontanées: {spontanees}")
    print(f"Candidatures sur offres: {sur_offres}")
    print(f"Candidatures intérim: {interim}")
    print(f"Candidatures en évaluation: {evaluations}")
    print("="*60)

    print("\nPour tester le dashboard:")
    print(f"1. Démarrer le serveur: python manage.py runserver")
    print(f"2. Se connecter avec: {admin.email} / admin123")
    print(f"3. Accéder à: http://localhost:8000/api/applications/dashboard_stats/")
    print("\nExemples de filtres:")
    print("- http://localhost:8000/api/applications/?contract_type_sought=interim")
    print("- http://localhost:8000/api/applications/?is_spontaneous=true")
    print("- http://localhost:8000/api/applications/?status=reviewed")
    print("- http://localhost:8000/api/applications/?application_status=completed")


if __name__ == '__main__':
    create_test_data()
