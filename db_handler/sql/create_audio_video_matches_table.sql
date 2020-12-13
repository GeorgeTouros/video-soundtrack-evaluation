CREATE TABLE `audio_video_matches` (
  `id` int NOT NULL AUTO_INCREMENT,
  `djv_song_id` mediumint DEFAULT NULL,
  `invalid_mode` int DEFAULT NULL,
  `real` int DEFAULT NULL,
  `clip_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_audio_video_matches_index` (`id`)
);
