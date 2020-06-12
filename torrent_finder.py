import requests, os, time
from bs4 import BeautifulSoup
import pandas as pd
from common import qbit_instance, chunker, append_to_csv

qb = qbit_instance()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
}

wishlist = pd.read_csv(r'var\film_list.csv', header=None)

if not os.path.exists(r'var\available_films.csv'):
    append_to_csv(csv_file=r'var\available_films.csv',
                  data =['movie', 'magnet_link', 'filename'],
                  create=True)

group_no = 1
for group in chunker(wishlist[0], 20):
    print("Starting work on batch %s " % group_no)
    for movie in group:
        # check if you already have a film
        available_films = pd.read_csv(r'var\available_films.csv', header=0)
        if movie in available_films['movie'].values:
            print(movie + ' already in db')
            pass
        else:
            q_movie = movie.replace(' ', '+')
            r = requests.get('https://tpb.party/search/{m}?q={m}'.format(m=q_movie), headers=headers)
            soup = BeautifulSoup(r.text, 'lxml')
            try:
                magnet_link = [x['href'] for x in soup.findAll('a', href=True) if 'magnet' in x['href']][0]
                print('Getting film ' + str(movie))
                qb.download_from_link(str(magnet_link))
                file_name = qb.torrents(filter='downloading', sort='added_on', limit=1, reverse=True)[0]['name']
                # update the film catalog file
                append_to_csv(r'var\available_films.csv', [movie, magnet_link, file_name], create=False)
            except:
                print('Failed to find magnet for ' + movie)

    downloading = qb.torrents(filter='downloading')
    while len(downloading) > 10:
        time.sleep(5)
        downloading = qb.torrents(filter='downloading')
        # cleanup
        completed = qb.torrents(filter='completed')
        for tor in completed:
            qb.delete(tor['hash'])
    group_no += 1


