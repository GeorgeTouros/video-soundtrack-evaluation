import os
import re
import pandas as pd

# Each midi file also has an indexing file that starts with .-
# We remove those
irrelevant = re.compile('\._|\.DS_Store')

dirs = []
names = []

for dirname, dirnames, filenames in os.walk('data\\midis\\'):
    if 'lmd_matched' in dirnames:
        # don't go into any lmd directories, which is some hashed deduplication of the other datasets.
        dirnames.remove('lmd_matched')

    for filename in filenames:
        if re.search(irrelevant, str(filename)):
            filenames.remove(filename)
        else:
            dirs.append(dirname)
            names.append(filename)
            #print(os.path.join(dirname, filename))

d = {'directory':dirs, 'filename':names}

catalog = pd.DataFrame.from_dict(d)

catalog.to_csv('var\\midi_catalog.csv',index=False)