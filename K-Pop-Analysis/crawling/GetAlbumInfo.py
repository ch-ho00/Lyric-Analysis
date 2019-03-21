#!/usr/bin/python
# -*- coding: utf-8 -*-

import mechanize
import re
import time
import sys
import os
import traceback
import pymssql
import DB
from bs4 import BeautifulSoup
from datetime import datetime
import urllib2
import logging

from utils import get_multi_artist, write_log

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

cursor = DB.cursor
conn = DB.conn
sleep_time = 0.5
baseURL = "http://music.bugs.co.kr/album/%s"
baseURL_track = "http://music.bugs.co.kr/track/%s"
idx = 0
log = "ErrorLogGetAlbumInfo.out"

for i in sys.argv:
    if "-sleep" in i:
        sleep_time = float(sys.argv[idx+1])

    if "-log" in i:
        log = sys.argv[idx+1]

    if "-h" in i:
        print "-sleep: Sleep time between links (unit:sec, default: 0.5 sec) \
        \n\n -i: Input file name (default: albums) \n\n\
        -start: ID of the album where we want to start \n\n -h: help \n"
        print "[Example] -sleep 0.5 -i input \n"
        os._exit()


    idx += 1

br = mechanize.Browser()
br.set_handle_robots(False)

while True:
    queue = list(DB.yield_all_album_not_crawled())
    if len(queue) == 0:
        break
    logging.info("%s albums in the queue to process" % len(queue))
    for album_id, date in queue:
        try:
            # Read Web page
            url = baseURL % album_id
            logging.info("\n####### " + url)
            response = br.open(url)
            text = response.read()
            text = unicode(text, 'utf-8').encode('euc-kr', 'replace')
            # Construct BS HTML Tree
            soup = BeautifulSoup(text, "html5lib", from_encoding="euc-kr")

            # Find the node having the album-info
            albumnode = soup.find("table", attrs={"class": "info"})

            if albumnode == None:
                logging.info("Album Info Not exist")
                continue

            table_rows = albumnode.findAll("tr")
            info = {}
            for row in table_rows:
                row_type = row.find("th").string
                row_detail = row.find("td")
                if row_detail.find("a"):
                    row_detail = ",".join([a.text.lstrip().rstrip() for a
                                        in row_detail.findAll("a")])
                else:
                    row_detail = row_detail.string

                if row_type == u"스타일":
                    info["style"] = row_detail
                elif row_type == u"앨범 종류":
                    info["type"] = row_detail
                elif row_type == u"유통사":
                    info["distributor"] = row_detail
                elif row_type == u"기획사":
                    info["company"] = row_detail
                elif row_type == u"발매일" and date is None:
                    info["date"] = datetime.strptime(row_detail, "%Y.%m.%d")

            album_content = soup.find("p", attrs={"class": "albumContents"})
            if album_content:
                info["review"] = album_content.find("span").text
            DB.update_album_info(album_id, info)
            logging.info("updated %s attributes" % len(info))

            time.sleep(sleep_time)
        except KeyboardInterrupt:
            print "Interrupt!"
            break
        except urllib2.URLError:
            logging.error("Network has some problem. Sleeping 2 mins and then resume")
            write_log(log, traceback.format_exc())
            time.sleep(60*2)
            continue
        except:
            logging.error("Error on URL or HTML(Parsing)")
            write_log(log, traceback.format_exc())
            continue

        try:
            pattern = re.compile(r'\"og:image" content=\"(.+?)\"')
            match = pattern.findall(text)
            image = match[0].strip()
            f = br.retrieve(image, 'album_image/'+image[image.rfind("/")+1:])
            logging.info("Saved Album Image")
        except KeyboardInterrupt:
            print "Interrupt!"
            break
        except urllib2.URLError:
            logging.error("Network has some problem. Sleeping 2 mins and then resume")
            write_log(log, traceback.format_exc())
            time.sleep(60*2)
            continue
        except:
            logging.error("DB Error or Storing Image Error")
            write_log(log, traceback.format_exc())
            continue

        try:
            DB.check_song_table()
            DB.check_song_artist_table()
            DB.check_artist_table()

            song_table = soup.find("table", attrs={"class": "trackList"})
            song_ids = []
            song_titles= []
            lyrics = []
            lyric_providers = []
            producer_infos = []
            song_artist_pairs = []
            artist_ids = []
            artist_names = []
            downloaded = []
            for i, row in enumerate(song_table.find("tbody").findChildren("tr",
                                                                        recursive=False)):
                if row.has_attr("rowtype") is not None and row["rowtype"] == "track":
                    song_id = row["trackid"]
                    if song_id is None:
                        continue
                    song_ids.append(song_id)

                    multi_artist = row["multiartist"]
                    if multi_artist == "N":
                        artist_id = row["artistid"]
                        song_artist_pairs.append((song_id, artist_id))
                        artist_ids.append(artist_id)
                        ahref = row.find("p", attrs={"class": "artist"})
                        ahref = ahref.find("a")
                        artist_name = ahref["title"]
                        artist_names.append(artist_name)
                    else:
                        ahref = row.find("p", attrs={"class": "artist"})
                        ahref = ahref.find("a", attrs={"class":"more"})
                        _artist_names, _artist_ids = get_multi_artist(ahref["onclick"])

                        artist_ids += _artist_ids
                        artist_names += _artist_names
                        song_artist_pairs += zip([song_id for _ in range(len(_artist_ids))],
                                                _artist_ids)
                    song_title = row.find("p", attrs={"class": "title"}).text
                    song_title = song_title.strip()
                    song_titles.append(song_title)
                    playable = row.find("p", attrs={"class":"title"}).find("a") is not None
                    if playable:
                        downloaded.append(False)
                    else:
                        downloaded.append(None)

                    # Read the detail info of the song from Web
                    time.sleep(sleep_time)
                    response = br.open(baseURL_track % song_id)
                    song_text = response.read()
                    song_text = unicode(song_text, 'utf-8').encode('euc-kr', 'replace')

                    # Construct BS HTML tree on the web page for the song
                    soup2 = BeautifulSoup(song_text, "html5lib", from_encoding="euc-kr")
                    ly_cont = soup2.find("div", attrs={"class": "lyricsContainer"})
                    if ly_cont is not None and ly_cont.find("xmp") is not None:
                        lyric = ly_cont.find("xmp").text
                        lyric_provider = ly_cont.find("cite",
                                                    attrs={"class": "writer"})
                        if lyric_provider is not None:
                            lyric_provider = lyric_provider.text
                    else:
                        lyric, lyric_provider = None, None
                    lyrics.append(lyric)
                    lyric_providers.append(lyric_provider)

                    # crawl song writer/composer info
                    info_table = soup2.find("table", attrs={"class":"info"})
                    producers = None
                    for row in info_table.find("tbody").findChildren("tr",recursive=False):
                        if row.find("th").text == u"참여 정보":
                            s = ""
                            for span in row.find("td").findAll("span", recursive=False):
                                _text = span.text.rstrip().lstrip()
                                if span.has_attr("class"):
                                    if span["class"][0] == "title":
                                        s += (_text + ":")
                                    elif span["class"][0] == "bar":
                                        s += ","
                                else:
                                    s += "".join(_text.split())

                            producers = s
                    producer_infos.append(producers)

            DB.insert_songs(song_ids, song_titles,
                            [album_id for _ in range(len(song_ids))],
                            lyrics, lyric_providers, producer_infos, downloaded)
            DB.insert_song_artist(song_artist_pairs)

            # remove duplicates
            artist_ids, artist_names = zip(*set(zip(artist_ids, artist_names)))
            DB.insert_artists(artist_ids, artist_names)

            logging.info("inserted %s songs for album_id: %s" % (len(song_ids), album_id))
            logging.info("inserted %s artists including %s" % (len(artist_names),
                                                        artist_names[0]))
        except KeyboardInterrupt:
            print "Interrupt!"
            break
        except urllib2.URLError:
            logging.error("Network has some problem. Sleeping 2 mins and then resume")
            write_log(log, traceback.format_exc())
            time.sleep(60*2)
            continue
        except:
            logging.error("Error Crawling #%s song" % (i+1))
            write_log(log, traceback.format_exc())
