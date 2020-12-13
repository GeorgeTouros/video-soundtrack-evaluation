create table file_system_catalogs.midi_catalog
(
	id bigint not null,
	directory text null,
	filename text null,
	title text null,
	spotify_name text null,
	spotify_artist text null,
	spotify_URL text null,
	constraint ix_midi_catalog_index
		unique (id)
);

alter table file_system_catalogs.midi_catalog
	add primary key (id);

