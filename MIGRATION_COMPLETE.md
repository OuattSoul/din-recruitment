# ✅ Migration Complète vers Account

## Résumé

La migration du modèle `User` vers `Account` est **terminée avec succès** ! Le système utilise maintenant `accounts.Account` comme modèle d'utilisateur principal avec authentification JWT Bearer Token.

## Ce qui a été fait

### 1. Transformation du modèle Account ✅
- `Account` hérite maintenant de `AbstractBaseUser` et `PermissionsMixin`
- Ajout de `AccountManager` avec méthodes `create_user()` et `create_superuser()`
- Champs principaux:
  - `email` (USERNAME_FIELD, unique)
  - `first_name`, `last_name`
  - `phone`
  - `role` (superadmin, admin, candidate)
  - `is_active`, `is_staff`
  - `password` (hashé via `set_password()`)

### 2. Configuration Django ✅
- `AUTH_USER_MODEL = "accounts.Account"` dans settings.py
- App `users` désactivée (commentée dans INSTALLED_APPS)
- URLs `/api/users/` commentées

### 3. Modèles mis à jour ✅
- `Application.candidate` → utilise `settings.AUTH_USER_MODEL`
- `JobOffer.created_by` → utilise `settings.AUTH_USER_MODEL`

### 4. Hashing des mots de passe corrigé ✅
- Scripts de création utilisent `Account.objects.create_user()`
- Serializer d'inscription utilise `create_user()`
- Les mots de passe sont maintenant correctement hashés avec `set_password()`

### 5. Migrations créées ✅
- `accounts/migrations/0001_initial.py`
- `jobs/migrations/0001_initial.py`
- `applications/migrations/0001_initial.py`

### 6. Tests validés ✅
- ✅ Authentification JWT Bearer Token
- ✅ Inscription de candidat
- ✅ Connexion avec email/password
- ✅ Accès aux endpoints protégés
- ✅ Vérification des rôles (admin, candidate)

## Endpoints disponibles

### Publics (AllowAny)
- `POST /api/accounts/register/` - Inscription (rôle "candidate" par défaut)
- `POST /api/accounts/login/` - Connexion (retourne JWT tokens)

### Protégés (Bearer Token requis)
- `GET /api/accounts/` - Liste des comptes
- `GET /api/applications/` - Liste des candidatures (filtrées par rôle)
- `POST /api/applications/` - Créer une candidature (candidats uniquement)
- `GET /api/jobs/` - Liste des offres d'emploi

## Comptes créés

### Admin
- **Email**: admin@din-africa.net
- **Password**: 09876
- **Role**: admin
- **is_staff**: True (peut accéder à /admin/)

### Candidat de test
- **Email**: jean.dupont@example.com
- **Password**: SecurePass123!
- **Role**: candidate

## Utilisation

### 1. Inscription d'un nouveau candidat

```bash
curl -X POST http://localhost:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Marie",
    "last_name": "Martin",
    "email": "marie@example.com",
    "phone": "0698765432",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!"
  }'
```

### 2. Connexion

```bash
curl -X POST http://localhost:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jean.dupont@example.com",
    "password": "SecurePass123!"
  }'
```

**Réponse**:
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "account": {
    "id": 5,
    "email": "jean.dupont@example.com",
    "first_name": "Jean",
    "last_name": "Dupont",
    "role": "candidate"
  }
}
```

### 3. Accès à un endpoint protégé

```bash
curl -X GET http://localhost:8000/api/applications/ \
  -H "Authorization: Bearer <access_token>"
```

### 4. Créer une candidature (candidat uniquement)

```bash
curl -X POST http://localhost:8000/api/applications/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: multipart/form-data" \
  -F "job=1" \
  -F "cv=@/chemin/vers/cv.pdf" \
  -F "cover_letter=Ma lettre de motivation"
```

## Structure des rôles

### Candidate (par défaut)
- Peut s'inscrire via `/api/accounts/register/`
- Peut voir ses propres candidatures
- Peut créer de nouvelles candidatures
- Peut modifier/supprimer ses candidatures (status=pending uniquement)

### Admin
- Peut voir toutes les candidatures
- Peut modifier le statut des candidatures
- Peut créer/modifier/supprimer des offres d'emploi
- Peut accéder à `/admin/` (si is_staff=True)

### Superadmin
- Accès complet à tout
- is_staff et is_superuser automatiquement à True

## Permissions

Le système utilise les permissions de `common/permissions.py`:
- `IsSuperAdmin` - Vérifie `role == "superadmin"`
- `IsAdmin` - Vérifie `role in ["admin", "superadmin"]`
- `IsCandidate` - Vérifie `role == "candidate"`
- `IsOwnerOrAdmin` - Propriétaire ou admin
- `IsAdminOrReadOnly` - Admin peut modifier, autres lecture seule

## JWT Token

### Format du payload
```json
{
  "account_id": 5,
  "email": "jean@example.com",
  "first_name": "Jean",
  "last_name": "Dupont",
  "role": "candidate",
  "type": "access",
  "exp": 1767060437,
  "iat": 1767056837
}
```

### Expiration
- **Access token**: 1 heure
- **Refresh token**: 7 jours

## Scripts utiles

- `python create_admin_direct.py` - Créer le compte admin
- `python test_jwt_bearer.py` - Tester l'authentification JWT
- `python test_candidate_application.py` - Tester inscription + candidature
- `python fix_existing_accounts.py` - Supprimer les anciens comptes mal hashés

## Admin Django

Pour accéder à l'interface d'administration Django:

1. Naviguez vers http://localhost:8000/admin/
2. Connectez-vous avec:
   - Email: admin@din-africa.net
   - Password: 09876

## Prochaines étapes suggérées

1. **Créer des offres d'emploi** via l'admin ou l'API
2. **Tester une candidature complète** avec un vrai fichier CV
3. **Implémenter la gestion des rôles** pour créer des admins via l'API
4. **Ajouter un endpoint de refresh token** pour renouveler les access tokens
5. **Implémenter la réinitialisation de mot de passe** par email

## Notes importantes

⚠️ **Mot de passe**: Tous les nouveaux comptes doivent être créés via:
- `Account.objects.create_user()` (dans le code)
- `/api/accounts/register/` (via l'API)
- `python manage.py createsuperuser` (pour les superusers)

⚠️ **Ne jamais** utiliser `Account.objects.create()` directement car il ne hashera pas le mot de passe.

⚠️ **Base de données**: Si vous devez réinitialiser la base de données, utilisez [fix_database.sql](fix_database.sql) puis `python manage.py migrate`.
