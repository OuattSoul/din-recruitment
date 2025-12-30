"""
Script de test pour l'API d'inscription

Usage:
    python test_inscription.py
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_register_account():
    """Test de création d'un compte"""
    print("\n=== Test: Création d'un compte ===")

    url = f"{BASE_URL}/api/accounts/register/"
    data = {
        "first_name": "Jean",
        "last_name": "Dupont",
        "email": "jean.dupont@example.com",
        "phone": "0612345678",
        "password": "MonMotDePasse123!",
        "password_confirm": "MonMotDePasse123!"
    }

    try:
        response = requests.post(url, json=data)
        print(f"Status: {response.status_code}")
        print(f"Réponse: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

        if response.status_code == 201:
            print("✅ Compte créé avec succès!")
        else:
            print("❌ Erreur lors de la création")

    except requests.exceptions.ConnectionError:
        print("❌ Erreur: Le serveur Django n'est pas démarré!")
        print("   Lancez d'abord: python manage.py runserver")
    except Exception as e:
        print(f"❌ Erreur: {e}")


def test_list_accounts():
    """Test de listage des comptes"""
    print("\n=== Test: Liste des comptes ===")

    url = f"{BASE_URL}/api/accounts/"

    try:
        response = requests.get(url)
        print(f"Status: {response.status_code}")

        data = response.json()
        print(f"Total de comptes: {data['count']}")

        for account in data['accounts']:
            print(f"  - {account['first_name']} {account['last_name']} ({account['email']})")

        if response.status_code == 200:
            print("✅ Liste récupérée avec succès!")

    except requests.exceptions.ConnectionError:
        print("❌ Erreur: Le serveur Django n'est pas démarré!")
        print("   Lancez d'abord: python manage.py runserver")
    except Exception as e:
        print(f"❌ Erreur: {e}")


def test_duplicate_email():
    """Test de création avec email existant"""
    print("\n=== Test: Email en double (doit échouer) ===")

    url = f"{BASE_URL}/api/accounts/register/"
    data = {
        "first_name": "Marie",
        "last_name": "Martin",
        "email": "jean.dupont@example.com",  # Email déjà utilisé
        "phone": "0698765432",
        "password": "AutreMotDePasse123!",
        "password_confirm": "AutreMotDePasse123!"
    }

    try:
        response = requests.post(url, json=data)
        print(f"Status: {response.status_code}")
        print(f"Réponse: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

        if response.status_code == 400:
            print("✅ Validation correcte: email déjà existant")
        else:
            print("❌ L'email en double n'a pas été détecté!")

    except Exception as e:
        print(f"❌ Erreur: {e}")


def test_password_mismatch():
    """Test de mots de passe non correspondants"""
    print("\n=== Test: Mots de passe différents (doit échouer) ===")

    url = f"{BASE_URL}/api/accounts/register/"
    data = {
        "first_name": "Pierre",
        "last_name": "Durand",
        "email": "pierre.durand@example.com",
        "phone": "0687654321",
        "password": "MotDePasse123!",
        "password_confirm": "MotDePasseDifferent123!"
    }

    try:
        response = requests.post(url, json=data)
        print(f"Status: {response.status_code}")
        print(f"Réponse: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

        if response.status_code == 400:
            print("✅ Validation correcte: mots de passe différents")
        else:
            print("❌ Les mots de passe différents n'ont pas été détectés!")

    except Exception as e:
        print(f"❌ Erreur: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("  TEST DE L'API D'INSCRIPTION")
    print("=" * 60)

    # 1. Créer un compte
    test_register_account()

    # 2. Lister les comptes
    test_list_accounts()

    # 3. Tester email en double
    test_duplicate_email()

    # 4. Tester mots de passe différents
    test_password_mismatch()

    print("\n" + "=" * 60)
    print("  TESTS TERMINÉS")
    print("=" * 60)
