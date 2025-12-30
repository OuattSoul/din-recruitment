# 📋 Structure du Projet - Plateforme de Recrutement

## Vue d'ensemble

Ce projet Django REST Framework gère une plateforme de recrutement avec 3 types d'utilisateurs :
- **Superadmin** : tous les droits
- **Admin** : gestion des offres d'emploi et des candidatures
- **Candidat** : consultation des offres et soumission de candidatures

---

## 🗂️ Structure du Projet

```
recruitment_backend/
├── backend/              # Configuration Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/               # Gestion des utilisateurs
│   ├── models.py        # Modèle User avec rôles
│   ├── views.py         # API utilisateurs
│   ├── serializers.py   # Serializers par rôle
│   └── urls.py
├── jobs/                # Gestion des offres d'emploi
│   ├── models.py        # Modèle JobOffer
│   ├── views.py         # API offres
│   ├── serializers.py
│   └── urls.py
├── applications/        # Gestion des candidatures
│   ├── models.py        # Modèle Application
│   ├── views.py         # API candidatures
│   ├── serializers.py
│   └── urls.py
└── common/              # Utilities partagées
    └── permissions.py   # Permissions personnalisées
```

---

## 👥 Modèles de Données

### User (users/models.py)
```python
Champs principaux:
- username, email, password
- role: 'superadmin' | 'admin' | 'candidate'
- first_name, last_name
- phone, country
- resume (fichier)
- linkedin_url, portfolio_url
- bio, skills (JSON)
```

### JobOffer (jobs/models.py)
```python
Champs principaux:
- title, company, location
- contract_type: CDI, CDD, Stage, etc.
- salary, description
- skills (JSON)
- status: 'draft' | 'published' | 'closed'
- created_by (ForeignKey vers User)
- application_deadline
```

### Application (applications/models.py)
```python
Champs principaux:
- candidate (ForeignKey vers User)
- job (ForeignKey vers JobOffer)
- cv (fichier)
- cover_letter
- status: 'pending' | 'reviewed' | 'accepted' | 'rejected'
```

---

## 🔐 Système de Permissions

### Permissions Personnalisées (common/permissions.py)

| Permission | Description |
|------------|-------------|
| `IsSuperAdmin` | Vérifie que l'utilisateur est superadmin |
| `IsAdmin` | Vérifie que l'utilisateur est admin ou superadmin |
| `IsCandidate` | Vérifie que l'utilisateur est candidat |
| `IsAdminOrReadOnly` | Admins peuvent modifier, autres lisent uniquement |
| `IsOwnerOrAdmin` | Utilisateur propriétaire ou admin |

---

## 📡 Endpoints API

### Authentification
```
POST /api/auth/login/          # Connexion (obtenir JWT token)
POST /api/auth/refresh/        # Rafraîchir le token
```

### Users (api/users/)
```
POST   /api/users/register/          # Inscription candidat (public)
POST   /api/users/create_admin/      # Créer admin (superadmin uniquement)
GET    /api/users/profile/           # Profil utilisateur connecté
PUT    /api/users/update_profile/    # Modifier profil
GET    /api/users/                   # Liste utilisateurs (selon rôle)
```

### Jobs (api/jobs/)
```
GET    /api/jobs/                    # Liste offres (publiées pour tous)
POST   /api/jobs/                    # Créer offre (admin uniquement)
GET    /api/jobs/{id}/               # Détail offre
PUT    /api/jobs/{id}/               # Modifier offre (admin uniquement)
DELETE /api/jobs/{id}/               # Supprimer offre (admin uniquement)

# Actions personnalisées
GET    /api/jobs/my_offers/          # Mes offres créées (admin)
POST   /api/jobs/{id}/publish/       # Publier offre (admin)
POST   /api/jobs/{id}/close/         # Fermer offre (admin)
```

### Applications (api/applications/)
```
GET    /api/applications/            # Liste candidatures (selon rôle)
POST   /api/applications/            # Postuler (candidat uniquement)
GET    /api/applications/{id}/       # Détail candidature
PUT    /api/applications/{id}/       # Modifier candidature
DELETE /api/applications/{id}/       # Supprimer candidature (si pending)

# Actions personnalisées (admin uniquement)
POST   /api/applications/{id}/review/   # Marquer comme revue
POST   /api/applications/{id}/accept/   # Accepter candidature
POST   /api/applications/{id}/reject/   # Rejeter candidature
```

---

## 🎯 Règles Métier par Rôle

### Superadmin
- ✅ Tous les droits
- ✅ Créer des admins et superadmins
- ✅ Gérer tous les utilisateurs
- ✅ Accès complet aux offres et candidatures

