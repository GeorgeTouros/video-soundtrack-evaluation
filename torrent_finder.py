import re, requests, os, time, errno, json
from bs4 import BeautifulSoup
import pandas as pd
from common import qbit_instance, chunker

qb = qbit_instance()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
}

wishlist = pd.read_csv(r'var\film_list.csv', header=None)


group_no = 0
for group in chunker(wishlist[0], 20):
    dir_catalog = {}
    path = r"data\films\batch"+str(group_no)
    try:
        os.umask(0o777)
        os.makedirs(path, mode=0o777)
        os.chmod(path, 0o777)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        else:
            pass
    else:
        print("Successfully created the directory %s " % path)

        for movie in group:
            q_movie = str(movie + ' film').replace(' ', '+')
            r = requests.get('https://tpb.party/search/{m}?q={m}'.format(m=q_movie), headers=headers)
            soup = BeautifulSoup(r.text, 'lxml')
            try:
                magnet_link = [x['href'] for x in soup.findAll('a', href=True) if 'magnet' in x['href']][0]
                print('Getting film ' + str(movie))
                qb.download_from_link(str(magnet_link), savepath=path)

                dir_catalog[movie] = {'path': path, 'magnet': magnet_link}
            except:
                print('Failed to find magnet for ' + movie)

        # update the film catalog file
        with open(r'var\film_directory.json', 'a+') as f:
            try:
                data = json.load(f)
                data.append(dir_catalog)
                json.dump(data, f)
            except json.decoder.JSONDecodeError:
                json.dump(dir_catalog, f)

        downloading = qb.torrents(filter='downloading')
        while len(downloading) > 5:
            time.sleep(5)
            downloading = qb.torrents(filter='downloading')
        # cleanup
        completed = qb.torrents(filter='completed')
        for tor in completed:
            qb.delete(tor['hash'])
    group_no += 1


