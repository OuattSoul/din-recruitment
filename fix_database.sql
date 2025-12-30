-- Script to fix the PostgreSQL database schema

-- Drop the existing schema if it exists (this will remove all tables)
DROP SCHEMA IF EXISTS public CASCADE;

-- Recreate the public schema
CREATE SCHEMA public;

-- Grant necessary permissions
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;
