# Guide de Migration vers Account

## Ce qui a été fait

✅ **Étape 1**: Modèle Account transformé en AUTH_USER_MODEL
- Hérite maintenant de `AbstractBaseUser` et `PermissionsMixin`
- Ajout de `AccountManager` personnalisé
- Champs: email (USERNAME_FIELD), first_name, last_name, phone, role, is_active, is_staff

✅ **Étape 2**: Modèle Application mis à jour
- Utilise maintenant `settings.AUTH_USER_MODEL` au lieu de `users.User`

✅ **Étape 3**: App users désactivée
- Retirée de `INSTALLED_APPS`
- URLs commentées dans `backend/urls.py`

✅ **Étape 4**: Nouvelles migrations créées
- `accounts/migrations/0001_initial.py`
- `jobs/migrations/0001_initial.py`
- `applications/migrations/0001_initial.py`

## Ce qu'il reste à faire

### Étape 5: Réinitialiser la base de données PostgreSQL

**IMPORTANT**: Cette étape va supprimer toutes les données existantes !

#### Option A: Utiliser psql en ligne de commande

```bash
psql -U postgres -d recruitment_db -f fix_database.sql
```

#### Option B: Utiliser pgAdmin

1. Ouvrez pgAdmin
2. Connectez-vous à votre serveur PostgreSQL
3. Sélectionnez la base de données `recruitment_db`
4. Ouvrez l'outil Query Tool (Tools > Query Tool)
5. Exécutez ce SQL:

```sql
DROP SCHEMA IF EXISTS public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;
```

### Étape 6: Appliquer les migrations

Une fois la base de données réinitialisée, exécutez:

```bash
python manage.py migrate
```

### Étape 7: Créer le compte admin

```bash
python create_admin_direct.py
```

Ou utilisez la commande Django:

```bash
python manage.py createsuperuser
```

Informations:
- Email: admin@din-africa.net
- Password: 09876
- First name: Admin
- Last name: DIN Africa

### Étape 8: Tester

```bash
python test_jwt_bearer.py
```

## Changements importants

### 1. Création de compte

L'inscription créera maintenant des comptes `Account` avec le rôle "candidate" par défaut:

```bash
curl -X POST http://localhost:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jean",
    "last_name": "Dupont",
    "email": "jean@example.com",
    "phone": "0612345678",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!"
  }'
```

### 2. Connexion

```bash
curl -X POST http://localhost:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@din-africa.net",
    "password": "09876"
  }'
```

### 3. Candidature

Les candidats pourront maintenant postuler car `Application.candidate` référence `accounts.Account`:

```bash
curl -X POST http://localhost:8000/api/applications/ \
  -H "Content-Type: multipart/form-data" \
  -H "Authorization: Bearer <token>" \
  -F "job=1" \
  -F "cv=@chemin/vers/cv.pdf" \
  -F "cover_letter=Ma lettre de motivation"
```

## Rôles disponibles

- **candidate** (défaut): Peut postuler aux offres
- **admin**: Peut gérer les candidatures et offres
- **superadmin**: Accès complet

## Structure des permissions

Les permissions existantes dans `common/permissions.py` fonctionnent maintenant avec Account:
- `IsSuperAdmin`
- `IsAdmin`
- `IsCandidate`
- `IsOwnerOrAdmin`
- `IsAdminOrReadOnly`

## Support Django Admin

Le compte admin peut maintenant se connecter à `/admin/` avec:
- Email: admin@din-africa.net
- Password: 09876

Le `is_staff=True` sera défini automatiquement pour les superadmins.
