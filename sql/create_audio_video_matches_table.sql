CREATE TABLE `audio_video_matches` (
  `id` int NOT NULL AUTO_INCREMENT,
  `match_id` double DEFAULT NULL,
  `song_id` double DEFAULT NULL,
  `start` bigint DEFAULT NULL,
  `end` bigint DEFAULT NULL,
  `video_audio_match_id` varchar(12) DEFAULT NULL,
  `video_type` varchar(4) DEFAULT NULL,
  `video_id` bigint DEFAULT NULL,
  `invalid_mode` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_audio_video_matches_index` (`index`)
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
