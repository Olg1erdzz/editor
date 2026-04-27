CREATE DATABASE IF NOT EXISTS `editer_database`
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE `editer_database`;

CREATE TABLE IF NOT EXISTS `users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(100) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `role` VARCHAR(100) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `image` LONGTEXT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_users_username` (`username`),
  UNIQUE KEY `uk_users_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `chat` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(100) NOT NULL,
  `chat_number` INT NOT NULL DEFAULT 0,
  `chat_memory` LONGTEXT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_chat_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `documents` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `file_path` VARCHAR(512) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `type` VARCHAR(100) NOT NULL,
  `last_modified_time` DATETIME NOT NULL,
  `size` VARCHAR(50) DEFAULT NULL,
  `star` VARCHAR(10) NOT NULL DEFAULT 'false',
  PRIMARY KEY (`id`),
  KEY `idx_documents_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `stencil` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(100) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `path` VARCHAR(512) NOT NULL,
  `description` TEXT,
  `label` VARCHAR(255) DEFAULT NULL,
  `create_time` DATETIME NOT NULL,
  `update_time` DATETIME NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `videos` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NOT NULL,
  `description` TEXT,
  `video_addr` VARCHAR(512) NOT NULL,
  `label` VARCHAR(255) DEFAULT NULL,
  `username` VARCHAR(100) NOT NULL,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `collaborations` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `share_code` VARCHAR(255) NOT NULL,
  `usernames` LONGTEXT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_collaborations_share_code` (`share_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `picture` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(100) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `path` VARCHAR(512) NOT NULL,
  `file_name` VARCHAR(255) NOT NULL,
  `text` LONGTEXT,
  `time` DATETIME NOT NULL,
  `star` VARCHAR(10) NOT NULL DEFAULT 'false',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `audio` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(100) NOT NULL,
  `file_name` VARCHAR(255) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `path` VARCHAR(512) NOT NULL,
  `text` LONGTEXT,
  `time` DATETIME NOT NULL,
  `star` VARCHAR(10) NOT NULL DEFAULT 'false',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `knowledge` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `file_path` VARCHAR(512) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `create_time` DATETIME NOT NULL,
  `star` VARCHAR(10) NOT NULL DEFAULT 'false',
  PRIMARY KEY (`id`),
  KEY `idx_knowledge_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
