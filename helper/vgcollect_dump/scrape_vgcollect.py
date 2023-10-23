#! /usr/bin/env python3
'''
Scrape metadata from VGCollect
'''
from bs4 import BeautifulSoup
from datetime import datetime
from json import dump as jdump
from sys import argv, stdout
from urllib.request import urlopen

# base URLs
BASE_URLS = {
    'NTSC-U': 'https://vgcollect.com/browse/ps2/',
    'NTSC-J': 'https://vgcollect.com/browse/ps2jp/',
    'PAL': 'https://vgcollect.com/browse/ps2eu/',
    'KOREAN': 'https://vgcollect.com/browse/ps2kr/',
    'CHINESE': 'https://vgcollect.com/browse/ps2cn/',
    'AUSTRALIAN': 'https://vgcollect.com/browse/ps2au/',
}

# clean a string
def clean(s):
    return s.replace(chr(65533),'').replace(chr(0),'').replace(u'\xa0 ',u' ').replace(u'\xa0',u' ').strip()

# main program
if __name__ == "__main__":
    data = dict()
    for region, base_url in BASE_URLS.items():
        # load page list
        print("Loading page list for %s region..." % region); stdout.flush()
        num_pages = 1; soup = BeautifulSoup(urlopen(base_url).read(), 'html.parser')
        for link in soup.find_all('a', href=True):
            url = link['href']
            if url.startswith(base_url):
                try:
                    num_pages = max(num_pages, int(url.split('/')[-1]))
                except:
                    pass

        # load games
        for page_num in range(1, num_pages+1):
            print("Scraping page %d of %d" % (page_num, num_pages), end=''); stdout.flush()
            page_soup = BeautifulSoup(urlopen('%s%d' % (base_url, page_num)), 'html.parser')
            for link in page_soup.find_all('a', href=True):
                url = link['href']
                if url.startswith('https://vgcollect.com/item'):
                    print('.', end=''); stdout.flush()
                    curr_data = {'region': region}; serial = None
                    game_soup = BeautifulSoup(urlopen(url), 'html.parser')
                    curr_data['title'] = clean(list(game_soup.find_all('h2'))[0].text)
                    for row in game_soup.find_all('tr'):
                        cols = [clean(col.text) for col in row.find_all('td')]
                        if len(cols) < 2 or cols[1] == 'NA':
                            continue
                        if cols[0] == 'Publisher(s):':
                            curr_data['publisher'] = cols[1]
                        elif cols[0] == 'Developer(s):':
                            curr_data['developer'] = cols[1]
                        elif cols[0] == 'Genre:':
                            curr_data['genre'] = cols[1]
                        elif cols[0] == 'Item Number:':
                            serial = cols[1]
                        elif cols[0] == 'Release Date:':
                            try:
                                curr_data['release_date'] = datetime.strptime(cols[1], '%B %d %Y').strftime('%Y-%m-%d')
                            except:
                                try:
                                    curr_data['release_date'] = datetime.strptime(cols[1], '%B %Y').strftime('%Y-%m')
                                except:
                                    try:
                                        curr_data['release_date'] = str(int(cols[1]))
                                    except:
                                        pass
                    if serial is None:
                        continue # raise RuntimeError("No serial: %s" % url)
                    elif serial in data:
                        continue # raise ValueError("Duplicate serial: %s" % url)
                    else:
                        data[serial] = curr_data
            print(); stdout.flush()
        print("Successfully scraped %d pages       " % num_pages); stdout.flush()
    f = open('vgcollect_dump.json', 'w'); jdump(data, f); f.close()
