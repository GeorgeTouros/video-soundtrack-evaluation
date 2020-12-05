from mido import MidiFile
import mido
import re

# set up regex for song name and artist
title_re = re.compile("<meta message track_name name=\'(.*)\'")
artist_re = re.compile("<meta message text text='Performed by:  (.*)\(|\'")

file = './temp/test_dataset/0a2d626401e49eb46c59ec6dbd4f048fa305b001.mid'

mid = MidiFile(str(file), clip=True)

outs = mido.get_output_names()

port = mido.open_output(outs[1])

# for msg in mid.play():
#     port.send(msg)

# There are three types of MIDI files:
#
# type 0 (single track): all messages are saved in one track
# type 1 (synchronous): all tracks start at the same time
# type 2 (asynchronous): each track is independent of the others

# print(mid)


# This allows you to see the track titles and how many messages are in each track.
for track in mid.tracks:
    print(track)

# This particular track contains only meta information about the MIDI file in general
# such as the tempo and time signature
# for msg in mid.tracks[0]:
#     title_search = re.search(title_re, str(msg))
#     if title_search:
#         title = title_search.group(1)
#         print(title)
#
#     artist_search = re.search(artist_re, str(msg))
#     if artist_search:
#         artist = artist_search.group(1)
#         if artist:
#             print(artist)
#     print(msg)
