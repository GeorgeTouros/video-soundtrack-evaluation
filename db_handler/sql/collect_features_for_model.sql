SELECT
    vm.id,
    vcc.video_id,
    vm.real as y,
    af.*,
    sf.*,
    vf.*
FROM
    file_system_catalogs.audio_video_matches vm
        LEFT JOIN
    file_system_catalogs.video_clip_catalog vcc
        on vcc.id = vm.clip_id
        LEFT JOIN
    file_system_catalogs.midi_audio_matches mam on mam.djv_song_id = vm.djv_song_id
	   LEFT JOIN
	file_system_catalogs.audio_video_match_curation cur on cur.audio_video_match_id = vm.id
        LEFT JOIN
    file_system_catalogs.audio_features af on af.audio_id = mam.index_audio
        LEFT JOIN
    file_system_catalogs.symbolic_features sf on sf.midi_id = mam.index_midi
        LEFT JOIN
    file_system_catalogs.video_features vf on vf.clip_id = vcc.id
where (cur.correct = 1 or vm.real=0)
and vf.clip_id is not null
order by vm.djv_song_id