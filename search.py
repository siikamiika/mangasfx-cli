#!/usr/bin/env python3

import json
import sys

def print_result(res):

    expl = []

    for r in res['explanation']:
        if len(r) > 40:
            buf = []
            for w in r.split():
                if len(' '.join(buf) + w) < 40:
                    buf.append(w)
                else:
                    expl.append(' '.join(buf))
                    buf = [w]
            if buf:
                expl.append(' '.join(buf))
        elif not r or '»' in r:
            continue
        else:
            expl.append(r)

    res['explanation'] = expl

    height = max(
        len(res['romaji']),
        len(res['english']),
        len(res['explanation']),
        )

    def w(a):
        return max(len(r) for r in res[a])

    widths = {
        'romaji': w('romaji'),
        'english': w('english'),
        'explanation': w('explanation'),
    }

    def safe_idx(r, i):
        if len(r) > i:
            return r[i]
        return ''

    for i in range(height):
        print('{} | {} | {}'.format(
            *[safe_idx(res[a], i).ljust(widths[a])
                for a in ['romaji', 'english', 'explanation']]
        ))


def search(translations, query):

    search_mode = 'romaji'

    if 0x30a0 <= ord(query[0]) <= 0x30ff:
        search_mode = 0

    elif 0x3040 <= ord(query[0]) <= 0x309f:
        search_mode = 1

    results = []

    for t in translations:
        if search_mode == 'romaji':
            if t['romaji'][0].replace(' ', '').startswith(query.replace(' ', '')):
                results.append(t)
        else:
            if t['japanese'][search_mode].startswith(query):
                results.append(t)

    results = sorted(results, key=lambda r: r['japanese'][0].replace(',', ''))

    if len(results) == 1:
        if search_mode == 'romaji':
            print(results[0]['japanese'][0].replace(',', ''))
        print_result(results[0])

    elif len(results) > 1:
        if search_mode == 'romaji':
            search_mode = 0

        info = []
        for i, r in enumerate(results):
            info.append('{}: {}'.format(i, r['japanese'][search_mode].replace(',', '')))

        idx = input('\n'.join(info) + '\n')
        try:
            idx = int(idx)
        except ValueError:
            idx = 0

        print_result(results[idx])

    else:
        print('No results')


def main():

    with open('translations.json') as f:
        translations = json.loads(f.read())

    print('Searching from {} translations'.format(len(translations)))

    query = ' '.join(sys.argv[1:])

    if query:
        search(translations, query)

    else:
        while True:
            search(translations, input('\n'))


if __name__ == '__main__':
    main()