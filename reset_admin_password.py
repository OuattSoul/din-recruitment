"""
Script pour réinitialiser le mot de passe admin
"""
import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import Account

# Récupérer ou créer l'admin
admin = Account.objects.filter(email='admin@example.com').first()

if admin:
    admin.set_password('admin123')
    admin.save()
    print(f"✓ Mot de passe réinitialisé pour {admin.email}")
else:
    # Créer l'admin
    admin = Account.objects.create_user(
        email='admin@example.com',
        password='admin123',
        first_name='Admin',
        last_name='Test',
        role='admin',
        is_staff=True
    )
    print(f"✓ Admin créé: {admin.email}")

print("Mot de passe: admin123")
