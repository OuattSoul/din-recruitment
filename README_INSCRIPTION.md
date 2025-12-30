# 🎯 Endpoint d'Inscription - Guide Rapide

## ✨ Ce qui a été créé

Une API d'inscription complète permettant de créer des comptes avec :
- Prénoms
- Nom
- Email
- Téléphone
- Mot de passe

---

## 📍 Endpoints

### 1️⃣ Créer un compte
```
POST /api/accounts/register/
```

**Body** :
```json
{
    "first_name": "Jean",
    "last_name": "Dupont",
    "email": "jean.dupont@example.com",
    "phone": "0612345678",
    "password": "SecurePassword123!",
    "password_confirm": "SecurePassword123!"
}
```

**Réponse (201)** :
```json
{
    "message": "Compte créé avec succès",
    "account": {
        "id": 1,
        "first_name": "Jean",
        "last_name": "Dupont",
        "email": "jean.dupont@example.com",
        "phone": "0612345678",
        "created_at": "2025-12-29T10:30:00Z"
    }
}
```

### 2️⃣ Lister les comptes
```
GET /api/accounts/
```

**Réponse (200)** :
```json
{
    "count": 1,
    "accounts": [...]
}
```

---

## 🚀 Démarrage Rapide

### Étape 1: Réinitialiser la base de données

⚠️ **IMPORTANT** : Vous devez réinitialiser PostgreSQL car il y a un conflit de migrations.

**Option A** : Créer une nouvelle base sur Render
1. Allez sur render.com dashboard
2. Créez une nouvelle database PostgreSQL
3. Copiez la connection string
4. Mettez-la dans `backend/settings.py`

**Option B** : Réinitialiser la base existante
```sql
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO din_d53n_user;
```

### Étape 2: Appliquer les migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Étape 3: Lancer le serveur
```bash
python manage.py runserver
```

### Étape 4: Tester l'API
```bash
# Option 1: Avec le script de test
python test_inscription.py

# Option 2: Avec curl
curl -X POST http://localhost:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jean",
    "last_name": "Dupont",
    "email": "jean@example.com",
    "phone": "0612345678",
    "password": "Pass123!",
    "password_confirm": "Pass123!"
  }'
```

---

## 📁 Fichiers créés

```
accounts/
├── models.py          # Modèle Account
├── serializers.py     # Validation et sérialisation
├── views.py           # API endpoints
├── urls.py            # Routes
├── admin.py           # Interface admin Django
└── migrations/
    └── __init__.py

INSCRIPTION_API.md     # Documentation complète
test_inscription.py    # Script de test
```

---

## 🔒 Sécurité

✅ Mot de passe automatiquement hashé (PBKDF2-SHA256)
✅ Email unique (pas de doublons)
✅ Validation des mots de passe correspondants
✅ Validation des champs obligatoires

---

## 🎨 Interface Admin

L'app est accessible via l'admin Django :
```
http://localhost:8000/admin/accounts/account/
```

Vous pouvez :
- Voir tous les comptes
- Rechercher par nom, email, téléphone
- Filtrer par statut et date de création

---

## 📚 Documentation complète

Pour plus de détails, consultez [INSCRIPTION_API.md](INSCRIPTION_API.md)

---

## ✅ Checklist

- [x] Modèle Account créé
- [x] Serializers de validation créés
- [x] Endpoints d'inscription et listage
- [x] Interface admin configurée
- [x] Documentation complète
- [x] Script de test fourni
- [ ] **Migrations à appliquer** ⚠️
- [ ] Tests à exécuter

---

## 🐛 Problème actuel

**Conflit de migrations** : La base de données PostgreSQL a des migrations incohérentes. Vous DEVEZ réinitialiser la base avant de continuer.

Suivez les instructions à l'Étape 1 ci-dessus.

---

## 💡 Prochaines étapes suggérées

1. Réinitialiser la base de données
2. Appliquer toutes les migrations
3. Tester l'endpoint d'inscription
4. Créer un superuser : `python manage.py createsuperuser`
5. Accéder à l'admin Django
6. Intégrer avec votre frontend

---

## 📞 Questions ?

Consultez :
- [INSCRIPTION_API.md](INSCRIPTION_API.md) - Documentation API complète
- [STRUCTURE_PROJET.md](STRUCTURE_PROJET.md) - Architecture globale du projet
