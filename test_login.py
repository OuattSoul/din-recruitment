"""
Script de test pour l'authentification par email

Usage:
    python test_login.py
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_register_and_login():
    """Test complet : inscription puis connexion"""
    print("\n" + "=" * 60)
    print("  TEST COMPLET : INSCRIPTION + CONNEXION")
    print("=" * 60)

    # Étape 1 : Créer un compte
    print("\n[Étape 1] Création d'un compte...")
    register_url = f"{BASE_URL}/api/accounts/register/"
    register_data = {
        "first_name": "Marie",
        "last_name": "Martin",
        "email": "marie.martin@example.com",
        "phone": "0698765432",
        "password": "MotDePasse123!",
        "password_confirm": "MotDePasse123!"
    }

    try:
        response = requests.post(register_url, json=register_data)
        print(f"Status: {response.status_code}")

        if response.status_code == 201:
            print("✅ Compte créé avec succès!")
            account = response.json()['account']
            print(f"   ID: {account['id']}")
            print(f"   Email: {account['email']}")
        elif response.status_code == 400:
            # Peut-être que le compte existe déjà
            print("⚠️  Compte existe peut-être déjà, continuons avec le login...")
        else:
            print("❌ Erreur lors de la création")
            print(f"   Réponse: {response.json()}")
            return

    except requests.exceptions.ConnectionError:
        print("❌ Erreur: Le serveur Django n'est pas démarré!")
        print("   Lancez d'abord: python manage.py runserver")
        return
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return

    # Étape 2 : Se connecter
    print("\n[Étape 2] Connexion avec email et mot de passe...")
    login_url = f"{BASE_URL}/api/accounts/login/"
    login_data = {
        "email": "marie.martin@example.com",
        "password": "MotDePasse123!"
    }

    try:
        response = requests.post(login_url, json=login_data)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            print("✅ Connexion réussie!")
            data = response.json()
            print(f"\n   Access Token: {data['access'][:20]}...")
            print(f"   Refresh Token: {data['refresh'][:20]}...")
            print(f"\n   Compte:")
            print(f"   - ID: {data['account']['id']}")
            print(f"   - Email: {data['account']['email']}")
            print(f"   - Nom: {data['account']['first_name']} {data['account']['last_name']}")
        else:
            print("❌ Erreur lors de la connexion")
            print(f"   Réponse: {response.json()}")

    except Exception as e:
        print(f"❌ Erreur: {e}")


def test_login_wrong_password():
    """Test de connexion avec mauvais mot de passe"""
    print("\n" + "=" * 60)
    print("  TEST : MAUVAIS MOT DE PASSE")
    print("=" * 60)

    login_url = f"{BASE_URL}/api/accounts/login/"
    login_data = {
        "email": "marie.martin@example.com",
        "password": "MauvaisMotDePasse"
    }

    try:
        response = requests.post(login_url, json=login_data)
        print(f"Status: {response.status_code}")

        if response.status_code == 401:
            print("✅ Rejet correct: mot de passe incorrect détecté")
            print(f"   Message: {response.json()['error']}")
        else:
            print("❌ Le mauvais mot de passe n'a pas été détecté!")

    except Exception as e:
        print(f"❌ Erreur: {e}")


def test_login_wrong_email():
    """Test de connexion avec email inexistant"""
    print("\n" + "=" * 60)
    print("  TEST : EMAIL INEXISTANT")
    print("=" * 60)

    login_url = f"{BASE_URL}/api/accounts/login/"
    login_data = {
        "email": "inexistant@example.com",
        "password": "MotDePasse123!"
    }

    try:
        response = requests.post(login_url, json=login_data)
        print(f"Status: {response.status_code}")

        if response.status_code == 401:
            print("✅ Rejet correct: email inexistant détecté")
            print(f"   Message: {response.json()['error']}")
        else:
            print("❌ L'email inexistant n'a pas été détecté!")

    except Exception as e:
        print(f"❌ Erreur: {e}")


def test_login_missing_fields():
    """Test de connexion avec champs manquants"""
    print("\n" + "=" * 60)
    print("  TEST : CHAMPS MANQUANTS")
    print("=" * 60)

    login_url = f"{BASE_URL}/api/accounts/login/"
    login_data = {
        "email": "marie.martin@example.com"
        # Pas de password
    }

    try:
        response = requests.post(login_url, json=login_data)
        print(f"Status: {response.status_code}")

        if response.status_code == 400:
            print("✅ Validation correcte: champs manquants détectés")
            print(f"   Message: {response.json()['error']}")
        else:
            print("❌ Les champs manquants n'ont pas été détectés!")

    except Exception as e:
        print(f"❌ Erreur: {e}")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  TESTS D'AUTHENTIFICATION PAR EMAIL")
    print("=" * 60)

    # Test 1 : Inscription + Connexion
    test_register_and_login()

    # Test 2 : Mauvais mot de passe
    test_login_wrong_password()

    # Test 3 : Email inexistant
    test_login_wrong_email()

    # Test 4 : Champs manquants
    test_login_missing_fields()

    print("\n" + "=" * 60)
    print("  TESTS TERMINÉS")
    print("=" * 60)
    print()
