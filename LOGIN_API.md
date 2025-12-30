# 🔐 API de Connexion (Login) - Documentation

## Vue d'ensemble

L'API de connexion permet aux utilisateurs de s'authentifier avec leur **email** et **mot de passe** pour obtenir un token d'accès.

---

## 📡 Endpoint de connexion

### Se connecter avec email et mot de passe

**Endpoint** : `POST /api/accounts/login/`

**Permission** : Public (pas d'authentification requise)

**Body (JSON)** :
```json
{
    "email": "user@example.com",
    "password": "password123"
}
```

**Champs obligatoires** :
- `email` : Adresse email du compte
- `password` : Mot de passe du compte

---

## 📋 Réponses

### ✅ Succès (200 OK)

```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "account": {
        "id": 1,
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe"
    }
}
```

**Contenu de la réponse** :
- `access` : Token d'accès à utiliser dans les requêtes authentifiées
- `refresh` : Token de rafraîchissement pour obtenir un nouveau token d'accès
- `account` : Informations du compte connecté

---

### ❌ Erreurs possibles

#### 1. Email ou mot de passe incorrect (401 Unauthorized)
```json
{
    "error": "Email ou mot de passe incorrect"
}
```

#### 2. Champs manquants (400 Bad Request)
```json
{
    "error": "Email et mot de passe requis"
}
```

#### 3. Compte inactif (401 Unauthorized)
Le compte existe mais `is_active = False`
```json
{
    "error": "Email ou mot de passe incorrect"
}
```

---

## 🧪 Exemples d'utilisation

### Avec cURL

```bash
curl -X POST http://localhost:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

**Réponse** :
```json
{
    "access": "abc123xyz...",
    "refresh": "def456uvw...",
    "account": {
        "id": 1,
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe"
    }
}
```

---

### Avec Python (requests)

```python
import requests

url = "http://localhost:8000/api/accounts/login/"
data = {
    "email": "user@example.com",
    "password": "password123"
}

response = requests.post(url, json=data)

if response.status_code == 200:
    result = response.json()
    access_token = result['access']
    account_info = result['account']

    print(f"Connecté en tant que: {account_info['first_name']} {account_info['last_name']}")
    print(f"Access Token: {access_token}")
else:
    print(f"Erreur: {response.json()['error']}")
```

---

### Avec JavaScript (fetch)

```javascript
const url = "http://localhost:8000/api/accounts/login/";
const data = {
    email: "user@example.com",
    password: "password123"
};

fetch(url, {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
})
.then(response => response.json())
.then(result => {
    if (result.access) {
        console.log("Connecté:", result.account);
        console.log("Token:", result.access);

        // Sauvegarder le token pour les requêtes futures
        localStorage.setItem('access_token', result.access);
        localStorage.setItem('refresh_token', result.refresh);
    } else {
        console.error("Erreur:", result.error);
    }
})
.catch(error => console.error("Erreur:", error));
```

---

## 🔒 Utilisation du token d'accès

Une fois connecté, utilisez le token `access` dans l'en-tête de vos requêtes :

### Exemple : Récupérer son profil

```bash
curl -X GET http://localhost:8000/api/accounts/ \
  -H "Authorization: Bearer abc123xyz..."
```

### Exemple en JavaScript

```javascript
const token = localStorage.getItem('access_token');

fetch('http://localhost:8000/api/accounts/', {
    headers: {
        'Authorization': `Bearer ${token}`
    }
})
.then(response => response.json())
.then(data => console.log(data));
```

---

## 🔄 Flux complet : Inscription → Connexion → Utilisation

### Étape 1 : Inscription

```bash
POST /api/accounts/register/
{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone": "0612345678",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!"
}
```

### Étape 2 : Connexion

```bash
POST /api/accounts/login/
{
    "email": "john@example.com",
    "password": "SecurePass123!"
}
```

**Réponse** :
```json
{
    "access": "token123...",
    "refresh": "refresh456...",
    "account": {...}
}
```

### Étape 3 : Utiliser le token

```bash
GET /api/jobs/
Headers: Authorization: Bearer token123...
```

---

## 🧪 Tests automatisés

Un script de test complet est fourni :

```bash
python test_login.py
```

Ce script teste :
- ✅ Inscription + Connexion réussie
- ✅ Connexion avec mauvais mot de passe
- ✅ Connexion avec email inexistant
- ✅ Connexion avec champs manquants

---

## 🔐 Sécurité

### Hashage du mot de passe
- Le mot de passe est hashé avec `PBKDF2-SHA256`
- Les mots de passe ne sont jamais stockés en clair
- La comparaison se fait avec `check_password()`

### Protection contre les attaques
- ✅ Messages d'erreur génériques (pas de distinction entre "email inexistant" et "mauvais mot de passe")
- ✅ Validation des champs obligatoires
- ✅ Vérification du statut `is_active` du compte

### Tokens
- Tokens générés avec `secrets.token_urlsafe()` (cryptographiquement sécurisés)
- 32 bytes de longueur minimale
- Uniques pour chaque session

---

## 📊 Différence avec /api/auth/login/

| Endpoint | Authentification | Type d'utilisateur | Token |
|----------|------------------|-------------------|--------|
| `/api/accounts/login/` | Email + Password | Account (simple) | Custom token |
| `/api/auth/login/` | Username + Password | User (Django) | JWT standard |

**Recommandation** : Utilisez `/api/accounts/login/` pour le système Account créé.

---

## ⚠️ Note importante

Le système de tokens actuel est **simplifié**. Pour une application en production, considérez :

1. **Stocker les tokens en base** pour pouvoir les révoquer
2. **Ajouter une expiration** aux tokens
3. **Implémenter le refresh** des tokens expirés
4. **Utiliser JWT réel** avec signature et validation

Pour l'instant, le système fonctionne pour tester l'authentification de base.

---

## 🎯 Prochaines étapes

Pour améliorer le système d'authentification :

1. Créer un modèle `Token` pour stocker les tokens en base
2. Ajouter une date d'expiration
3. Implémenter `/api/accounts/logout/` pour révoquer les tokens
4. Ajouter `/api/accounts/refresh/` pour rafraîchir les tokens
5. Créer un middleware d'authentification personnalisé

---

## 📞 Support

Pour toute question :
- Consultez [INSCRIPTION_API.md](INSCRIPTION_API.md) pour l'inscription
- Consultez [STRUCTURE_PROJET.md](STRUCTURE_PROJET.md) pour l'architecture globale
