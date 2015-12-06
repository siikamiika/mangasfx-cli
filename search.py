#!/usr/bin/env python3

import json
import sys

def squeeze(lines, width=40):
    new = []

    for l in lines:
        if len(l) > width:
            buf = []
            for w in l.split():
                if len(' '.join(buf) + w) < width:
                    buf.append(w)
                else:
                    if buf:
                        new.append(' '.join(buf))
                    buf = [w]
            if buf:
                new.append(' '.join(buf))
        elif not l or '»' in l:
            continue
        else:
            new.append(l)

    return new


def print_result(res):

    jpn = res['japanese'][:2]
    romaji = res['romaji'][0]
    print(', '.join([kana.replace(',', '') for kana in jpn] + [romaji]))

    for attr in 'english', 'explanation':
        res[attr] = squeeze(res[attr])

    height = max(
        len(res['english']),
        len(res['explanation']),
        )

    def w(a):
        return max([len(r) for r in res[a]] + [0])

    widths = {
        'english': w('english'),
        'explanation': w('explanation'),
    }

    def safe_idx(r, i):
        if len(r) > i:
            return r[i]
        return ''

    for i in range(height):
        print('{} | {}'.format(*[
            safe_idx(res[a], i).ljust(widths[a])
            for a in ['english', 'explanation']
        ]))


def search(translations, query):

    if not query:
        return

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

    # result
    if len(results) == 1:
        print_result(results[0])

    elif len(results) > 1:
        if search_mode == 'romaji':
            search_mode = 0

        info = []

        for i, r in enumerate(results):
            info.append('{}: {}'.format(i, r['japanese'][search_mode].replace(',', '')))

        idx = input('\n'.join(info) + '\nIndex? [0]>')
        try:
            idx = int(idx)
        except ValueError:
            if not idx:
                idx = 0

        try:
            print_result(results[idx])
        except (IndexError, TypeError):
            print('Invalid index')

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
            search(translations, input('\n>'))


if __name__ == '__main__':
    main()
