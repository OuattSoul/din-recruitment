"""
Test complet du système d'authentification JWT Bearer

Usage:
    python test_jwt_bearer.py
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_login_jwt():
    """Test de connexion et récupération du JWT"""
    print("\n" + "=" * 60)
    print("  TEST 1: CONNEXION ET GENERATION JWT")
    print("=" * 60)

    login_url = f"{BASE_URL}/api/accounts/login/"
    login_data = {
        "email": "admin@din-africa.net",
        "password": "09876"
    }

    try:
        response = requests.post(login_url, json=login_data)
        print(f"\n[REPONSE] Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("\n[OK] Connexion reussie!")
            print(f"\nToken Type: {data.get('token_type', 'Bearer')}")
            print(f"Expires In: {data.get('expires_in', 3600)} secondes")
            print(f"\nAccess Token (JWT):")
            print(f"  {data['access'][:50]}...")
            print(f"\nRefresh Token (JWT):")
            print(f"  {data['refresh'][:50]}...")
            print(f"\nCompte:")
            print(f"  - ID: {data['account']['id']}")
            print(f"  - Email: {data['account']['email']}")
            print(f"  - Nom: {data['account']['first_name']} {data['account']['last_name']}")

            return data['access']

        else:
            print("\n[ERREUR] Connexion echouee")
            print(json.dumps(response.json(), indent=2))
            return None

    except Exception as e:
        print(f"\n[ERREUR] {e}")
        return None


def test_protected_endpoint(token):
    """Test d'un endpoint protégé avec le Bearer Token"""
    print("\n" + "=" * 60)
    print("  TEST 2: ACCES A UN ENDPOINT PROTEGE")
    print("=" * 60)

    # Test avec le endpoint de liste des comptes
    url = f"{BASE_URL}/api/accounts/"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    print(f"\n[INFO] Requete GET {url}")
    print(f"[INFO] Header: Authorization: Bearer {token[:30]}...")

    try:
        response = requests.get(url, headers=headers)
        print(f"\n[REPONSE] Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("\n[OK] Acces autorise avec Bearer Token!")
            print(f"\nNombre de comptes: {data.get('count', len(data.get('accounts', [])))}")

            if 'accounts' in data:
                for account in data['accounts'][:3]:  # Afficher les 3 premiers
                    print(f"  - {account['email']} ({account['first_name']} {account['last_name']})")

        elif response.status_code == 401:
            print("\n[ERREUR] Non autorise - Token invalide ou expire")
            print(json.dumps(response.json(), indent=2))

        else:
            print(f"\n[ERREUR] Code: {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"\n[ERREUR] {e}")


def test_without_token():
    """Test sans token pour vérifier la protection"""
    print("\n" + "=" * 60)
    print("  TEST 3: ACCES SANS TOKEN (DOIT ECHOUER)")
    print("=" * 60)

    url = f"{BASE_URL}/api/accounts/"

    print(f"\n[INFO] Requete GET {url} sans token")

    try:
        response = requests.get(url)
        print(f"\n[REPONSE] Status: {response.status_code}")

        if response.status_code == 401:
            print("\n[OK] Protection correcte - Acces refuse sans token")
        elif response.status_code == 200:
            print("\n[ATTENTION] Endpoint non protege!")
        else:
            print(f"\n[INFO] Code: {response.status_code}")

    except Exception as e:
        print(f"\n[ERREUR] {e}")


def test_invalid_token():
    """Test avec un token invalide"""
    print("\n" + "=" * 60)
    print("  TEST 4: ACCES AVEC TOKEN INVALIDE (DOIT ECHOUER)")
    print("=" * 60)

    url = f"{BASE_URL}/api/accounts/"
    headers = {
        "Authorization": "Bearer invalid_token_12345"
    }

    print(f"\n[INFO] Requete GET {url} avec token invalide")

    try:
        response = requests.get(url, headers=headers)
        print(f"\n[REPONSE] Status: {response.status_code}")

        if response.status_code == 401:
            print("\n[OK] Validation correcte - Token invalide detecte")
        else:
            print(f"\n[ATTENTION] Code inattendu: {response.status_code}")

    except Exception as e:
        print(f"\n[ERREUR] {e}")


def decode_jwt_locally(token):
    """Décoder le JWT pour voir son contenu"""
    print("\n" + "=" * 60)
    print("  BONUS: DECODAGE DU JWT")
    print("=" * 60)

    try:
        import jwt
        # Decoder sans vérifier la signature (juste pour voir le contenu)
        payload = jwt.decode(token, options={"verify_signature": False})

        print("\n[INFO] Contenu du token JWT:")
        print(json.dumps(payload, indent=2, default=str))

    except Exception as e:
        print(f"\n[INFO] Decodage non disponible: {e}")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  TESTS D'AUTHENTIFICATION JWT BEARER")
    print("=" * 60)

    # Test 1: Connexion et génération JWT
    token = test_login_jwt()

    if token:
        # Test 2: Accès avec le Bearer Token
        test_protected_endpoint(token)

        # Test 3: Accès sans token
        test_without_token()

        # Test 4: Accès avec token invalide
        test_invalid_token()

        # Bonus: Décoder le JWT
        decode_jwt_locally(token)

    print("\n" + "=" * 60)
    print("  TESTS TERMINES")
    print("=" * 60)
    print()
