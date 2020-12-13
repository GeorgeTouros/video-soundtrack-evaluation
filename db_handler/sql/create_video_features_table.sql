CREATE TABLE `file_system_catalogs`.`video_features`
(
    `clip_id`                        INT        NOT NULL,
    `mean_hist_r0`                   DECIMAL(7, 5) NULL,
    `mean_hist_r1`                   DECIMAL(7, 5) NULL,
    `mean_hist_r2`                   DECIMAL(7, 5) NULL,
    `mean_hist_r3`                   DECIMAL(7, 5) NULL,
    `mean_hist_r4`                   DECIMAL(7, 5) NULL,
    `mean_hist_r5`                   DECIMAL(7, 5) NULL,
    `mean_hist_r6`                   DECIMAL(7, 5) NULL,
    `mean_hist_r7`                   DECIMAL(7, 5) NULL,
    `mean_hist_g0`                   DECIMAL(7, 5) NULL,
    `mean_hist_g1`                   DECIMAL(7, 5) NULL,
    `mean_hist_g2`                   DECIMAL(7, 5) NULL,
    `mean_hist_g3`                   DECIMAL(7, 5) NULL,
    `mean_hist_g4`                   DECIMAL(7, 5) NULL,
    `mean_hist_g5`                   DECIMAL(7, 5) NULL,
    `mean_hist_g6`                   DECIMAL(7, 5) NULL,
    `mean_hist_g7`                   DECIMAL(7, 5) NULL,
    `mean_hist_b0`                   DECIMAL(7, 5) NULL,
    `mean_hist_b1`                   DECIMAL(7, 5) NULL,
    `mean_hist_b2`                   DECIMAL(7, 5) NULL,
    `mean_hist_b3`                   DECIMAL(7, 5) NULL,
    `mean_hist_b4`                   DECIMAL(7, 5) NULL,
    `mean_hist_b5`                   DECIMAL(7, 5) NULL,
    `mean_hist_b6`                   DECIMAL(7, 5) NULL,
    `mean_hist_b7`                   DECIMAL(7, 5) NULL,
    `mean_hist_v0`                   DECIMAL(7, 5) NULL,
    `mean_hist_v1`                   DECIMAL(7, 5) NULL,
    `mean_hist_v2`                   DECIMAL(7, 5) NULL,
    `mean_hist_v3`                   DECIMAL(7, 5) NULL,
    `mean_hist_v4`                   DECIMAL(7, 5) NULL,
    `mean_hist_v5`                   DECIMAL(7, 5) NULL,
    `mean_hist_v6`                   DECIMAL(7, 5) NULL,
    `mean_hist_v7`                   DECIMAL(7, 5) NULL,
    `mean_hist_rgb0`                 DECIMAL(7, 5) NULL,
    `mean_hist_rgb1`                 DECIMAL(7, 5) NULL,
    `mean_hist_rgb2`                 DECIMAL(7, 5) NULL,
    `mean_hist_rgb3`                 DECIMAL(7, 5) NULL,
    `mean_hist_rgb4`                 DECIMAL(7, 5) NULL,
    `mean_hist_s0`                   DECIMAL(7, 5) NULL,
    `mean_hist_s1`                   DECIMAL(7, 5) NULL,
    `mean_hist_s2`                   DECIMAL(7, 5) NULL,
    `mean_hist_s3`                   DECIMAL(7, 5) NULL,
    `mean_hist_s4`                   DECIMAL(7, 5) NULL,
    `mean_hist_s5`                   DECIMAL(7, 5) NULL,
    `mean_hist_s6`                   DECIMAL(7, 5) NULL,
    `mean_hist_s7`                   DECIMAL(7, 5) NULL,
    `mean_frame_value_diff`          DECIMAL(7, 5) NULL,
    `mean_frontal_faces_num`         DECIMAL(7, 5) NULL,
    `mean_fronatl_faces_ratio`       DECIMAL(7, 5) NULL,
    `mean_tilt_pan_confidences`      DECIMAL(7, 5) NULL,
    `mean_mag_mean`                  DECIMAL(7, 5) NULL,
    `mean_mag_std`                   DECIMAL(7, 5) NULL,
    `mean_shot_durations`            DECIMAL(7, 5) NULL,
    `std_hist_r0`                    DECIMAL(7, 5) NULL,
    `std_hist_r1`                    DECIMAL(7, 5) NULL,
    `std_hist_r2`                    DECIMAL(7, 5) NULL,
    `std_hist_r3`                    DECIMAL(7, 5) NULL,
    `std_hist_r4`                    DECIMAL(7, 5) NULL,
    `std_hist_r5`                    DECIMAL(7, 5) NULL,
    `std_hist_r6`                    DECIMAL(7, 5) NULL,
    `std_hist_r7`                    DECIMAL(7, 5) NULL,
    `std_hist_g0`                    DECIMAL(7, 5) NULL,
    `std_hist_g1`                    DECIMAL(7, 5) NULL,
    `std_hist_g2`                    DECIMAL(7, 5) NULL,
    `std_hist_g3`                    DECIMAL(7, 5) NULL,
    `std_hist_g4`                    DECIMAL(7, 5) NULL,
    `std_hist_g5`                    DECIMAL(7, 5) NULL,
    `std_hist_g6`                    DECIMAL(7, 5) NULL,
    `std_hist_g7`                    DECIMAL(7, 5) NULL,
    `std_hist_b0`                    DECIMAL(7, 5) NULL,
    `std_hist_b1`                    DECIMAL(7, 5) NULL,
    `std_hist_b2`                    DECIMAL(7, 5) NULL,
    `std_hist_b3`                    DECIMAL(7, 5) NULL,
    `std_hist_b4`                    DECIMAL(7, 5) NULL,
    `std_hist_b5`                    DECIMAL(7, 5) NULL,
    `std_hist_b6`                    DECIMAL(7, 5) NULL,
    `std_hist_b7`                    DECIMAL(7, 5) NULL,
    `std_hist_v0`                    DECIMAL(7, 5) NULL,
    `std_hist_v1`                    DECIMAL(7, 5) NULL,
    `std_hist_v2`                    DECIMAL(7, 5) NULL,
    `std_hist_v3`                    DECIMAL(7, 5) NULL,
    `std_hist_v4`                    DECIMAL(7, 5) NULL,
    `std_hist_v5`                    DECIMAL(7, 5) NULL,
    `std_hist_v6`                    DECIMAL(7, 5) NULL,
    `std_hist_v7`                    DECIMAL(7, 5) NULL,
    `std_hist_rgb0`                  DECIMAL(7, 5) NULL,
    `std_hist_rgb1`                  DECIMAL(7, 5) NULL,
    `std_hist_rgb2`                  DECIMAL(7, 5) NULL,
    `std_hist_rgb3`                  DECIMAL(7, 5) NULL,
    `std_hist_rgb4`                  DECIMAL(7, 5) NULL,
    `std_hist_s0`                    DECIMAL(7, 5) NULL,
    `std_hist_s1`                    DECIMAL(7, 5) NULL,
    `std_hist_s2`                    DECIMAL(7, 5) NULL,
    `std_hist_s3`                    DECIMAL(7, 5) NULL,
    `std_hist_s4`                    DECIMAL(7, 5) NULL,
    `std_hist_s5`                    DECIMAL(7, 5) NULL,
    `std_hist_s6`                    DECIMAL(7, 5) NULL,
    `std_hist_s7`                    DECIMAL(7, 5) NULL,
    `std_frame_value_diff`           DECIMAL(7, 5) NULL,
    `std_frontal_faces_num`          DECIMAL(7, 5) NULL,
    `std_fronatl_faces_ratio`        DECIMAL(7, 5) NULL,
    `std_tilt_pan_confidences`       DECIMAL(7, 5) NULL,
    `std_mag_mean`                   DECIMAL(7, 5) NULL,
    `std_mag_std`                    DECIMAL(7, 5) NULL,
    `std_shot_durations`             DECIMAL(7, 5) NULL,
    `stdmean_hist_r0`                DECIMAL(7, 5) NULL,
    `stdmean_hist_r1`                DECIMAL(7, 5) NULL,
    `stdmean_hist_r2`                DECIMAL(7, 5) NULL,
    `stdmean_hist_r3`                DECIMAL(7, 5) NULL,
    `stdmean_hist_r4`                DECIMAL(7, 5) NULL,
    `stdmean_hist_r5`                DECIMAL(7, 5) NULL,
    `stdmean_hist_r6`                DECIMAL(7, 5) NULL,
    `stdmean_hist_r7`                DECIMAL(7, 5) NULL,
    `stdmean_hist_g0`                DECIMAL(7, 5) NULL,
    `stdmean_hist_g1`                DECIMAL(7, 5) NULL,
    `stdmean_hist_g2`                DECIMAL(7, 5) NULL,
    `stdmean_hist_g3`                DECIMAL(7, 5) NULL,
    `stdmean_hist_g4`                DECIMAL(7, 5) NULL,
    `stdmean_hist_g5`                DECIMAL(7, 5) NULL,
    `stdmean_hist_g6`                DECIMAL(7, 5) NULL,
    `stdmean_hist_g7`                DECIMAL(7, 5) NULL,
    `stdmean_hist_b0`                DECIMAL(7, 5) NULL,
    `stdmean_hist_b1`                DECIMAL(7, 5) NULL,
    `stdmean_hist_b2`                DECIMAL(7, 5) NULL,
    `stdmean_hist_b3`                DECIMAL(7, 5) NULL,
    `stdmean_hist_b4`                DECIMAL(7, 5) NULL,
    `stdmean_hist_b5`                DECIMAL(7, 5) NULL,
    `stdmean_hist_b6`                DECIMAL(7, 5) NULL,
    `stdmean_hist_b7`                DECIMAL(7, 5) NULL,
    `stdmean_hist_v0`                DECIMAL(7, 5) NULL,
    `stdmean_hist_v1`                DECIMAL(7, 5) NULL,
    `stdmean_hist_v2`                DECIMAL(7, 5) NULL,
    `stdmean_hist_v3`                DECIMAL(7, 5) NULL,
    `stdmean_hist_v4`                DECIMAL(7, 5) NULL,
    `stdmean_hist_v5`                DECIMAL(7, 5) NULL,
    `stdmean_hist_v6`                DECIMAL(7, 5) NULL,
    `stdmean_hist_v7`                DECIMAL(7, 5) NULL,
    `stdmean_hist_rgb0`              DECIMAL(7, 5) NULL,
    `stdmean_hist_rgb1`              DECIMAL(7, 5) NULL,
    `stdmean_hist_rgb2`              DECIMAL(7, 5) NULL,
    `stdmean_hist_rgb3`              DECIMAL(7, 5) NULL,
    `stdmean_hist_rgb4`              DECIMAL(7, 5) NULL,
    `stdmean_hist_s0`                DECIMAL(7, 5) NULL,
    `stdmean_hist_s1`                DECIMAL(7, 5) NULL,
    `stdmean_hist_s2`                DECIMAL(7, 5) NULL,
    `stdmean_hist_s3`                DECIMAL(7, 5) NULL,
    `stdmean_hist_s4`                DECIMAL(7, 5) NULL,
    `stdmean_hist_s5`                DECIMAL(7, 5) NULL,
    `stdmean_hist_s6`                DECIMAL(7, 5) NULL,
    `stdmean_hist_s7`                DECIMAL(7, 5) NULL,
    `stdmean_frame_value_diff`       DECIMAL(7, 5) NULL,
    `stdmean_frontal_faces_num`      DECIMAL(9, 5) NULL,
    `stdmean_fronatl_faces_ratio`    DECIMAL(9, 5) NULL,
    `stdmean_tilt_pan_confidences`   DECIMAL(7, 5) NULL,
    `stdmean_mag_mean`               DECIMAL(7, 5) NULL,
    `stdmean_mag_std`                DECIMAL(7, 5) NULL,
    `stdmean_shot_durations`         DECIMAL(7, 5) NULL,
    `mean10top_hist_r0`              DECIMAL(7, 5) NULL,
    `mean10top_hist_r1`              DECIMAL(7, 5) NULL,
    `mean10top_hist_r2`              DECIMAL(7, 5) NULL,
    `mean10top_hist_r3`              DECIMAL(7, 5) NULL,
    `mean10top_hist_r4`              DECIMAL(7, 5) NULL,
    `mean10top_hist_r5`              DECIMAL(7, 5) NULL,
    `mean10top_hist_r6`              DECIMAL(7, 5) NULL,
    `mean10top_hist_r7`              DECIMAL(7, 5) NULL,
    `mean10top_hist_g0`              DECIMAL(7, 5) NULL,
    `mean10top_hist_g1`              DECIMAL(7, 5) NULL,
    `mean10top_hist_g2`              DECIMAL(7, 5) NULL,
    `mean10top_hist_g3`              DECIMAL(7, 5) NULL,
    `mean10top_hist_g4`              DECIMAL(7, 5) NULL,
    `mean10top_hist_g5`              DECIMAL(7, 5) NULL,
    `mean10top_hist_g6`              DECIMAL(7, 5) NULL,
    `mean10top_hist_g7`              DECIMAL(7, 5) NULL,
    `mean10top_hist_b0`              DECIMAL(7, 5) NULL,
    `mean10top_hist_b1`              DECIMAL(7, 5) NULL,
    `mean10top_hist_b2`              DECIMAL(7, 5) NULL,
    `mean10top_hist_b3`              DECIMAL(7, 5) NULL,
    `mean10top_hist_b4`              DECIMAL(7, 5) NULL,
    `mean10top_hist_b5`              DECIMAL(7, 5) NULL,
    `mean10top_hist_b6`              DECIMAL(7, 5) NULL,
    `mean10top_hist_b7`              DECIMAL(7, 5) NULL,
    `mean10top_hist_v0`              DECIMAL(7, 5) NULL,
    `mean10top_hist_v1`              DECIMAL(7, 5) NULL,
    `mean10top_hist_v2`              DECIMAL(7, 5) NULL,
    `mean10top_hist_v3`              DECIMAL(7, 5) NULL,
    `mean10top_hist_v4`              DECIMAL(7, 5) NULL,
    `mean10top_hist_v5`              DECIMAL(7, 5) NULL,
    `mean10top_hist_v6`              DECIMAL(7, 5) NULL,
    `mean10top_hist_v7`              DECIMAL(7, 5) NULL,
    `mean10top_hist_rgb0`            DECIMAL(7, 5) NULL,
    `mean10top_hist_rgb1`            DECIMAL(7, 5) NULL,
    `mean10top_hist_rgb2`            DECIMAL(7, 5) NULL,
    `mean10top_hist_rgb3`            DECIMAL(7, 5) NULL,
    `mean10top_hist_rgb4`            DECIMAL(7, 5) NULL,
    `mean10top_hist_s0`              DECIMAL(7, 5) NULL,
    `mean10top_hist_s1`              DECIMAL(7, 5) NULL,
    `mean10top_hist_s2`              DECIMAL(7, 5) NULL,
    `mean10top_hist_s3`              DECIMAL(7, 5) NULL,
    `mean10top_hist_s4`              DECIMAL(7, 5) NULL,
    `mean10top_hist_s5`              DECIMAL(7, 5) NULL,
    `mean10top_hist_s6`              DECIMAL(7, 5) NULL,
    `mean10top_hist_s7`              DECIMAL(7, 5) NULL,
    `mean10top_frame_value_diff`     DECIMAL(7, 5) NULL,
    `mean10top_frontal_faces_num`    DECIMAL(7, 5) NULL,
    `mean10top_fronatl_faces_ratio`  DECIMAL(7, 5) NULL,
    `mean10top_tilt_pan_confidences` DECIMAL(7, 5) NULL,
    `mean10top_mag_mean`             DECIMAL(7, 5) NULL,
    `mean10top_mag_std`              DECIMAL(7, 5) NULL,
    `mean10top_shot_durations`       DECIMAL(7, 5) NULL,
    `person_freq`                    DECIMAL(7, 5) NULL,
    `vehicle_freq`                   DECIMAL(7, 5) NULL,
    `outdoor_freq`                   DECIMAL(7, 5) NULL,
    `animal_freq`                    DECIMAL(7, 5) NULL,
    `accessory_freq`                 DECIMAL(7, 5) NULL,
    `sports_freq`                    DECIMAL(7, 5) NULL,
    `kitchen_freq`                   DECIMAL(7, 5) NULL,
    `food_freq`                      DECIMAL(7, 5) NULL,
    `furniture_freq`                 DECIMAL(7, 5) NULL,
    `electronic_freq`                DECIMAL(7, 5) NULL,
    `appliance_freq`                 DECIMAL(7, 5) NULL,
    `indoor_freq`                    DECIMAL(7, 5) NULL,
    `person_mean_confidence`         DECIMAL(7, 5) NULL,
    `vehicle_mean_confidence`        DECIMAL(7, 5) NULL,
    `outdoor_mean_confidence`        DECIMAL(7, 5) NULL,
    `animal_mean_confidence`         DECIMAL(7, 5) NULL,
    `accessory_mean_confidence`      DECIMAL(7, 5) NULL,
    `sports_mean_confidence`         DECIMAL(7, 5) NULL,
    `kitchen_mean_confidence`        DECIMAL(7, 5) NULL,
    `food_mean_confidence`           DECIMAL(7, 5) NULL,
    `furniture_mean_confidence`      DECIMAL(7, 5) NULL,
    `electronic_mean_confidence`     DECIMAL(7, 5) NULL,
    `appliance_mean_confidence`      DECIMAL(7, 5) NULL,
    `indoor_mean_confidence`         DECIMAL(7, 5) NULL,
    `person_mean_area_ratio`         DECIMAL(7, 5) NULL,
    `vehicle_mean_area_ratio`        DECIMAL(7, 5) NULL,
    `outdoor_mean_area_ratio`        DECIMAL(7, 5) NULL,
    `animal_mean_area_ratio`         DECIMAL(7, 5) NULL,
    `accessory_mean_area_ratio`      DECIMAL(7, 5) NULL,
    `sports_mean_area_ratio`         DECIMAL(7, 5) NULL,
    `kitchen_mean_area_ratio`        DECIMAL(7, 5) NULL,
    `food_mean_area_ratio`           DECIMAL(7, 5) NULL,
    `furniture_mean_area_ratio`      DECIMAL(7, 5) NULL,
    `electronic_mean_area_ratio`     DECIMAL(7, 5) NULL,
    `appliance_mean_area_ratio`      DECIMAL(7, 5) NULL,
    `indoor_mean_area_ratio`         DECIMAL(7, 5) NULL,
    PRIMARY KEY (`clip_id`),
    UNIQUE INDEX `video_id_UNIQUE` (`clip_id` ASC) VISIBLE,
    CONSTRAINT `fk_video_features_1`
        FOREIGN KEY (`clip_id`)
            REFERENCES `file_system_catalogs`.`video_clip_catalog` (`id`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
);