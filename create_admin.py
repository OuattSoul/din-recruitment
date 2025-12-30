"""
Script pour créer un compte admin

Usage:
    python create_admin.py
"""

import os
import django

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from accounts.models import Account

def create_admin_account():
    """Créer un compte admin"""
    email = "admin@din-africa.net"
    password = "09876"

    # Vérifier si le compte existe déjà
    if Account.objects.filter(email=email).exists():
        print(f"[ERREUR] Un compte avec l'email {email} existe deja!")

        # Demander si on veut le supprimer et recréer
        choice = input("Voulez-vous le supprimer et le recreer? (o/n): ")
        if choice.lower() == 'o':
            Account.objects.filter(email=email).delete()
            print("[OK] Ancien compte supprime")
        else:
            print("[ANNULE] Operation annulee")
            return

    # Créer le compte avec create_user pour hasher le mot de passe
    admin_account = Account.objects.create_user(
        email=email,
        password=password,
        first_name="Admin",
        last_name="DIN Africa",
        phone="",
        role="admin",  # Définir le rôle comme admin
        is_staff=True,  # Peut accéder à l'admin Django
        is_active=True
    )

    print("\n" + "=" * 60)
    print("  [OK] COMPTE ADMIN CREE AVEC SUCCES!")
    print("=" * 60)
    print(f"\nID: {admin_account.id}")
    print(f"Email: {admin_account.email}")
    print(f"Nom: {admin_account.first_name} {admin_account.last_name}")
    print(f"Statut: {'Actif' if admin_account.is_active else 'Inactif'}")
    print(f"Date de création: {admin_account.created_at}")
    print("\n" + "=" * 60)
    print("\nVous pouvez maintenant vous connecter avec :")
    print(f"  Email: {email}")
    print(f"  Password: {password}")
    print("\nEndpoint de connexion:")
    print("  POST http://localhost:8000/api/accounts/login/")
    print("=" * 60)

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  CRÉATION DU COMPTE ADMIN")
    print("=" * 60)

    try:
        create_admin_account()
    except Exception as e:
        print(f"\n[ERREUR] Erreur lors de la creation du compte: {e}")
        import traceback
        traceback.print_exc()
