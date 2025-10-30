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


-- Create trigger function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';


-- Create triggers for automatic timestamp updates
CREATE TRIGGER update_grooming_sessions_updated_at
    BEFORE UPDATE ON grooming_sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();


-- Create indexes for better performance
CREATE INDEX idx_grooming_sessions_real_time_channel_name ON grooming_sessions(real_time_channel_name);