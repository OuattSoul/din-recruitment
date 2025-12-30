"""
Test direct de la fonction generate_jwt_tokens_for_account
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from accounts.models import Account
from accounts.authentication import generate_jwt_tokens_for_account

# Récupérer le compte admin
account = Account.objects.get(email="admin@din-africa.net")

# Générer les tokens
tokens = generate_jwt_tokens_for_account(account)

print("=== TOKENS GENERES ===")
print(f"Account ID: {tokens['account']['id']}")
print(f"Account Email: {tokens['account']['email']}")
print(f"Account Name: {tokens['account']['first_name']} {tokens['account']['last_name']}")
print(f"Account Role: {tokens['account'].get('role', 'MISSING!')}")
