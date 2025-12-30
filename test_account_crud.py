"""
Script pour tester les opérations CRUD sur les comptes
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import requests
import json

BASE_URL = "http://localhost:8000"

def get_token(email, password):
    """Obtenir un token JWT"""
    url = f"{BASE_URL}/api/accounts/login/"
    response = requests.post(url, json={"email": email, "password": password})
    if response.status_code == 200:
        return response.json()['access']
    return None

def test_get_account(token, account_id):
    """Test GET account by ID"""
    print(f"\n{'='*60}")
    print(f"TEST: GET /api/accounts/{account_id}/")
    print('='*60)

    url = f"{BASE_URL}/api/accounts/{account_id}/"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"✓ Compte récupéré avec succès!")
        print(f"  ID: {data['id']}")
        print(f"  Nom: {data['first_name']} {data['last_name']}")
        print(f"  Email: {data['email']}")
        print(f"  Rôle: {data['role_display']}")
        return True
    else:
        print(f"✗ Échec: {response.text}")
        return False

def test_update_account(token, account_id):
    """Test PATCH account by ID"""
    print(f"\n{'='*60}")
    print(f"TEST: PATCH /api/accounts/{account_id}/update/")
    print('='*60)

    url = f"{BASE_URL}/api/accounts/{account_id}/update/"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "first_name": "Jean-Updated",
        "phone": "0987654321"
    }

    response = requests.patch(url, json=data, headers=headers)
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print(f"✓ {result['message']}")
        print(f"  Nouveau nom: {result['account']['first_name']}")
        print(f"  Nouveau téléphone: {result['account']['phone']}")
        return True
    else:
        print(f"✗ Échec: {response.text}")
        return False

def test_delete_account(token, account_id):
    """Test DELETE account by ID"""
    print(f"\n{'='*60}")
    print(f"TEST: DELETE /api/accounts/{account_id}/delete/")
    print('='*60)

    url = f"{BASE_URL}/api/accounts/{account_id}/delete/"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.delete(url, headers=headers)
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print(f"✓ {result['message']}")
        return True
    else:
        print(f"✗ Échec: {response.text}")
        return False

def test_permissions():
    """Test des permissions - un utilisateur ne peut pas accéder au compte d'un autre"""
    print(f"\n{'='*60}")
    print("TEST: Permissions - Accès refusé à un compte d'un autre utilisateur")
    print('='*60)

    # Connexion en tant que candidat
    candidate_token = get_token("candidat@example.com", "candidat123")
    if not candidate_token:
        print("✗ Impossible de se connecter en tant que candidat")
        return False

    # Essayer d'accéder au compte admin (ID 1)
    url = f"{BASE_URL}/api/accounts/1/"
    headers = {"Authorization": f"Bearer {candidate_token}"}

    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")

    if response.status_code == 403:
        print("✓ Accès refusé correctement (403 Forbidden)")
        print(f"  Message: {response.json().get('error')}")
        return True
    else:
        print(f"✗ Erreur: Le candidat ne devrait pas avoir accès à ce compte")
        return False

def test_admin_access():
    """Test que l'admin peut accéder à tous les comptes"""
    print(f"\n{'='*60}")
    print("TEST: Permissions - Admin peut accéder à tous les comptes")
    print('='*60)

    # Connexion en tant qu'admin
    admin_token = get_token("admin@example.com", "admin123")
    if not admin_token:
        print("✗ Impossible de se connecter en tant qu'admin")
        return False

    # Essayer d'accéder au compte candidat (ID 2)
    url = f"{BASE_URL}/api/accounts/2/"
    headers = {"Authorization": f"Bearer {admin_token}"}

    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print("✓ Admin peut accéder aux comptes des autres utilisateurs")
        print(f"  Compte consulté: {data['first_name']} {data['last_name']}")
        return True
    else:
        print(f"✗ Erreur: L'admin devrait avoir accès à tous les comptes")
        return False

def main():
    print("="*60)
    print("TEST DES OPÉRATIONS CRUD SUR LES COMPTES")
    print("="*60)

    # Connexion en tant qu'admin
    print("\n1. Connexion en tant qu'admin...")
    admin_token = get_token("admin@example.com", "admin123")
    if not admin_token:
        print("✗ Impossible de continuer sans token admin")
        return
    print("✓ Connexion admin réussie")

    # Connexion en tant que candidat
    print("\n2. Connexion en tant que candidat...")
    candidate_token = get_token("candidat@example.com", "candidat123")
    if not candidate_token:
        print("✗ Impossible de continuer sans token candidat")
        return
    print("✓ Connexion candidat réussie")

    # Test GET account (candidat consulte son propre compte - ID 2)
    test_get_account(candidate_token, 2)

    # Test PATCH account (candidat met à jour son propre compte)
    test_update_account(candidate_token, 2)

    # Test permissions (candidat essaie d'accéder au compte admin)
    test_permissions()

    # Test admin access (admin consulte le compte du candidat)
    test_admin_access()

    # Test DELETE account (créer un nouveau compte puis le supprimer)
    print(f"\n{'='*60}")
    print("TEST: Création et suppression d'un compte de test")
    print('='*60)

    # Créer un nouveau compte
    register_url = f"{BASE_URL}/api/accounts/register/"
    new_account = {
        "first_name": "Test",
        "last_name": "User",
        "email": "test.delete@example.com",
        "phone": "0000000000",
        "password": "test123",
        "password_confirm": "test123"
    }

    response = requests.post(register_url, json=new_account)
    if response.status_code == 201:
        test_account_id = response.json()['account']['id']
        print(f"✓ Compte de test créé (ID: {test_account_id})")

        # Se connecter avec ce compte
        test_token = get_token("test.delete@example.com", "test123")
        if test_token:
            # Supprimer le compte
            test_delete_account(test_token, test_account_id)
    else:
        print(f"✗ Échec de création du compte de test: {response.text}")

    print("\n" + "="*60)
    print("TESTS TERMINÉS")
    print("="*60)

    print("\nEndpoints disponibles:")
    print("  GET    /api/accounts/<id>/         - Récupérer un compte")
    print("  PATCH  /api/accounts/<id>/update/  - Mettre à jour un compte")
    print("  DELETE /api/accounts/<id>/delete/  - Supprimer un compte")
    print("\nPermissions:")
    print("  - Les utilisateurs peuvent gérer leur propre compte")
    print("  - Les admins peuvent gérer tous les comptes")
    print("  - Seuls les admins peuvent modifier le rôle d'un utilisateur")

if __name__ == '__main__':
    main()
