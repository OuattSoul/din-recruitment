import sys
sys.stdout.reconfigure(encoding='utf-8')
import requests

BASE_URL = "http://localhost:8000"

# 1. Login
print("1. Login...")
r = requests.post(f"{BASE_URL}/api/accounts/login/", json={
    'email': 'admin@example.com',
    'password': 'admin123'
})
if r.status_code != 200:
    print(f"✗ Login failed: {r.status_code}")
    exit(1)

token = r.json()['access']
print(f"✓ Login successful")

headers = {"Authorization": f"Bearer {token}"}

# 2. Test GET account by ID
print("\n2. Test GET /api/accounts/1/")
r = requests.get(f"{BASE_URL}/api/accounts/1/", headers=headers)
print(f"Status: {r.status_code}")
if r.status_code == 200:
    data = r.json()
    print(f"✓ Account retrieved: {data['first_name']} {data['last_name']} ({data['email']})")
else:
    print(f"✗ Failed: {r.text[:200]}")

# 3. Test PATCH account
print("\n3. Test PATCH /api/accounts/1/update/")
r = requests.patch(f"{BASE_URL}/api/accounts/1/update/",
                   headers=headers,
                   json={"phone": "0999999999"})
print(f"Status: {r.status_code}")
if r.status_code == 200:
    data = r.json()
    print(f"✓ Account updated: Phone = {data['account']['phone']}")
else:
    print(f"✗ Failed: {r.text[:200]}")

# 4. Test DELETE account (on a test account)
print("\n4. Test DELETE account")
# Create a test account first
r = requests.post(f"{BASE_URL}/api/accounts/register/", json={
    "first_name": "Test",
    "last_name": "Delete",
    "email": "test.delete.now@example.com",
    "phone": "0000000000",
    "password": "test123",
    "password_confirm": "test123"
})

if r.status_code == 201:
    test_id = r.json()['account']['id']
    print(f"✓ Test account created (ID: {test_id})")

    # Login with test account
    r = requests.post(f"{BASE_URL}/api/accounts/login/", json={
        'email': 'test.delete.now@example.com',
        'password': 'test123'
    })
    test_token = r.json()['access']
    test_headers = {"Authorization": f"Bearer {test_token}"}

    # Delete it
    r = requests.delete(f"{BASE_URL}/api/accounts/{test_id}/delete/", headers=test_headers)
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        print(f"✓ Account deleted successfully")
    else:
        print(f"✗ Failed: {r.text[:200]}")
else:
    print(f"✗ Could not create test account: {r.text[:200]}")

print("\n" + "="*60)
print("TESTS COMPLETED!")
print("="*60)
