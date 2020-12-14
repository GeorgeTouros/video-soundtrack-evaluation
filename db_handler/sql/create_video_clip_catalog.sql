CREATE TABLE `file_system_catalogs`.`video_clip_catalog` (
  `id` int NOT NULL AUTO_INCREMENT,
  `video_id` bigint DEFAULT NULL,
  `start` bigint DEFAULT NULL,
  `end` bigint DEFAULT NULL,
  `video_type` varchar(4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `clip_id_UNIQUE` (`id` ASC) VISIBLE,
    CONSTRAINT `fk_video_clip_1`
        FOREIGN KEY (`video_id`)
            REFERENCES `file_system_catalogs`.`video_catalog` (id)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
);
