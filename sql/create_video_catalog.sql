CREATE TABLE `video_catalog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `directory` text,
  `filename` text,
  `title` text,
  `file_type` text,
  `full_path` text,
  `searched` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `ix_video_catalog_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=152 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
