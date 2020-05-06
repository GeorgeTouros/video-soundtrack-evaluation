import os
import re
import pandas as pd


def create_catalog(directory, except_dir=None, except_file=None):
    """
    Takes a directory as an input, and outputs a pandas DF with a full catalog of files and locations
    :param directory: the directory you want to be cataloged
    :param except_dir: optional argument to exclude irrelevant directories. Accepts str or compiled RegEx
    :param except_file: optional argument to exclude irrelevant files. Accepts str or compiled RegEx
    :return: Pandas DF with the relevant catalog
    """
    dirs = []
    names = []
    for dirname, dirnames, filenames in os.walk(directory):
        # remove unwanted directories
        if except_dir:
            if except_dir in dirnames:
                dirnames.remove(except_dir)

        for filename in filenames:
            if except_file:
                if re.search(except_file, str(filename)):
                    filenames.remove(filename)
            else:
                dirs.append(dirname)
                names.append(filename)
    d = {'directory': dirs, 'filename': names}

    output = pd.DataFrame.from_dict(d)
    return output


if __name__ == '__main__':
    # Each midi file also has an indexing file that starts with .-
    # We remove those
    irrelevant_midi = re.compile('\._|\.DS_Store')
    irrelevant_dir = 'lmd_matched'
    midi_dir = 'data\\midis\\'

    midi_catalog = create_catalog(midi_dir, irrelevant_dir, irrelevant_midi)
    midi_catalog.to_csv('var\\midi_catalog.csv', index=False)

    # continue with the audio files
    audio_dir = 'data\\2020-03-22_21_25\\data\\downloads\\downloaded\\audio'
    audio_catalog = create_catalog(audio_dir)
    audio_catalog.to_csv('var\\audio_catalog.csv', index=False)

    #continue with the video files
    video_dir = 'data\\2020-03-22_21_25\\data\\downloads\\downloaded\\video'
    video_catalog = create_catalog(video_dir)
    video_catalog.to_csv('var\\video_catalog.csv', index=False)