### Admin
- ✅ Créer/modifier/supprimer des offres d'emploi
- ✅ Voir toutes les candidatures
- ✅ Modifier le statut des candidatures (review, accept, reject)
- ✅ Voir la liste des candidats
- ❌ Ne peut pas créer d'autres admins
- ❌ Ne peut pas supprimer des utilisateurs

### Candidat
- ✅ Consulter les offres publiées
- ✅ Postuler aux offres
- ✅ Voir et modifier ses propres candidatures (si status=pending)
- ✅ Mettre à jour son profil
- ❌ Ne peut pas voir les autres candidats
- ❌ Ne peut pas créer d'offres d'emploi
- ❌ Ne peut pas modifier le statut de ses candidatures

---

## 🚀 Installation et Démarrage

### 1. Réinitialiser la base de données

Si vous avez des problèmes de migrations, connectez-vous à PostgreSQL et exécutez :

```sql
-- Option 1: Supprimer toutes les tables
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO din_d53n_user;
```

OU créez une nouvelle base de données dans votre dashboard Render.

### 2. Appliquer les migrations

```bash
python manage.py migrate
```

### 3. Créer un superadmin

```bash
python manage.py createsuperuser
```

### 4. Lancer le serveur

```bash
python manage.py runserver
```

---

## 📝 Exemples d'utilisation

### Inscription d'un candidat
```bash
POST /api/users/register/
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+33612345678",
    "country": "France"
}
```

### Connexion
```bash
POST /api/auth/login/
{
    "username": "john_doe",
    "password": "SecurePass123!"
}

Réponse:
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Créer une offre (Admin)
```bash
POST /api/jobs/
Headers: Authorization: Bearer <access_token>
{
    "title": "Développeur Python",
    "company": "TechCorp",
    "location": "Paris",
    "contract_type": "cdi",
    "salary": "45000-55000€",
    "description": "Nous recherchons un développeur Python...",
    "skills": ["Python", "Django", "PostgreSQL"],
    "application_deadline": "2025-02-28",
    "status": "published"
}
```

### Postuler à une offre (Candidat)
```bash
POST /api/applications/
Headers: Authorization: Bearer <access_token>
Content-Type: multipart/form-data
{
    "job": 1,
    "cv": <fichier_cv.pdf>,
    "cover_letter": "Je suis très intéressé par ce poste..."
}
```

---

## ⚙️ Configuration REST Framework

Dans `backend/settings.py` :

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}
```

Cela signifie que **par défaut**, toutes les routes nécessitent une authentification JWT, sauf si explicitement configuré autrement (comme `/register/`).

---

## 🐛 Résolution de Problèmes

### Erreur: "Model class users.models.User doesn't declare an explicit app_label"
➡️ Vérifiez que `'users'` est bien dans `INSTALLED_APPS`

### Erreur: "InconsistentMigrationHistory"
➡️ Réinitialisez les migrations en supprimant la table `django_migrations` de PostgreSQL

### Erreur: "basename argument not specified"
➡️ Ajoutez `basename` dans le router: `router.register("", ViewSet, basename="name")`

---

## 📊 Résumé des Accès

| Action | Superadmin | Admin | Candidat | Public |
|--------|:----------:|:-----:|:--------:|:------:|
| Voir offres publiées | ✅ | ✅ | ✅ | ✅ |
| Créer offre | ✅ | ✅ | ❌ | ❌ |
| Modifier offre | ✅ | ✅ | ❌ | ❌ |
| Postuler | ✅ | ✅ | ✅ | ❌ |
| Voir toutes candidatures | ✅ | ✅ | ❌ | ❌ |
| Voir mes candidatures | ✅ | ✅ | ✅ | ❌ |
| Accepter/Rejeter candidature | ✅ | ✅ | ❌ | ❌ |
| Créer admin | ✅ | ❌ | ❌ | ❌ |
| S'inscrire | - | - | - | ✅ |

---

## 🔧 Prochaines Étapes Recommandées

1. **Ajoutez CORS** si vous avez un frontend séparé :
   ```bash
   pip install django-cors-headers
   ```

2. **Configurez les emails** pour les notifications de candidature

3. **Ajoutez la pagination** dans les ViewSets

4. **Créez des tests unitaires** pour chaque endpoint

5. **Documentez l'API** avec drf-spectacular (Swagger)

6. **Ajoutez des filtres** et recherche sur les offres

7. **Implémentez un système de notifications** pour les candidats

---

## 📞 Support

Pour toute question sur la structure du projet, référez-vous à ce document ou consultez le code source qui est commenté.
