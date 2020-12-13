SELECT
    vm.id,
    vcc.id as clip_id,
    mam.index_audio as audio_id,
    mam.index_midi as midi_id,
    vcc.video_id,
    vcc.start,
    vcc.end,
    vcc.video_type,
    RIGHT(ac.filename,3) as audio_type,
    RIGHT(mc.filename,3) as midi_type,
    CONCAT(ac.directory, '/', ac.filename) as audio_file_path,
    CONCAT(mc.directory, '/', mc.filename) as midi_file_path,
    CONCAT(vc.directory, '/', vc.filename) as video_file_path,
    vm.real
FROM
    file_system_catalogs.audio_video_matches vm
        LEFT JOIN
    file_system_catalogs.video_clip_catalog vcc
        on vcc.id = vm.clip_id
        LEFT JOIN
    file_system_catalogs.midi_audio_matches mam on mam.djv_song_id = vm.djv_song_id
        LEFT JOIN
    file_system_catalogs.audio_catalog ac on ac.id = mam.index_audio
        LEFT JOIN
    file_system_catalogs.midi_catalog mc on mc.id = mam.index_midi
       LEFT JOIN
	file_system_catalogs.video_catalog vc ON vc.id = vcc.video_id
	   LEFT JOIN
	file_system_catalogs.audio_video_match_curation cur on cur.audio_video_match_id = vm.id
where cur.correct = 1 or vm.real=0
order by vm.djv_song_id
;