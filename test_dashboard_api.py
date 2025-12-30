"""
Script pour tester le dashboard admin
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import requests
import json

BASE_URL = "http://localhost:8000"

def get_admin_token():
    """Obtenir le token JWT pour l'admin"""
    url = f"{BASE_URL}/api/accounts/login/"
    data = {
        "email": "admin@example.com",
        "password": "admin123"
    }

    print("1. Tentative de connexion admin...")
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            token_data = response.json()
            print("✓ Connexion réussie!")
            print(f"   Access Token: {token_data['access'][:50]}...")
            return token_data['access']
        else:
            print(f"✗ Échec de connexion: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        print("✗ Impossible de se connecter au serveur. Est-il démarré?")
        print("   Lancez: python manage.py runserver")
        return None

def test_dashboard_stats(token):
    """Tester l'endpoint des statistiques du dashboard"""
    url = f"{BASE_URL}/api/applications/dashboard_stats/"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    print("\n2. Accès aux statistiques du dashboard...")
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            stats = response.json()
            print("✓ Statistiques récupérées avec succès!")
            print("\n   DASHBOARD STATISTIQUES:")
            print("   " + "="*50)
            print(f"   Total de candidatures: {stats.get('total', 0)}")
            print(f"   Candidatures spontanées: {stats.get('spontanees', 0)}")
            print(f"   Candidatures sur offres: {stats.get('sur_offres', 0)}")
            print(f"   Candidatures intérim: {stats.get('interim', 0)}")
            print(f"   Candidatures en évaluation: {stats.get('evaluations', 0)}")
            print("   " + "="*50)
            return True
        else:
            print(f"✗ Échec: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Erreur: {str(e)}")
        return False

def test_filters(token):
    """Tester les différents filtres"""
    headers = {
        "Authorization": f"Bearer {token}"
    }

    print("\n3. Test des filtres...")

    # Test 1: Candidatures spontanées
    print("\n   a) Candidatures spontanées:")
    url = f"{BASE_URL}/api/applications/?is_spontaneous=true"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', data) if isinstance(data, dict) else data
        print(f"      ✓ Trouvées: {len(results)} candidature(s)")
        for app in results:
            print(f"         - {app['first_name']} {app['last_name']} ({app['contract_type_sought']})")

    # Test 2: Candidatures intérim
    print("\n   b) Candidatures intérim:")
    url = f"{BASE_URL}/api/applications/?contract_type_sought=interim"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', data) if isinstance(data, dict) else data
        print(f"      ✓ Trouvées: {len(results)} candidature(s)")
        for app in results:
            print(f"         - {app['first_name']} {app['last_name']}")

    # Test 3: Candidatures en évaluation
    print("\n   c) Candidatures en évaluation (reviewed):")
    url = f"{BASE_URL}/api/applications/?status=reviewed"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', data) if isinstance(data, dict) else data
        print(f"      ✓ Trouvées: {len(results)} candidature(s)")
        for app in results:
            print(f"         - {app['first_name']} {app['last_name']} - {app['status_display']}")

    # Test 4: Candidatures complétées
    print("\n   d) Candidatures complétées:")
    url = f"{BASE_URL}/api/applications/?application_status=completed"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', data) if isinstance(data, dict) else data
        print(f"      ✓ Trouvées: {len(results)} candidature(s)")

    # Test 5: Recherche par email
    print("\n   e) Recherche par email (marie):")
    url = f"{BASE_URL}/api/applications/?search=marie"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', data) if isinstance(data, dict) else data
        print(f"      ✓ Trouvées: {len(results)} candidature(s)")
        for app in results:
            print(f"         - {app['email']}")

def main():
    print("="*60)
    print("TEST DU DASHBOARD ADMIN - AUTHENTIFICATION JWT")
    print("="*60)

    # Étape 1: Obtenir le token
    token = get_admin_token()
    if not token:
        print("\n✗ Impossible de continuer sans token")
        return

    # Étape 2: Tester le dashboard
    success = test_dashboard_stats(token)
    if not success:
        print("\n✗ Échec du test du dashboard")
        return

    # Étape 3: Tester les filtres
    test_filters(token)

    print("\n" + "="*60)
    print("TESTS TERMINÉS AVEC SUCCÈS!")
    print("="*60)
    print("\nPour tester manuellement dans le navigateur ou Postman:")
    print("1. POST http://localhost:8000/api/accounts/login/")
    print("   Body: {\"email\": \"admin@example.com\", \"password\": \"admin123\"}")
    print("\n2. GET http://localhost:8000/api/applications/dashboard_stats/")
    print("   Header: Authorization: Bearer <votre_token>")
    print("\n3. Exemples de filtres:")
    print("   - /api/applications/?is_spontaneous=true")
    print("   - /api/applications/?contract_type_sought=cdi")
    print("   - /api/applications/?status=reviewed")
    print("   - /api/applications/?application_status=completed")
    print("   - /api/applications/?search=jean")

if __name__ == '__main__':
    main()
