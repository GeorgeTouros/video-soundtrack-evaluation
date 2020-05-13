import pandas as pd
import re

df = pd.read_csv('var\\midi_catalog.csv')

suffix = re.compile('(.*)(\.mid|\.MID|\.Mid)')
titles = []

for filename in df['filename']:
    # remove suffix
    suf_search = re.search(suffix, filename)
    if suf_search:
        stripped = suf_search.group(1)
        words = stripped.replace('_',' ')
        titles.append(words)
    else:
        titles.append('')

df['titles'] = titles

print(df[df['titles']=='']['filename'])
