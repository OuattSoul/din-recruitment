"""
Test rapide pour vérifier le champ role
"""

import requests
import json

BASE_URL = "http://localhost:8000"

# 1. Connexion
login_response = requests.post(
    f"{BASE_URL}/api/accounts/login/",
    json={"email": "admin@din-africa.net", "password": "09876"}
)

print("=== REPONSE LOGIN ===")
print(json.dumps(login_response.json(), indent=2))

token = login_response.json()['access']

# 2. Accès endpoint protégé
accounts_response = requests.get(
    f"{BASE_URL}/api/accounts/",
    headers={"Authorization": f"Bearer {token}"}
)

print("\n=== REPONSE LIST ACCOUNTS ===")
print(json.dumps(accounts_response.json(), indent=2))
