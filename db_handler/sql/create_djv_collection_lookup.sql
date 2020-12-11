ALTER TABLE file_system_catalogs.midi_audio_matches
ADD COLUMN djv_song_id MEDIUMINT;

UPDATE file_system_catalogs.midi_audio_matches mam
join dejavu.songs s on LEFT(s.song_name, LOCATE('_', s.song_name)-1) = mam.pair_id
set mam.djv_song_id = s.song_id
where mam.djv_song_id IS NULL;