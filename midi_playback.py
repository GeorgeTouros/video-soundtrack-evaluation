from mido import MidiFile
import re

# set up regex for song name and artist
title_re = re.compile("<meta message track_name name=\'(.*)\'")
artist_re = re.compile("<meta message text text='Performed by:  (.*)\(|\'")

directory = 'D:\Data Science\\thesis_dataset_creation\\data\\midis\\Big_Data_Set\\0\\'
file = '070107 (Music of the Third Kind).MID'


mid = MidiFile(str(directory+file), clip=True)

# There are three types of MIDI files:
#
# type 0 (single track): all messages are saved in one track
# type 1 (synchronous): all tracks start at the same time
# type 2 (asynchronous): each track is independent of the others

# print(mid)


# This allows you to see the track titles and how many messages are in each track.
#for track in mid.tracks:
#    print(track)

# This particular track contains only meta information about the MIDI file in general
# such as the tempo and time signature
for msg in mid.tracks[1]:
    title_search = re.search(title_re, str(msg))
    if title_search:
        title = title_search.group(1)
        print(title)

    artist_search = re.search(artist_re, str(msg))
    if artist_search:
        artist = artist_search.group(1)
        if artist:
            print(artist)
    print(msg)


