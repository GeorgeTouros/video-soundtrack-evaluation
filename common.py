from credentials import webui
import re
from datetime import datetime
from qbittorrent import Client
import os.path
import time
import csv
from collections import Counter

FILENAME_STOPWORDS = ['bdrip', 'brrip', '1080p', '720p', 'aac'
                      'www', 'yifi', 'yts','anoxmous', 'bluray', 'hdtv'
                      'webrip', 'criterion', 'dvdrip', 'x264', 'xvid', 'gaz'
                      'dm', 'kar', 'karaoke', 'version', 'jpp',
                      'mix', 'remix', 'dj', 'nr', 'song', 'k'
                      ]


def wait_for_file(file_path):
    while not os.path.exists(file_path):
        time.sleep(1)


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


def reg_cleaner(string, allow_numbers=True):
    """
    simple function to convert string to lowercase and remove special characters
    :param allow_numbers: specify if you want to allow numbers or not (default yes)
    :param string: the string you want to clean
    :return: the clean string
    """
    if allow_numbers:
        remove_special = re.sub('[^A-Za-z0-9]+', ' ', string)
    else:
        remove_special = re.sub('[^A-Za-z]+', ' ', string)

    pascalcase = re.sub(r'([a-z](?=[A-Z])|[A-Z](?=[A-Z][a-z]))', r'\1 ', remove_special)

    clean_string = pascalcase.lower()

    stop = ''
    for stopword in FILENAME_STOPWORDS:
        stop += str(stopword) + '|'
    stop = stop[0:-1]

    stopword_re = re.compile('(\s+)'+stop+'(\s+|$)')

    remove_stopwords = stopword_re.sub('', clean_string)

    return remove_stopwords


def script_start_time():
    start_time = datetime.now()
    print('Script started running at: ' + str(start_time))


def script_run_time():
    end_time = datetime.now()
    print('Script ended at:' + str(end_time))


def qbit_instance():
    qb = Client(webui['IP'])

    qb.login(webui['username'], webui['pass'])
    return qb


def append_to_csv(csv_file, data, create=False):
    if create:
        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(data)
    if not create:
        with open(csv_file, 'a+', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(data)


def stopword_finder(string_list, n):
    """
    helps identify stop words from a list of strings
    :param string_list: the list of strings to be searched
    :param n: the number of potential stopwords to be returned
    :return: dictionary of potential stopwords with words as keys and frequencies as values.
    """
    vocabulary = Counter()
    all_tokens = []
    for string in string_list:
        tokens = string.split()
        for token in tokens:
            if len(token) < 5:
                all_tokens.append(token)
    vocabulary.update(all_tokens)
    stopwords = vocabulary.most_common(n=n)
    return stopwords
