-- AVTech Platform - Database Initialization
-- ==========================================

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create database if not exists (this will be handled by Docker)
-- CREATE DATABASE IF NOT EXISTS avtech_db;

-- Set timezone
SET timezone = 'UTC';

-- Create indexes for better performance
-- These will be created after the tables are created by SQLAlchemy

-- Create a function to update the updated_at column
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE avtech_db TO avtech_user;
GRANT ALL PRIVILEGES ON SCHEMA public TO avtech_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO avtech_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO avtech_user;

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO avtech_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO avtech_user;
