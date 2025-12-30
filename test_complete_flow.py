"""
Test du flux complet : inscription candidat + test de candidature
"""

import requests
import json

BASE_URL = "http://localhost:8000"

print("\n" + "=" * 60)
print("  TEST FLUX COMPLET")
print("=" * 60)

# 1. Connexion du candidat existant
print("\n[ETAPE 1] Connexion du candidat")
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
    print(f"[OK] Connecte en tant que: {login_data['account']['first_name']}")
    print(f"[OK] Role: {login_data['account']['role']}")
else:
    print(f"[ERREUR] {login_response.text}")
    exit(1)

# 2. Vérifier les offres d'emploi disponibles
print("\n[ETAPE 2] Verification des offres d'emploi")
headers = {"Authorization": f"Bearer {token}"}

jobs_response = requests.get(
    f"{BASE_URL}/api/jobs/",
    headers=headers
)

print(f"Status: {jobs_response.status_code}")
if jobs_response.status_code == 200:
    jobs = jobs_response.json()
    if isinstance(jobs, list):
        print(f"[INFO] Nombre d'offres disponibles: {len(jobs)}")
        if len(jobs) > 0:
            print(f"[INFO] Premiere offre: {jobs[0]}")
    else:
        print(f"[INFO] Reponse: {jobs}")
else:
    print(f"[ERREUR] {jobs_response.text}")

# 3. Tester l'accès à l'endpoint de candidature
print("\n[ETAPE 3] Acces aux candidatures")
applications_response = requests.get(
    f"{BASE_URL}/api/applications/",
    headers=headers
)

print(f"Status: {applications_response.status_code}")
if applications_response.status_code == 200:
    apps = applications_response.json()
    print(f"[OK] Acces autorise")
    print(f"[INFO] Nombre de candidatures: {len(apps) if isinstance(apps, list) else 'N/A'}")
    print(f"[INFO] Reponse: {json.dumps(apps, indent=2)}")
elif applications_response.status_code == 403:
    print(f"[ERREUR] Acces refuse: {applications_response.text}")
else:
    print(f"[ERREUR] Erreur {applications_response.status_code}: {applications_response.text}")

print("\n" + "=" * 60)
print("  FIN DES TESTS")
print("=" * 60)
