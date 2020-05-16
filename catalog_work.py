import os
import re
import pandas as pd


def create_catalog(directory, except_dir='', except_file=''):
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
        if except_dir in dirnames:
            dirnames.remove(except_dir)

        for filename in filenames:
            if re.search(except_file, str(filename)):
                filenames.remove(filename)
            else:
                dirs.append(dirname)
                names.append(filename)
    d = {'directory': dirs, 'filename': names}

    output = pd.DataFrame.from_dict(d)
    return output


def identify_ennio_names(cat):
    """
    adds an extra column to the catalog df with the clean title and the id.
    :param cat: the catalog dataframe
    :return: the clean df
    """
    patterns = re.compile('title_(.*)-id_(.*?)(-.*|$)')
    titles = []
    ids = []
    for filename in cat['filename']:
        search = re.search(patterns, str(filename))
        if search:
            title = search.group(1)
            db_id = search.group(2)
            titles.append(title)
            ids.append(db_id)
        else:
            titles.append(' ')
            ids.append(' ')
    cat['title'] = titles
    cat['id'] = ids
    return cat

def merge_ennio_audio_video_catalogs(audio_df, video_df):
    """
    takes the ennio catalogues and only keeps the files that exist in both
    :param audio_df: a pandas dataframe
    :param video_df: another pandas dataframe
    :return: joined dataframe
    """
    audio_df.set_index(keys='title', inplace=True)
    video_df.set_index(keys='title', inplace=True)

    merged = audio_df.merge(right=video_df,
                            left_index=True,
                            right_index=True,
                            how='inner',
                            suffixes=('_audio', '_video'))
    merged.reset_index(inplace=True)
    return merged


if __name__ == '__main__':
    # Each midi file also has an indexing file that starts with .-
    # We remove those
    irrelevant_midi = re.compile('\._|\.DS_Store')
    irrelevant_dir = 'lmd_matched'
    # we also remove the windows hidden files
    irrelevant_index_file = re.compile('desktop.ini')

    # start with the midi files
    print('start midi catalog')
    midi_dir = 'data\\midis\\'
    midi_catalog = create_catalog(midi_dir, irrelevant_dir, irrelevant_midi)
    print('finish midi catalog')

    # continue with the audio files
    print('start audio catalog')
    audio_dir = 'data\\2020-03-22_21_25\\data\\downloads\\downloaded\\audio'
    audio_catalog = create_catalog(audio_dir, except_file=irrelevant_index_file)
    audio_catalog = identify_ennio_names(audio_catalog)
    audio_catalog.to_csv('var\\audio_catalog.csv', index=False)
    print('finish audio catalog')

    # continue with the video files
    print('start video catalog')
    video_dir = 'data\\2020-03-22_21_25\\data\\downloads\\downloaded\\video'
    video_catalog = create_catalog(video_dir, except_file=irrelevant_index_file)
    video_catalog = identify_ennio_names(video_catalog)
    video_catalog.to_csv('var\\video_catalog.csv', index=False)
    print('finish video catalog')
    print('cleanup audio_video')
    merge = merge_ennio_audio_video_catalogs(audio_catalog, video_catalog)

    print('dumping all to csv')

    merge.to_csv('var\\ennio_catalog.csv', index=False)
    midi_catalog.to_csv('var\\midi_catalog.csv', index=False)

