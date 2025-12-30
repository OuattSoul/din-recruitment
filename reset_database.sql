-- Script SQL pour réinitialiser la base de données PostgreSQL
-- Exécutez ce script en vous connectant à votre base de données

-- 1. Supprimer complètement le schéma public (toutes les tables)
DROP SCHEMA public CASCADE;

-- 2. Recréer le schéma public
CREATE SCHEMA public;

-- 3. Redonner les permissions à votre utilisateur
GRANT ALL ON SCHEMA public TO din_d53n_user;
GRANT ALL ON SCHEMA public TO public;

-- 4. Afficher un message de confirmation
SELECT 'Base de données réinitialisée avec succès!' AS status;
