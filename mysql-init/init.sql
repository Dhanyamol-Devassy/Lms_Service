CREATE DATABASE IF NOT EXISTS lms_users;
CREATE DATABASE IF NOT EXISTS lms_books;
CREATE DATABASE IF NOT EXISTS lms_borrowing;

-- Create user and grant privileges
CREATE USER IF NOT EXISTS 'lms_user1'@'%' IDENTIFIED BY 'lms_pass1';
GRANT ALL PRIVILEGES ON lms_users.* TO 'lms_user1'@'%';
GRANT ALL PRIVILEGES ON lms_books.* TO 'lms_user1'@'%';
GRANT ALL PRIVILEGES ON lms_borrowing.* TO 'lms_user1'@'%';
FLUSH PRIVILEGES;

-- lms_users schema
USE lms_users;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    role VARCHAR(50),  -- ✅ Add this line
    borrowed_books TEXT
);


-- Sample users with bcrypt-hashed passwords and roles
INSERT INTO users (name, email, password, role) VALUES
('Alice Smith', 'alice@example.com', '$2b$12$on3.rwWZ8hSDZ6lCNEf3ruSTuRhULqP1gubzOcKAsz6tx1d0E4zQa', 'admin'),
('Bob Johnson', 'bob@example.com', '$2b$12$gNPi7r9oeSTnW9BePB2fweAJoUmEejG5Uby14NKLgiKIK1JhN1VqG', 'librarian');

-- lms_books schema
USE lms_books;

CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    isbn VARCHAR(20) UNIQUE,
    available BOOLEAN DEFAULT TRUE
);

-- Sample books
INSERT INTO books (title, author, isbn, available) VALUES
('Clean Code', 'Robert C. Martin', '9780132350884', TRUE),
('The Pragmatic Programmer', 'Andrew Hunt', '9780201616224', TRUE),
('Design Patterns', 'Erich Gamma', '9780201633610', TRUE);

-- lms_borrowing schema
USE lms_borrowing;

CREATE TABLE IF NOT EXISTS borrowing (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    book_id INT NOT NULL,
    borrowed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    returned BOOLEAN DEFAULT FALSE
);
