CREATE DATABASE IF NOT EXISTS login_db;

USE login_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Insert sample data
INSERT INTO users (username, password) VALUES ('user1', 'password123');

