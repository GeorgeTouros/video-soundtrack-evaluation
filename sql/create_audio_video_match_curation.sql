CREATE TABLE `file_system_catalogs`.`audio_video_match_curation` (
  `audio_video_match_id` INT NOT NULL,
  `correct` INT NOT NULL,
  PRIMARY KEY (`audio_video_match_id`),
  UNIQUE INDEX `audio_video_match_id_UNIQUE` (`audio_video_match_id` ASC) VISIBLE,
  CONSTRAINT `fk_audio_video_match_curation_1`
    FOREIGN KEY (`audio_video_match_id`)
    REFERENCES `file_system_catalogs`.`audio_video_matches` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);