#!/usr/bin/python
# -*- coding: utf-8 -*-

import mechanize
import re
import time
import os
import sys
from bs4 import BeautifulSoup
from datetime import datetime
import traceback
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


import DB
from utils import get_multi_artist, write_log
import urllib2

idx = 0
sleep_time = 0.5
startPage = 1
baseURL = "https://music.bugs.co.kr/genre/kpop/%s/total?tabtype=3&page="
log = "ErrorLogGetAlbumList.out"
genre = "ballad"

for i in sys.argv:
    if "-sleep" in i:
        sleep_time = float(sys.argv[idx+1])

    if "-log" in i:
        log = sys.argv[idx+1]

    if "-s" in i:
        startPage = int(sys.argv[idx+1])

    if "-b" in i:
        baseURL = sys.argv[idx+1]

    if "-g" in i:
        genre = sys.argv[idx+1]
        assert genre in ["ballad", "rnh", "rns", "elec",
                         "rock", "jazz", "indie", "adultkpop",
                         "nost", "nclassic", "nnewage","njpop", "nwpop",
                         "nkclassic", "nccm", "nchildren", "nprenatal", "ncarol"]
        if genre in ["nost", "nclassic", "nnewage","njpop", "nwpop",
                     "nkclassic", "nccm", "nchildren", "nprenatal", "ncarol"]:
            baseURL = "https://music.bugs.co.kr/newest/album/%s?tabetype=3&page="
    if "-h" in i:
        print "-sleep: Sleep time between links (unit:sec, default: 0.5 sec)"
        print "\n\n-b:BaseURL (default:\"https://music.bugs.co.kr/genre/kpop/%s/total?tabtype=3&page=\")"
        print "\n\n-g:Genre (should be one of [ballad, rnh, rns, elec, rock, jazz, indie, adultkpop)"
        print "\n nost, nclassic, nnewage,njpop, nwpop, nkclassic, nccm, nchildren, nprenatal, ncarol"
        print "\n\n -h: help \n"
        os._exit(0)

    idx += 1

baseURL = baseURL % genre

print "Checking DB tables"

DB.check_album_table()
DB.check_artist_table()
DB.check_album_artist_table()

print "Crawling Genre: %s" % genre

br = mechanize.Browser()
br.set_handle_robots(False)

page = startPage

while True:
    url = baseURL + str(page)

    time.sleep(sleep_time)

    try:
        logging.info("\nCrawling " + url)

        response = br.open(url)
        text = response.read()
        text = unicode(text, 'utf-8').encode('euc-kr', 'replace')

        soup = BeautifulSoup(text, features="html5lib", from_encoding="euc-kr")

        # album and ids name
        count = 0
        albums = soup.findAll('figure', attrs={'class': 'albumInfo'})

        album_titles = []
        album_ids = []
        artist_ids = []
        artist_names = []
        album_dates = []
        album_artist_pairs = []
        for a in albums:
            try:
                album_id = a['albumid']
                album_ids.append(album_id)
                assert album_id.isdigit(), "Album ID is not digit. Error"

                ahrefs = a.find('p',
                                attrs={'class': 'artist'}).findChildren("a",
                                                                        recursive=False)
                if len(ahrefs) == 1:
                    artist_name = ahrefs[0].text
                    artist_id = ahrefs[0]["href"].split('?')[0].split('/')[-1]
                    assert artist_id.isdigit(), "Artist ID is not digit. Error"
                    artist_ids.append(artist_id)
                    artist_names.append(artist_name)
                    album_artist_pairs.append((album_id, artist_id))

                elif len(ahrefs) > 1:
                    # extracting from javascript code
                    _artist_names, _artist_ids = get_multi_artist(ahrefs[1]["onclick"])
                    album_artist_pairs = list(zip([album_id for _ in range(len(_artist_ids))],
                                            _artist_ids))
                    artist_ids += _artist_ids
                    artist_names += _artist_names

                album_title = a.find('a',
                                    attrs={'class': 'btnActions'})["album_title"]

                album_titles.append(album_title)

                date_text = a.find('time').text
                if len(date_text) == 10:
                    album_date = datetime.strptime(date_text, "%Y.%m.%d")
                elif len(date_text) == 7:
                    album_date = datetime.strptime(date_text, "%Y.%m")
                elif len(date_text) == 4:
                    album_date = datetime.strptime(date_text, "%Y")
                else:
                    album_date = None

                album_dates.append(album_date)
                count += 1
            except AssertionError:
                logging.error("Assertion Error")
                write_log(log, traceback.format_exc())
                continue
        # bulk insert
        DB.insert_album_basics(album_ids, album_titles,
                               [genre for _ in range(count)],
                               album_dates)
        DB.insert_artists(artist_ids, artist_names)
        DB.insert_album_artist(album_artist_pairs)
        if album_date.year < 2000:
            logging.info("Finsihed Crawling All Albums in %s After 2000" % genre)
            os._exit(0)
        logging.info("Done with Page %s. %s albums including %s/%s/%s" % (page, count,
                                                album_title, artist_name,
                                                '{:%y.%m.%d}'.format(album_date)))
        page += 1
    except KeyboardInterrupt:
        print "Interrupt!"
        break
    except urllib2.URLError:
        logging.error("Network has some problem. Sleeping 2 mins and then resume")
        write_log(log, traceback.format_exc())
        time.sleep(60*2)
        continue
    except:
        logging.error("Unexpected Error: " + url)
        write_log(log, traceback.format_exc())
        continue
