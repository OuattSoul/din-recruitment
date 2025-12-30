# API de Candidature - Documentation

## Nouveau modèle de candidature

Le modèle de candidature a été mis à jour avec tous les champs nécessaires pour une candidature complète.

## Champs de la candidature

### Informations obligatoires

#### Informations personnelles
- **civility** (enum): Civilité
  - Valeurs: `monsieur`, `madame`, `mademoiselle`
- **first_name** (string): Prénom(s)
- **last_name** (string): Nom
- **email** (string): Email
- **phone** (string): Téléphone
- **country** (string): Pays
- **address** (text): Adresse complète

#### Informations professionnelles
- **contract_type_sought** (enum): Type de contrat recherché
  - Valeurs: `cdi`, `cdd`, `stage`, `alternance`, `interim`, `freelance`, `temps_partiel`
- **experience** (array): Liste des expériences professionnelles
  - Format: tableau de textes
  - Exemple: `["Développeur chez ABC (2020-2023)", "Stagiaire chez XYZ (2019)"]`
- **education_level** (string): Niveau d'études
  - Exemple: "Master en Informatique", "Licence Pro", etc.
- **expected_salary** (integer): Prétention salariale
  - Valeur: entier (montant en devise locale)

### Informations facultatives
- **current_salary** (integer): Salaire actuel
  - Valeur: entier ou null

### Champs automatiques
- **candidate**: Automatiquement rempli avec l'utilisateur connecté
- **status**: Automatiquement défini à "pending"
- **created_at**: Date de création automatique
- **updated_at**: Date de mise à jour automatique

## Exemples d'utilisation

### 1. Créer une candidature

**Endpoint**: `POST /api/applications/`

**Headers**:
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Body (JSON)**:
```json
{
  "job": 1,
  "civility": "monsieur",
  "first_name": "Jean",
  "last_name": "Dupont",
  "email": "jean.dupont@example.com",
  "phone": "0612345678",
  "country": "France",
  "address": "123 Rue de la Paix, 75001 Paris",
  "contract_type_sought": "cdi",
  "experience": [
    "Développeur Full Stack chez TechCorp (2020-2023) - React, Node.js, PostgreSQL",
    "Développeur Junior chez StartupXYZ (2018-2020) - PHP, MySQL",
    "Stage de développement chez WebAgency (2017-2018)"
  ],
  "education_level": "Master en Informatique - Université Paris Diderot",
  "current_salary": 45000,
  "expected_salary": 55000
}
```

**Réponse (201 Created)**:
```json
{
  "id": 1,
  "candidate": 5,
  "candidate_name": "Jean Dupont",
  "job": 1,
  "job_title": "Développeur Full Stack",
  "civility": "monsieur",
  "civility_display": "Monsieur",
  "first_name": "Jean",
  "last_name": "Dupont",
  "email": "jean.dupont@example.com",
  "phone": "0612345678",
  "country": "France",
  "address": "123 Rue de la Paix, 75001 Paris",
  "contract_type_sought": "cdi",
  "contract_type_display": "CDI",
  "experience": [
    "Développeur Full Stack chez TechCorp (2020-2023) - React, Node.js, PostgreSQL",
    "Développeur Junior chez StartupXYZ (2018-2020) - PHP, MySQL",
    "Stage de développement chez WebAgency (2017-2018)"
  ],
  "education_level": "Master en Informatique - Université Paris Diderot",
  "current_salary": 45000,
  "expected_salary": 55000,
  "status": "pending",
  "status_display": "En attente",
  "created_at": "2025-12-30T02:00:00Z",
  "updated_at": "2025-12-30T02:00:00Z"
}
```

### 2. Lister ses candidatures

**Endpoint**: `GET /api/applications/`

**Headers**:
```
Authorization: Bearer <access_token>
```

**Réponse (200 OK)**:
```json
[
  {
    "id": 1,
    "candidate": 5,
    "candidate_name": "Jean Dupont",
    "job": 1,
    "job_title": "Développeur Full Stack",
    "civility": "monsieur",
    "civility_display": "Monsieur",
    "first_name": "Jean",
    "last_name": "Dupont",
    "email": "jean.dupont@example.com",
    "phone": "0612345678",
    "country": "France",
    "address": "123 Rue de la Paix, 75001 Paris",
    "contract_type_sought": "cdi",
    "contract_type_display": "CDI",
    "experience": [...],
    "education_level": "Master en Informatique",
    "current_salary": 45000,
    "expected_salary": 55000,
    "status": "pending",
    "status_display": "En attente",
    "created_at": "2025-12-30T02:00:00Z",
    "updated_at": "2025-12-30T02:00:00Z"
  }
]
```

### 3. Exemple avec curl

```bash
# 1. Connexion
TOKEN=$(curl -s -X POST http://localhost:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"jean.dupont@example.com","password":"SecurePass123!"}' \
  | python -c "import sys, json; print(json.load(sys.stdin)['access'])")

# 2. Créer une candidature
curl -X POST http://localhost:8000/api/applications/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "job": 1,
    "civility": "monsieur",
    "first_name": "Jean",
    "last_name": "Dupont",
    "email": "jean.dupont@example.com",
    "phone": "0612345678",
    "country": "France",
    "address": "123 Rue de la Paix, 75001 Paris",
    "contract_type_sought": "cdi",
    "experience": [
      "Développeur Full Stack chez TechCorp (2020-2023)",
      "Développeur Junior chez StartupXYZ (2018-2020)"
    ],
    "education_level": "Master en Informatique",
    "current_salary": 45000,
    "expected_salary": 55000
  }'
```

## Validation

### Règles de validation

1. **civility**: Doit être `monsieur`, `madame` ou `mademoiselle`
2. **contract_type_sought**: Doit être une des valeurs valides
3. **experience**: Doit être un tableau (array)
4. **expected_salary**: Doit être > 0
5. **current_salary**: Si fourni, doit être > 0
6. **email**: Doit être un email valide
7. **Tous les champs obligatoires** doivent être fournis

### Erreurs de validation

**Exemple**: Salaire invalide
```json
{
  "expected_salary": ["La prétention salariale doit être supérieure à 0"]
}
```

**Exemple**: Expérience invalide
```json
{
  "experience": ["L'expérience doit être une liste"]
}
```

## Permissions

### Candidats
- ✅ **Créer** leurs propres candidatures
- ✅ **Lire** uniquement leurs candidatures
- ✅ **Modifier** leurs candidatures (si status = "pending")
- ✅ **Supprimer** leurs candidatures (si status = "pending")

### Admins
- ✅ **Lire** toutes les candidatures
- ✅ **Modifier** le statut des candidatures
- ✅ **Supprimer** n'importe quelle candidature

### Actions admin disponibles
- `POST /api/applications/{id}/review/` - Marquer comme examinée
- `POST /api/applications/{id}/accept/` - Accepter la candidature
- `POST /api/applications/{id}/reject/` - Rejeter la candidature

## Statuts de candidature

1. **pending** (En attente): Candidature soumise, en attente d'examen
2. **reviewed** (Examinée): Candidature examinée par un admin
3. **accepted** (Acceptée): Candidature acceptée
4. **rejected** (Rejetée): Candidature rejetée

## Notes

- Le champ `candidate` est automatiquement rempli avec l'utilisateur connecté
- Seuls les utilisateurs avec le rôle "candidate" peuvent créer des candidatures
- Le champ `current_salary` est optionnel
- Le tableau `experience` peut contenir autant d'éléments que nécessaire
- Les données sont validées avant la création
