-- Initialize databases for all services
CREATE DATABASE user_db;
CREATE DATABASE tournament_db;
CREATE DATABASE submission_db;
CREATE DATABASE rank_db;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE user_db TO postgres;
GRANT ALL PRIVILEGES ON DATABASE tournament_db TO postgres;
GRANT ALL PRIVILEGES ON DATABASE submission_db TO postgres;
GRANT ALL PRIVILEGES ON DATABASE rank_db TO postgres;
