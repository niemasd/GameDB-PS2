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
    'A':   'Arabic',
    'AF':  'Afrikaans',
    'AR':  'Arabic',
    'C':   'Czech',
    'CA':  'Catalan',
    'CAT': 'Catalan',
    'CH':  'Chinese',
    'CR':  'Croatian', # not sure
    'CZ':  'Czech',
    'D':   'Danish',
    'DU':  'Dutch',
    'E':   'English',
    'F':   'French',
    'FI':  'Finnish',
    'FL':  'Finnish',
    'G':   'German',
    'GA':  'Gaelic',
    'GR':  'Greek',
    'H':   'Hungarian',
    'HI':  'Hindi',
    'HU':  'Hungarian',
    'I':   'Italian',
    'J':   'Japanese',
    'K':   'Korean',
    'N':   'Norwegian',
    'NW':  'Norwegian',
    'P':   'Portuguese',
    'PL':  'Polish',
    'PO':  'Polish', # not sure
    'R':   'Russian',
    'S':   'Spanish',
    'SC':  'Scandinavian',
    'SW':  'Swedish',
    'T':   'Turkish',
}

# clean a string
def clean(s):
    return s.replace(chr(65533),'').replace(chr(0),'').replace(u'\xa0 ',u' ').replace(u'\xa0',u' ').strip()

# main program
if __name__ == "__main__":
    games_path = '%s/games' % '/'.join(abspath(expanduser(argv[0])).split('/')[:-3])
    for region, url in URLS.items():
        print("Parsing %s..." % region)
        raw_data = clean(urlopen(url).read().decode('utf-8', errors='replace'))
        raw_data = raw_data.replace('<tr>\n<tr>','<tr>')
        raw_data = raw_data.replace('</td>\n</td>', '</td>\n</tr>')
        raw_data = raw_data.replace('<td>\n</tr>', '</td>\n</tr>')
        raw_data = raw_data.replace('</td>\n<tr>', '</td>\n</tr>\n<tr>')
        soup = BeautifulSoup(raw_data, 'html.parser')
        for row in soup.find_all('tr'):
            cols = [clean(v.text) for v in row.find_all('td')]
            if len(cols) == 0:
                continue
            DUMMY, serial, title, language_s = cols
            language = list()
            for lang in language_s.upper().replace('<','').replace('/TD>','').replace(';','').replace('`','').replace('J[E]','[J][E]').replace('(N(SW)','(N)(SW)').replace('{','').replace('(','').replace('}',']').replace(')',']').replace('[','').split(']'):
                if len(lang) != 0 and lang not in LANG:
                    print(title); print(lang); exit()
            game_path = '%s/%s' % (games_path, serial); makedirs(game_path, exist_ok=True)
            title_path = '%s/title.txt' % game_path
            if not isfile(title_path):
                f = open(title_path, 'w'); f.write('%s\n' % title); f.close()
            language_path = '%s/language.txt' % game_path
            if len(language) != 0 and not isfile(language_path):
                f = open(language_path, 'w'); f.write('%s\n' % '\n'.join(language)); f.close()
            region_path = '%s/region.txt' % game_path
            f = open(region_path, 'w'); f.write('%s\n' % region); f.close()
