# 📝 API d'Inscription - Documentation

## Vue d'ensemble

L'API d'inscription permet de créer de nouveaux comptes utilisateurs avec les informations suivantes :
- Prénom(s)
- Nom
- Email
- Téléphone
- Mot de passe

## 🔧 Modèle Account

Le modèle `Account` est défini dans `accounts/models.py` :

```python
class Account(models.Model):
    first_name = models.CharField(max_length=100)  # Prénom(s)
    last_name = models.CharField(max_length=100)   # Nom
    email = models.EmailField(unique=True)         # Email (unique)
    phone = models.CharField(max_length=20)        # Téléphone
    password = models.CharField(max_length=128)    # Mot de passe (hashé)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
```

**Note importante** : Le mot de passe est automatiquement hashé avant la sauvegarde.

---

## 📡 Endpoints disponibles

### 1. Créer un compte

**Endpoint** : `POST /api/accounts/register/`

**Permission** : Public (pas d'authentification requise)

**Body (JSON)** :
```json
{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "0612345678",
    "password": "SecurePassword123!",
    "password_confirm": "SecurePassword123!"
}
```

**Champs obligatoires** :
- `first_name` : Prénom(s) de l'utilisateur
- `last_name` : Nom de famille
- `email` : Adresse email (doit être unique)
- `phone` : Numéro de téléphone
- `password` : Mot de passe
- `password_confirm` : Confirmation du mot de passe (doit correspondre)

**Réponse réussie (201 Created)** :
```json
{
    "message": "Compte créé avec succès",
    "account": {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "0612345678",
        "created_at": "2025-12-29T10:30:00Z"
    }
}
```

**Erreurs possibles** :

1. **Email déjà existant (400 Bad Request)** :
```json
{
    "email": ["Un compte avec cet email existe déjà."]
}
```

2. **Mots de passe non correspondants (400 Bad Request)** :
```json
{
    "password": "Les mots de passe ne correspondent pas."
}
```

3. **Champ manquant (400 Bad Request)** :
```json
{
    "first_name": ["This field is required."]
}
```

---

### 2. Lister tous les comptes

**Endpoint** : `GET /api/accounts/`

**Permission** : Public (pas d'authentification requise)

**Réponse (200 OK)** :
```json
{
    "count": 2,
    "accounts": [
        {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "0612345678",
            "created_at": "2025-12-29T10:30:00Z"
        },
        {
            "id": 2,
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com",
            "phone": "0698765432",
            "created_at": "2025-12-29T11:00:00Z"
        }
    ]
}
```

---

## 🧪 Exemples d'utilisation

### Avec cURL

#### Créer un compte
```bash
curl -X POST http://localhost:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "0612345678",
    "password": "SecurePassword123!",
    "password_confirm": "SecurePassword123!"
  }'
```

#### Lister les comptes
```bash
curl -X GET http://localhost:8000/api/accounts/
```

---

### Avec Python (requests)

#### Créer un compte
```python
import requests

url = "http://localhost:8000/api/accounts/register/"
data = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "0612345678",
    "password": "SecurePassword123!",
    "password_confirm": "SecurePassword123!"
}

response = requests.post(url, json=data)
print(response.status_code)
print(response.json())
```

#### Lister les comptes
```python
import requests

url = "http://localhost:8000/api/accounts/"
response = requests.get(url)

data = response.json()
print(f"Total comptes: {data['count']}")
for account in data['accounts']:
    print(f"- {account['first_name']} {account['last_name']} ({account['email']})")
```

---

### Avec JavaScript (fetch)

#### Créer un compte
```javascript
const url = "http://localhost:8000/api/accounts/register/";
const data = {
    first_name: "John",
    last_name: "Doe",
    email: "john.doe@example.com",
    phone: "0612345678",
    password: "SecurePassword123!",
    password_confirm: "SecurePassword123!"
};

fetch(url, {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error("Erreur:", error));
```

#### Lister les comptes
```javascript
const url = "http://localhost:8000/api/accounts/";

fetch(url)
    .then(response => response.json())
    .then(data => {
        console.log(`Total: ${data.count} comptes`);
        data.accounts.forEach(account => {
            console.log(`${account.first_name} ${account.last_name} - ${account.email}`);
        });
    });
```

---

## 🔒 Sécurité

### Hashage du mot de passe
Le mot de passe est automatiquement hashé à l'aide de l'algorithme `PBKDF2-SHA256` avant d'être stocké en base de données. Cela se fait dans la méthode `save()` du modèle :

```python
def save(self, *args, **kwargs):
    if not self.pk or 'pbkdf2_sha256' not in self.password:
        self.password = make_password(self.password)
    super().save(*args, **kwargs)
```

### Unicité de l'email
Le champ `email` est défini avec `unique=True`, ce qui garantit qu'aucun compte ne peut être créé avec un email déjà utilisé.

### Validation
Le serializer valide :
- Que tous les champs requis sont présents
- Que l'email n'existe pas déjà
- Que les deux mots de passe correspondent

---

## 🚀 Installation et démarrage

### 1. Ajouter l'app aux settings

Dans `backend/settings.py`, l'app `accounts` a été ajoutée :
```python
INSTALLED_APPS = [
    # ...
    "accounts",
    # ...
]
```

### 2. Créer les migrations

**IMPORTANT** : En raison d'un conflit de migrations existant, vous devez d'abord réinitialiser votre base de données PostgreSQL.

#### Option A : Créer une nouvelle base de données
1. Connectez-vous à votre dashboard Render
2. Créez une nouvelle base de données PostgreSQL
3. Récupérez la nouvelle connection string
4. Mettez à jour `backend/settings.py` avec la nouvelle URL

#### Option B : Réinitialiser la base existante
Connectez-vous à PostgreSQL et exécutez :
```sql
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO din_d53n_user;
```

### 3. Appliquer les migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Lancer le serveur

```bash
python manage.py runserver
```

Le endpoint sera disponible à : `http://localhost:8000/api/accounts/register/`

---

## 📊 Structure des fichiers

```
accounts/
├── __init__.py
├── models.py          # Modèle Account
├── serializers.py     # AccountRegistrationSerializer, AccountSerializer
├── views.py           # register_account, list_accounts
├── urls.py            # Routes
├── admin.py
├── apps.py
└── migrations/
    └── __init__.py
```

---

## 🔍 Admin Django

Pour gérer les comptes via l'admin Django, ajoutez dans `accounts/admin.py` :

```python
from django.contrib import admin
from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'phone', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at', 'password']
```

---

## 🧩 Intégration avec le reste de l'API

Cette API d'inscription est **indépendante** du système utilisateur principal (`users.User`).

Si vous souhaitez intégrer les deux :
1. Après la création d'un `Account`, vous pouvez créer automatiquement un `User` correspondant
2. Ou vous pouvez utiliser uniquement le système `Account` pour gérer l'authentification

---

## ✅ Checklist de test

- [ ] Créer un compte avec des données valides
- [ ] Vérifier que le mot de passe est hashé en base
- [ ] Tenter de créer un compte avec un email existant
- [ ] Vérifier la validation des mots de passe non correspondants
- [ ] Lister tous les comptes actifs
- [ ] Vérifier que le mot de passe n'apparaît pas dans les réponses

---

## 📞 Support

Pour toute question, consultez :
- [STRUCTURE_PROJET.md](STRUCTURE_PROJET.md) pour l'architecture globale
- Les fichiers dans `accounts/` pour l'implémentation
