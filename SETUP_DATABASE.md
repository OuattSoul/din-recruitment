# Guide de Configuration de la Base de Données

## Problème
La base de données PostgreSQL n'a pas le schéma `public`, ce qui empêche Django de créer les tables.

## Solution

### Étape 1: Recréer le schéma PostgreSQL

Exécutez le fichier SQL pour recréer le schéma public:

```bash
psql -U postgres -d recruitment_db -f fix_database.sql
```

**Ou** si vous utilisez pgAdmin:
1. Ouvrez pgAdmin
2. Connectez-vous à votre serveur PostgreSQL
3. Sélectionnez la base de données `recruitment_db`
4. Ouvrez l'outil Query Tool
5. Copiez et exécutez le contenu de `fix_database.sql`:
   ```sql
   DROP SCHEMA IF EXISTS public CASCADE;
   CREATE SCHEMA public;
   GRANT ALL ON SCHEMA public TO postgres;
   GRANT ALL ON SCHEMA public TO public;
   ```

### Étape 2: Appliquer les migrations Django

Une fois le schéma créé, exécutez les migrations:

```bash
# Appliquer toutes les migrations
python manage.py migrate

# Créer le compte admin
python create_admin_direct.py
```

### Étape 3: Vérifier l'installation

Testez l'authentification JWT:

```bash
python test_jwt_bearer.py
```

## Informations sur le Compte Admin

Après avoir exécuté les migrations et créé le compte admin:

- **Email**: admin@din-africa.net
- **Password**: 09876
- **Role**: admin

## Endpoints Disponibles

- `POST /api/accounts/register/` - Créer un nouveau compte
- `POST /api/accounts/login/` - Se connecter (retourne des tokens JWT)
- `GET /api/accounts/` - Lister les comptes (protégé - nécessite Bearer token)

## Format d'Authentification

Utilisez le header suivant pour les endpoints protégés:

```
Authorization: Bearer <votre_access_token>
```

## Exemple de Requête

```bash
# Login
curl -X POST http://localhost:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@din-africa.net","password":"09876"}'

# Accès endpoint protégé
curl -X GET http://localhost:8000/api/accounts/ \
  -H "Authorization: Bearer <access_token>"
```
