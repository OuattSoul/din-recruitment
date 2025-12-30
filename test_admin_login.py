"""
Test de connexion du compte admin

Usage:
    python test_admin_login.py
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_admin_login():
    """Test de connexion avec le compte admin"""
    print("\n" + "=" * 60)
    print("  TEST DE CONNEXION ADMIN")
    print("=" * 60)

    login_url = f"{BASE_URL}/api/accounts/login/"
    login_data = {
        "email": "admin@din-africa.net",
        "password": "09876"
    }

    print(f"\n[INFO] Tentative de connexion a {login_url}")
    print(f"[INFO] Email: {login_data['email']}")

    try:
        response = requests.post(login_url, json=login_data)
        print(f"\n[REPONSE] Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("\n" + "=" * 60)
            print("  [OK] CONNEXION REUSSIE!")
            print("=" * 60)
            print(f"\nAccess Token: {data['access'][:30]}...")
            print(f"Refresh Token: {data['refresh'][:30]}...")
            print(f"\nCompte:")
            print(f"  - ID: {data['account']['id']}")
            print(f"  - Email: {data['account']['email']}")
            print(f"  - Nom: {data['account']['first_name']} {data['account']['last_name']}")
            print("=" * 60)

            return data['access']

        else:
            print("\n[ERREUR] Connexion echouee")
            print(f"Reponse: {json.dumps(response.json(), indent=2)}")
            return None

    except requests.exceptions.ConnectionError:
        print("\n[ERREUR] Le serveur Django n'est pas demarre!")
        print("Lancez d'abord: python manage.py runserver")
        return None

    except Exception as e:
        print(f"\n[ERREUR] {e}")
        return None


if __name__ == "__main__":
    token = test_admin_login()

    if token:
        print("\n[INFO] Vous pouvez utiliser ce token pour les requetes authentifiees")
        print(f'[INFO] Header: Authorization: Bearer {token[:30]}...')
