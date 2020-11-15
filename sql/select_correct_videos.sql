SELECT
    vm.id, vm.video_audio_match_id, vm.start, vm.end,vm.video_type, s.song_name, vc.title
FROM
    file_system_catalogs.audio_video_matches vm
       LEFT JOIN
    dejavu.songs s ON s.song_id = vm.song_id
       LEFT JOIN
	file_system_catalogs.video_catalog vc ON vc.id = vm.video_id
	   LEFT JOIN
	file_system_catalogs.audio_video_match_curation cur on cur.audio_video_match_id = vm.id
where cur.correct = 1
;