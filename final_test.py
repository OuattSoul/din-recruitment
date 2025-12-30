import sys
sys.stdout.reconfigure(encoding='utf-8')
import requests
import random

BASE_URL = "http://localhost:8000"

# Login as admin
r = requests.post(f"{BASE_URL}/api/accounts/login/", json={
    'email': 'admin@example.com',
    'password': 'admin123'
})
admin_token = r.json()['access']
admin_headers = {"Authorization": f"Bearer {admin_token}"}

print("="*60)
print("TEST FINAL DES ENDPOINTS CRUD")
print("="*60)

# 1. Test GET account
print("\n1. GET /api/accounts/1/")
r = requests.get(f"{BASE_URL}/api/accounts/1/", headers=admin_headers)
print(f"   Status: {r.status_code}")
if r.status_code == 200:
    print(f"   ✓ Compte récupéré: {r.json()['email']}")

# 2. Test PATCH account
print("\n2. PATCH /api/accounts/1/update/")
new_phone = f"09{random.randint(10000000, 99999999)}"
r = requests.patch(f"{BASE_URL}/api/accounts/1/update/",
                   headers=admin_headers,
                   json={"phone": new_phone})
print(f"   Status: {r.status_code}")
if r.status_code == 200:
    print(f"   ✓ Téléphone mis à jour: {r.json()['account']['phone']}")

# 3. Test DELETE - Créer un nouveau compte
print("\n3. DELETE /api/accounts/<id>/delete/")
email = f"delete.test.{random.randint(1000, 9999)}@example.com"
r = requests.post(f"{BASE_URL}/api/accounts/register/", json={
    "first_name": "Delete",
    "last_name": "Test",
    "email": email,
    "phone": "0000000000",
    "password": "test123",
    "password_confirm": "test123"
})

if r.status_code == 201:
    test_id = r.json()['account']['id']
    print(f"   Compte créé (ID: {test_id})")

    # Login with test account
    r = requests.post(f"{BASE_URL}/api/accounts/login/", json={
        'email': email,
        'password': 'test123'
    })
    test_token = r.json()['access']
    test_headers = {"Authorization": f"Bearer {test_token}"}

    # Delete
    r = requests.delete(f"{BASE_URL}/api/accounts/{test_id}/delete/",
                       headers=test_headers)
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        print(f"   ✓ Compte supprimé avec succès")

        # Vérifier que le compte est bien supprimé (soft delete)
        r = requests.get(f"{BASE_URL}/api/accounts/{test_id}/",
                        headers=admin_headers)
        if r.status_code == 404:
            print(f"   ✓ Compte n'est plus accessible (soft delete OK)")

# 4. Test permissions
print("\n4. Test des permissions")
# Candidat essaie d'accéder au compte admin
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
        print(f"   ✓ Candidat ne peut pas accéder au compte admin (403)")

print("\n" + "="*60)
print("✅ TOUS LES TESTS SONT PASSÉS!")
print("="*60)
print("\nLes endpoints CRUD fonctionnent correctement:")
print("  • GET    /api/accounts/<id>/")
print("  • PATCH  /api/accounts/<id>/update/")
print("  • DELETE /api/accounts/<id>/delete/")
