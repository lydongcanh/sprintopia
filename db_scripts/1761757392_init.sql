-- Drop existing tables and types if they exist
DROP TABLE IF EXISTS grooming_sessions CASCADE;
DROP TYPE IF EXISTS entity_status CASCADE;


-- Create ENUM types
CREATE TYPE entity_status AS ENUM (
    'active',
    'disabled',
    'deleted'
);


-- Create tables
CREATE TABLE grooming_sessions (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    real_time_channel_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    status entity_status DEFAULT 'active'
);