#!/usr/bin/env python3

from urllib.request import urlopen
from bs4 import BeautifulSoup as BS
import time
import json

INDEX = 'http://thejadednetwork.com/sfx/index/'

def bs(url):
    return BS(urlopen(url).read().decode(), 'html5lib')

def text(el):
    return [l.strip() for l in el.find_all(text=True)]

def definitions(tbl):
    return [
        dict(
            japanese=text(r[0]),
            romaji=text(r[1]),
            english=text(r[2]),
            explanation=text(r[3]),
        )
        for r in [_r.find_all('td') for _r in tbl.find_all('tr')]
        if not 'title' in r[0]['class']
    ]

def main():

    soup = bs(INDEX)
    kana = [
        td.a['href']
        for td in soup.find('table', class_='hiraganaMenuTable').find_all('td')
        if td.a
    ]

    translations = []

    for i, k in enumerate(kana):
        print('kana no. {}'.format(i))
        time.sleep(5)

        soup = bs(k)
        pagecount = soup.find('div', class_='pagin')

        # first page
        t = soup.find('table', class_='definitions')
        d = definitions(t)
        print(d)
        translations += d

        # rest of the pages
        if pagecount:
            # [< Prev] [1] [2] [3] ... [this one-->10] [Next >]
            for i in range(2, int(pagecount.find_all('a')[-2].text) + 1):
                time.sleep(5)
                soup = bs(k + str(i))
                t = soup.find('table', class_='definitions')
                d = definitions(t)
                print(d)
                translations += d

    with open('translations.json', 'w') as f:
        f.write(json.dumps(translations))

if __name__ == '__main__':
    main()
