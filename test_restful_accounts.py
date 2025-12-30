"""
Test des endpoints RESTful pour les comptes
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import requests
import random

BASE_URL = "http://localhost:8000"

def test_restful_endpoints():
    print("="*70)
    print("TEST DES ENDPOINTS RESTFUL ACCOUNTS")
    print("="*70)

    # 1. POST /api/accounts/ - Créer un compte (inscription publique)
    print("\n1. POST /api/accounts/ - Créer un nouveau compte")
    email = f"test.user.{random.randint(1000, 9999)}@example.com"
    r = requests.post(f"{BASE_URL}/api/accounts/", json={
        "first_name": "Test",
        "last_name": "User",
        "email": email,
        "phone": "0123456789",
        "password": "test123",
        "password_confirm": "test123"
    })
    print(f"   Status: {r.status_code}")
    if r.status_code == 201:
        new_user_id = r.json()['account']['id']
        print(f"   ✓ Compte créé (ID: {new_user_id})")
    else:
        print(f"   ✗ Échec: {r.text[:200]}")
        return

    # Login avec le nouveau compte
    r = requests.post(f"{BASE_URL}/api/accounts/login/", json={
        'email': email,
        'password': 'test123'
    })
    user_token = r.json()['access']
    user_headers = {"Authorization": f"Bearer {user_token}"}

    # Login admin
    r = requests.post(f"{BASE_URL}/api/accounts/login/", json={
        'email': 'admin@example.com',
        'password': 'admin123'
    })
    admin_token = r.json()['access']
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    # 2. GET /api/accounts/ - Lister les comptes
    print("\n2. GET /api/accounts/ - Lister tous les comptes (admin)")
    r = requests.get(f"{BASE_URL}/api/accounts/", headers=admin_headers)
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"   ✓ Comptes récupérés: {data['count']} compte(s)")
    else:
        print(f"   ✗ Échec: {r.text[:200]}")

    # 3. GET /api/accounts/<id>/ - Récupérer un compte spécifique
    print(f"\n3. GET /api/accounts/{new_user_id}/ - Récupérer son propre compte")
    r = requests.get(f"{BASE_URL}/api/accounts/{new_user_id}/", headers=user_headers)
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"   ✓ Compte récupéré: {data['email']}")
    else:
        print(f"   ✗ Échec: {r.text[:200]}")

    # 4. PATCH /api/accounts/<id>/ - Mettre à jour un compte
    print(f"\n4. PATCH /api/accounts/{new_user_id}/ - Mettre à jour le téléphone")
    new_phone = f"06{random.randint(10000000, 99999999)}"
    r = requests.patch(f"{BASE_URL}/api/accounts/{new_user_id}/",
                      headers=user_headers,
                      json={"phone": new_phone})
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"   ✓ Téléphone mis à jour: {data['account']['phone']}")
    else:
        print(f"   ✗ Échec: {r.text[:200]}")

    # 5. PUT /api/accounts/<id>/ - Mise à jour complète
    print(f"\n5. PUT /api/accounts/{new_user_id}/ - Mise à jour complète (doit échouer - champs manquants)")
    r = requests.put(f"{BASE_URL}/api/accounts/{new_user_id}/",
                     headers=user_headers,
                     json={"phone": "0987654321"})
    print(f"   Status: {r.status_code}")
    if r.status_code == 400:
        print(f"   ✓ Échec attendu (champs requis manquants)")
    else:
        print(f"   Note: Status {r.status_code}")

    # 6. DELETE /api/accounts/<id>/ - Supprimer un compte
    print(f"\n6. DELETE /api/accounts/{new_user_id}/ - Supprimer le compte")
    r = requests.delete(f"{BASE_URL}/api/accounts/{new_user_id}/", headers=user_headers)
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        print(f"   ✓ Compte supprimé (soft delete)")

        # Vérifier que le compte n'est plus accessible
        r = requests.get(f"{BASE_URL}/api/accounts/{new_user_id}/", headers=admin_headers)
        if r.status_code == 404:
            print(f"   ✓ Compte n'est plus accessible")
    else:
        print(f"   ✗ Échec: {r.text[:200]}")

    # 7. Test permissions - utilisateur ne peut pas voir un autre compte
    print(f"\n7. Test permissions - Candidat essaie d'accéder au compte admin")
    r = requests.post(f"{BASE_URL}/api/accounts/login/", json={
        'email': 'candidat@example.com',
        'password': 'candidat123'
    })
    if r.status_code == 200:
        candidate_token = r.json()['access']
        candidate_headers = {"Authorization": f"Bearer {candidate_token}"}

        r = requests.get(f"{BASE_URL}/api/accounts/1/", headers=candidate_headers)
        print(f"   Status: {r.status_code}")
        if r.status_code == 403:
            print(f"   ✓ Accès refusé (403 Forbidden)")
        else:
            print(f"   ✗ Le candidat ne devrait pas avoir accès")

    print("\n" + "="*70)
    print("✅ TESTS TERMINÉS!")
    print("="*70)
    print("\nNouveaux endpoints RESTful:")
    print("  POST   /api/accounts/         - Créer un compte (public)")
    print("  GET    /api/accounts/         - Lister tous les comptes")
    print("  GET    /api/accounts/<id>/    - Récupérer un compte")
    print("  PATCH  /api/accounts/<id>/    - Mettre à jour un compte")
    print("  PUT    /api/accounts/<id>/    - Mise à jour complète")
    print("  DELETE /api/accounts/<id>/    - Supprimer un compte")
    print("\nEndpoints de compatibilité:")
    print("  POST   /api/accounts/register/ - Créer un compte (DEPRECATED)")
    print("  POST   /api/accounts/login/    - Se connecter")

if __name__ == '__main__':
    test_restful_endpoints()
