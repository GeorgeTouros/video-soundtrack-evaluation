SELECT
    vcc.id, vcc.start, vcc.end,vcc.video_type, s.song_name, vc.title, vc.directory, vc.filename
FROM
    file_system_catalogs.audio_video_matches vm
        LEFT JOIN
    file_system_catalogs.video_clip_catalog vcc
        on vm.clip_id = vcc.id
       LEFT JOIN
    dejavu.songs s ON s.song_id = vm.djv_song_id
       LEFT JOIN
	file_system_catalogs.video_catalog vc ON vc.id = vcc.video_id
	   LEFT JOIN
	file_system_catalogs.audio_video_match_curation cur on cur.audio_video_match_id = vm.id
where cur.correct = 1
;