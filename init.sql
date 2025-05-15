-- Create ENUM types
DO $$ BEGIN
    CREATE TYPE status_enum AS ENUM ('active', 'inactive');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE type_enum AS ENUM ('primary', 'secondary', 'foreign_language', 'redirected');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;


-- Create companies table
CREATE TABLE IF NOT EXISTS companies (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    status status_enum NOT NULL
);

-- Seed companies
INSERT INTO companies (id, name, status) VALUES
(1, 'Apple Company', 'active'),
(2, 'Banana Company', 'active');


-- Create domains table
CREATE TABLE IF NOT EXISTS domains (
    id SERIAL PRIMARY KEY,
    domain TEXT NOT NULL,
    status status_enum NOT NULL,
    type type_enum NOT NULL,
    company_id INTEGER NOT NULL,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

-- Seed domains
INSERT INTO domains (domain, status, type, company_id) VALUES
('apple.com', 'active', 'primary', 1),
('apple.dev', 'inactive', 'secondary', 1),
('banana.co', 'active', 'primary', 2),
('banana.io', 'active', 'foreign_language', 2);