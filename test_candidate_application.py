"""
Test complet : inscription candidat + candidature
"""

import requests
import json

BASE_URL = "http://localhost:8000"

print("\n" + "=" * 60)
print("  TEST COMPLET: CANDIDAT ET CANDIDATURE")
print("=" * 60)

# 1. Inscription d'un nouveau candidat
print("\n[ETAPE 1] Inscription d'un nouveau candidat")
register_data = {
    "first_name": "Jean",
    "last_name": "Dupont",
    "email": "jean.dupont@example.com",
    "phone": "0612345678",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!"
}

register_response = requests.post(
    f"{BASE_URL}/api/accounts/register/",
    json=register_data
)

print(f"Status: {register_response.status_code}")
if register_response.status_code == 201:
    print("[OK] Compte candidat cree avec succes")
    print(json.dumps(register_response.json(), indent=2))
else:
    print(f"[ERREUR] {register_response.text}")
    exit(1)

# 2. Connexion du candidat
print("\n[ETAPE 2] Connexion du candidat")
login_response = requests.post(
    f"{BASE_URL}/api/accounts/login/",
    json={
        "email": "jean.dupont@example.com",
        "password": "SecurePass123!"
    }
)

print(f"Status: {login_response.status_code}")
if login_response.status_code == 200:
    login_data = login_response.json()
    token = login_data['access']
    print("[OK] Connexion reussie")
    print(f"Role: {login_data['account']['role']}")
else:
    print(f"[ERREUR] {login_response.text}")
    exit(1)

# 3. Vérifier que le candidat peut lister ses candidatures (vide pour l'instant)
print("\n[ETAPE 3] Liste des candidatures du candidat")
headers = {"Authorization": f"Bearer {token}"}

applications_response = requests.get(
    f"{BASE_URL}/api/applications/",
    headers=headers
)

print(f"Status: {applications_response.status_code}")
if applications_response.status_code == 200:
    print("[OK] Acces autorise")
    print(f"Nombre de candidatures: {len(applications_response.json())}")
else:
    print(f"[ERREUR] {applications_response.text}")

print("\n" + "=" * 60)
print("  TESTS TERMINES")
print("=" * 60)
print("\n[INFO] Le candidat peut maintenant postuler aux offres d'emploi")
print("[INFO] Pour creer une candidature, utilisez:")
print("  POST /api/applications/")
print("  avec les champs: job, cv, cover_letter")
