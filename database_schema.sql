-- ============================================
-- DATABASE SCHEMA: Task Management System
-- ============================================
-- Generated from SQLAlchemy ORM Models
-- Database: SQLite (Development) / PostgreSQL (Production)
-- Date: 2026-02-01
-- ============================================

-- ============================================
-- TABLE: users
-- Description: Stores user information and profiles
-- ============================================
CREATE TABLE users (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL,  -- Allowed values: admin, manager, team_member
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    address VARCHAR(200),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for users table
CREATE UNIQUE INDEX ix_users_username ON users (username);
CREATE INDEX ix_users_id ON users (id);

-- ============================================
-- TABLE: tasks
-- Description: Stores task information and assignments
-- ============================================
CREATE TABLE tasks (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,  -- Must start with capital letter
    description VARCHAR(1000),
    priority INTEGER NOT NULL,  -- Range: 1-5
    status VARCHAR(20) NOT NULL,  -- Allowed values: pending, in_progress, completed
    assigned_to INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    FOREIGN KEY(assigned_to) REFERENCES users (id)
);

-- Indexes for tasks table
CREATE INDEX ix_tasks_id ON tasks (id);

-- ============================================
-- RELATIONSHIPS
-- ============================================
-- users.id (1) → tasks.assigned_to (Many)
-- One user can have multiple tasks assigned
-- One task can be assigned to one user (or none)

-- ============================================
-- SAMPLE DATA
-- ============================================

-- Insert sample users
INSERT INTO users (username, full_name, role, email, phone, address, created_at) VALUES
('ahmed_ali', 'Ahmed Ali', 'manager', 'ahmed@example.com', '+966501234567', 'Riyadh, Saudi Arabia', '2026-02-01 16:18:25'),
('sarah_mohammed', 'Sarah Mohammed', 'team_member', 'sarah@example.com', '+966507654321', 'Jeddah, Saudi Arabia', '2026-02-01 16:18:58');

-- Insert sample tasks
INSERT INTO tasks (title, description, priority, status, assigned_to, created_at) VALUES
('Complete database integration', 'Implement PostgreSQL with SQLAlchemy', 5, 'completed', 1, '2026-02-01 16:21:14'),
('Deploy to Railway platform', 'Setup Railway deployment with PostgreSQL', 4, 'in_progress', 2, '2026-02-01 16:22:35');

-- ============================================
-- VERIFICATION QUERIES
-- ============================================

-- View all users
-- SELECT * FROM users;

-- View all tasks
-- SELECT * FROM tasks;

-- View tasks with assigned user names
-- SELECT 
--     t.id,
--     t.title,
--     t.priority,
--     t.status,
--     u.full_name as assigned_to_user
-- FROM tasks t
-- LEFT JOIN users u ON t.assigned_to = u.id;

-- ============================================
-- POSTGRESQL VERSION (for Railway deployment)
-- ============================================
-- CREATE TABLE users (
--     id SERIAL PRIMARY KEY,
--     username VARCHAR(50) UNIQUE NOT NULL,
--     full_name VARCHAR(100) NOT NULL,
--     role VARCHAR(20) NOT NULL,
--     email VARCHAR(100) NOT NULL,
--     phone VARCHAR(20),
--     address VARCHAR(200),
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );
-- 
-- CREATE TABLE tasks (
--     id SERIAL PRIMARY KEY,
--     title VARCHAR(200) NOT NULL,
--     description VARCHAR(1000),
--     priority INTEGER NOT NULL,
--     status VARCHAR(20) NOT NULL,
--     assigned_to INTEGER REFERENCES users(id),
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     updated_at TIMESTAMP
-- );
