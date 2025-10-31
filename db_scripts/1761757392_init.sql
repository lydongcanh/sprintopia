-- Drop existing tables and types if they exist
DROP TYPE IF EXISTS entity_status CASCADE;

DROP TABLE IF EXISTS grooming_sessions CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS estimation_turns CASCADE;
DROP TABLE IF EXISTS user_estimation_turns CASCADE;


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

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    external_auth_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    status entity_status DEFAULT 'active'
);

CREATE TABLE estimation_turns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    grooming_session_id UUID REFERENCES grooming_sessions(id) ON DELETE CASCADE,
    is_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    status entity_status DEFAULT 'active'
);

CREATE TABLE user_estimation_turns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    estimation_turn_id UUID REFERENCES estimation_turns(id) ON DELETE CASCADE,
    estimation_value FLOAT NOT NULL,
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

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_estimation_turns_updated_at
    BEFORE UPDATE ON estimation_turns
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_estimation_turns_updated_at
    BEFORE UPDATE ON user_estimation_turns
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();


-- Create indexes for better performance
CREATE INDEX idx_grooming_sessions_real_time_channel_name ON grooming_sessions(real_time_channel_name);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_estimation_turns_grooming_session_id ON estimation_turns(grooming_session_id);
CREATE INDEX idx_user_estimation_turns_user_id ON user_estimation_turns(user_id);
CREATE INDEX idx_user_estimation_turns_estimation_turn_id ON user_estimation_turns(estimation_turn_id);