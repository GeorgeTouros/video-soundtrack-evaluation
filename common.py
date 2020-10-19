from credentials import webui
from datetime import datetime
from qbittorrent import Client
import os.path
import time
import csv
from collections import Counter



def wait_for_file(file_path):
    while not os.path.exists(file_path):
        time.sleep(1)


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


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
            if len(token) < 4:
                all_tokens.append(token)
    vocabulary.update(all_tokens)
    stopwords = vocabulary.most_common(n=n)
    return stopwords


CHUNK_SIZE = 30 * 1000  # ms
SAMPLE_RATE = 32000
CHANNELS = 1
BATCH_SIZE = 100
