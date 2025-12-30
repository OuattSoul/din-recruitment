# 🔐 Login avec Email - Guide Rapide

## ✨ Nouveau endpoint créé

**Connexion avec email et mot de passe** :
```
POST /api/accounts/login/
```

---

## 🚀 Utilisation rapide

### 1. Inscription (si pas encore de compte)

```bash
curl -X POST http://localhost:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Jean","last_name":"Dupont","email":"jean@example.com","phone":"0612345678","password":"test123","password_confirm":"test123"}'
```

### 2. Connexion avec email

```bash
curl -X POST http://localhost:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"jean@example.com","password":"test123"}'
```

**Réponse** :
```json
{
    "access": "abc123xyz...",
    "refresh": "def456uvw...",
    "account": {
        "id": 1,
        "email": "jean@example.com",
        "first_name": "Jean",
        "last_name": "Dupont"
    }
}
```

---

## 📋 Format de la requête

**Champs requis** :
- `email` : Email du compte
- `password` : Mot de passe

**Exemple** :
```json
{
    "email": "user@example.com",
    "password": "password123"
}
```

---

## ✅ Test automatisé

Testez facilement avec le script fourni :

```bash
python test_login.py
```

Ce script teste :
- ✅ Inscription + Connexion
- ✅ Mauvais mot de passe
- ✅ Email inexistant
- ✅ Champs manquants

---

## 🔒 Sécurité

- ✅ Mot de passe hashé (PBKDF2-SHA256)
- ✅ Vérification du compte actif
- ✅ Tokens sécurisés générés
- ✅ Messages d'erreur génériques

---

## 📡 Endpoints disponibles

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/api/accounts/register/` | POST | Créer un compte |
| `/api/accounts/login/` | POST | Se connecter |
| `/api/accounts/` | GET | Lister les comptes |

---

## 📚 Documentation complète

Pour plus de détails, consultez [LOGIN_API.md](LOGIN_API.md)

---

## 🧪 Exemple complet

```python
import requests

# 1. Inscription
response = requests.post('http://localhost:8000/api/accounts/register/', json={
    "first_name": "Marie",
    "last_name": "Martin",
    "email": "marie@example.com",
    "phone": "0698765432",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!"
})
print("Compte créé:", response.json())

# 2. Connexion
response = requests.post('http://localhost:8000/api/accounts/login/', json={
    "email": "marie@example.com",
    "password": "SecurePass123!"
})

if response.status_code == 200:
    data = response.json()
    token = data['access']
    account = data['account']

    print(f"Connecté: {account['first_name']} {account['last_name']}")
    print(f"Token: {token}")

    # 3. Utiliser le token pour d'autres requêtes
    headers = {'Authorization': f'Bearer {token}'}
    # ... vos requêtes authentifiées
```

---

## ⚡ Différence avec `/api/auth/login/`

| Feature | `/api/accounts/login/` | `/api/auth/login/` |
|---------|----------------------|-------------------|
| Champ login | **email** | username |
| Type compte | Account | User Django |
| Token | Custom | JWT standard |

**Utilisez `/api/accounts/login/`** pour votre système Account actuel.

---

## 📞 Support

Consultez :
- [README_INSCRIPTION.md](README_INSCRIPTION.md) - Guide inscription
- [LOGIN_API.md](LOGIN_API.md) - Documentation login complète
- [INSCRIPTION_API.md](INSCRIPTION_API.md) - Documentation inscription complète
