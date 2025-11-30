-- Init script for Question 3
-- Creates database, user, tables and a stored procedure

DROP DATABASE IF EXISTS quizdb;
CREATE DATABASE quizdb
    DEFAULT CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE quizdb;

-- Create a user for the application
DROP USER IF EXISTS 'quizuser'@'localhost';
CREATE USER 'quizuser'@'localhost' IDENTIFIED BY 'quizpassword';
GRANT ALL PRIVILEGES ON quizdb.* TO 'quizuser'@'localhost';
FLUSH PRIVILEGES;

-- Tables

CREATE TABLE games (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    game_id INT NOT NULL,
    question_text TEXT NOT NULL,
    correct_option_index INT NOT NULL,
    FOREIGN KEY (game_id) REFERENCES games(id)
);

CREATE TABLE options (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT NOT NULL,
    option_index INT NOT NULL,
    option_text TEXT NOT NULL,
    FOREIGN KEY (question_id) REFERENCES questions(id)
);

-- Stored procedure

DROP PROCEDURE IF EXISTS sp_get_questions_by_game;

DELIMITER $$

CREATE PROCEDURE sp_get_questions_by_game(IN gameId INT)
BEGIN
    SELECT
        q.id AS question_id,
        q.question_text,
        q.correct_option_index,
        o.option_index,
        o.option_text
    FROM questions q
    JOIN options o ON q.id = o.question_id
    WHERE q.game_id = gameId
    ORDER BY q.id, o.option_index;
END$$

DELIMITER ;
