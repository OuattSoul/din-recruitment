"""
Script pour corriger les comptes existants avec le bon hashing de mot de passe

ATTENTION: Ce script ne peut PAS récupérer les mots de passe originaux.
Vous devez les supprimer et les recréer manuellement.

Usage:
    python fix_existing_accounts.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from accounts.models import Account

def fix_accounts():
    """Afficher tous les comptes et demander confirmation pour les supprimer"""

    accounts = Account.objects.all()

    if not accounts.exists():
        print("[INFO] Aucun compte trouve dans la base de donnees")
        return

    print("\n" + "=" * 60)
    print("  COMPTES EXISTANTS")
    print("=" * 60)

    for account in accounts:
        print(f"\nID: {account.id}")
        print(f"Email: {account.email}")
        print(f"Nom: {account.first_name} {account.last_name}")
        print(f"Role: {account.role}")
        print(f"Password hash: {account.password[:50]}...")

    print("\n" + "=" * 60)
    print("\n[ATTENTION] Ces comptes utilisent probablement un mauvais hashing")
    print("Ils doivent etre supprimes et recrees.")
    print("\nPour recréer le compte admin:")
    print("  python create_admin_direct.py")
    print("\nPour créer de nouveaux comptes candidats:")
    print("  Utilisez l'endpoint POST /api/accounts/register/")

    choice = input("\nVoulez-vous supprimer TOUS les comptes? (o/n): ")

    if choice.lower() == 'o':
        count = accounts.count()
        accounts.delete()
        print(f"\n[OK] {count} compte(s) supprime(s)")
        print("\nVous pouvez maintenant recreer les comptes avec:")
        print("  python create_admin_direct.py")
    else:
        print("\n[ANNULE] Operation annulee")

if __name__ == "__main__":
    try:
        fix_accounts()
    except Exception as e:
        print(f"\n[ERREUR] {e}")
        import traceback
        traceback.print_exc()
