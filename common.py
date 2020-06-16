from credentials import webui
import re
from datetime import datetime
from qbittorrent import Client
import os.path
import time
import csv


def wait_for_file(file_path):
    while not os.path.exists(file_path):
        time.sleep(1)


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


def reg_cleaner(string, numbers=True):
    """
    simple function to convert string to lowercase and remove special characters
    :param numbers: specify if you want to allow numbers or not (default yes)
    :param string: the string you want to clean
    :return: the clean string
    """
    if numbers:
        clean_string = re.sub('[^A-Za-z0-9]+', ' ', string).lower()
    else:
        clean_string = re.sub('[^A-Za-z]+', ' ', string).lower()
    return clean_string


def script_start_time():
    start_time = datetime.now()
    print('Script started running at: '+str(start_time))


def script_run_time():
    end_time = datetime.now()
    print('Script ended at:'+str(end_time))


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



