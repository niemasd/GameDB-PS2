#! /usr/bin/env python3
'''
Scrape titles + serials from PlayStation DataCenter main pages
'''
from bs4 import BeautifulSoup
from datetime import datetime
from os import makedirs
from os.path import abspath, expanduser, isfile
from urllib.request import urlopen
from sys import argv

# PlayStation DataCenter PS2 main pages
URLS = {
    'NTSC-U': 'https://psxdatacenter.com/psx2/ulist2.html',
    'NTSC-J': 'https://psxdatacenter.com/psx2/jlist2.html',
    'PAL': 'https://psxdatacenter.com/psx2/plist2.html',
}

# language map (need to upper() the original ones first)
LANG = {
    'CZ': 'Czech',
    'D':  'Danish',
    'DU': 'Dutch',
    'E':  'English',
    'F':  'French',
    'FI': 'Finnish',
    'G':  'German',
    'HU': 'Hungarian',
    'I':  'Italian',
    'J':  'Japanese',
    'K':  'Korean',
    'PL': 'Polish',
    'R':  'Russian',
    'S':  'Spanish',
    'SW': 'Swedish',
}

# clean a string
def clean(s):
    return s.replace(chr(65533),'').replace(chr(0),'').replace(u'\xa0 ',u' ').replace(u'\xa0',u' ').strip()

# main program
if __name__ == "__main__":
    games_path = '%s/games' % '/'.join(abspath(expanduser(argv[0])).split('/')[:-3])
    for region, url in URLS.items():
        print("Parsing %s..." % region)
        soup = BeautifulSoup(urlopen(url).read(), 'html.parser')
        for row in list(soup.find_all('table', {'id':'table302'}))[0].find_all('tr'):
            DUMMY, serial, title, language_s = [clean(v.text) for v in row.find_all('td')]
            language = list()
            for lang in language_s.upper().replace('(','').replace(')',']').replace('[','').split(']'):
                if len(lang) != 0 and lang not in LANG:
                    print(lang); exit()
            game_path = '%s/%s' % (games_path, serial); makedirs(game_path, exist_ok=True)
            title_path = '%s/title.txt' % game_path
            if not isfile(title_path):
                f = open(title_path, 'w'); f.write('%s\n' % title); f.close()
            language_path = '%s/language.txt' % game_path
            if len(language) != 0 and not isfile(language_path):
                f = open(language_path, 'w'); f.write('%s\n' % '\n'.join(language)); f.close()
            region_path = '%s/region.txt' % game_path
            f = open(region_path, 'w'); f.write('%s\n' % region); f.close()
