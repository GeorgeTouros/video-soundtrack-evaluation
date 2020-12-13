create table file_system_catalogs.midi_audio_matches
(
	pair_id text null,
	index_midi bigint null,
	index_audio bigint null,
	djv_song_id mediumint null,
	constraint midi_audio_matches_audio_catalog_id_fk
		foreign key (index_audio) references file_system_catalogs.audio_catalog (id),
	constraint midi_audio_matches_midi_catalog_id_fk
		foreign key (index_midi) references file_system_catalogs.midi_catalog (id)
);

create index midi_audio_matches_djv_song_id_index
	on file_system_catalogs.midi_audio_matches (djv_song_id);

create index midi_audio_matches_index_audio_index
	on file_system_catalogs.midi_audio_matches (index_audio);

create index midi_audio_matches_index_midi_index
	on file_system_catalogs.midi_audio_matches (index_midi);

