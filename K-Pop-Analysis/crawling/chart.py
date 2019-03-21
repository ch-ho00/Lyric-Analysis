import os
import mechanize
import re
import time
import sys
from collections import deque
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime
import traceback

from utils import write_log

base_url = "https://music.bugs.co.kr/chart/%s/week/%s?chartdate=%s"

# Domain of Parameter
charts = ['track', 'album', 'mv']

genre_map = {"total": "total", "ballad": "nbdp",
             "rnh": "nrh", "rns": "nrs", "elec": "nkelec",
             "rock": "nkrock", "jazz": "nkjazz", "indie": "nindie",
             "adultkpop": "ntrot"}

idx = 0
chart = "track"
year = 2018
month = 7
day = 1
m = "10000"
sleep_time = 0.5
deli = "|"
log = "ErrorLogChart.out"
genre = "total"

for i in sys.argv:
    if "-c" in i:
        chart = sys.argv[idx+1]
        assert chart in charts

    if "-g" in i:
        genre = sys.argv[idx+1]
        assert genre in genre_map.keys()
        genre = genre_map[genre]

    if "-sleep" in i:
        sleep_time = float(sys.argv[idx+1])

    if "-y" in i:
        year = sys.argv[idx+1]
        assert year.isdigit()
        year = int(year)

    if "-m" in i:
        month = sys.argv[idx+1]
        assert month.isdigit()
        month = int(month)

    if "-d" in i:
        day = sys.argv[idx+1]
        assert day.isdigit()
        day = int(day)

    if "-M" in i:
        m = sys.argv[idx+1]

    # delimiter
    if "-deli" in i:
        deli = sys.argv[idx+1]

    if "-h" in i:
        print "-c chart : Charts = %s (default: track)" % ",".join(charts)
        print "-g type  : Genre = %s (default: total)" % ",".join(genre_map.keys())
        print "-y year : year (ex. -y 2011)"
        print "-m month : month (ex. -m 10)"
        print "-d day : day (ex. -d 1)"
        print "-M weeks : crawls M charts from the date (ex. -M 50)"
        os._exit(0)

    idx += 1


_date = date(year, month, day)

br = mechanize.Browser()
br.set_handle_robots(False)

container_type = {"track": "table", "album": "ul", "mv": "ul"}


_date += timedelta(days=7)
for _ in range(int(m)):
    writing_file = False
    _date -= timedelta(days=7)
    try:
        print "Crawling the week of %s" % _date.strftime("%Y-%m-%d")
        time.sleep(sleep_time)
        url = base_url % (chart, genre, _date.strftime("%Y%m%d"))
        print(url)
        response = br.open(url)
        text = response.read()
        text = unicode(text, 'utf-8').encode('euc-kr', 'replace')

        soup = BeautifulSoup(text, features="html5lib", from_encoding="euc-kr")

        chart_time = soup.find('time')
        chart_name = re.sub('[^0-9]','', chart_time.text)

        if genre != "total" and chart == "mv":
            chart_name = _date.strftime("%Y%m%d") + _date.strftime("%Y%m%d")
            print("MV chart with specific genre does not show date")
        else:
            assert len(chart_name) == 16
            if not (datetime.strptime(chart_name[:8], "%Y%m%d").date() <= _date and
                    datetime.strptime(chart_name[8:], "%Y%m%d").date() >= _date):
                print("Probably Bugs chart doesn't have this time period. Exit program")
                break

        chart_name = chart_name[:8] + "_" + chart_name[8:]
        chart_name = "%s_%s_%s" % (chart, genre, chart_name)
        chart_name = "".join(chart_name.split())
        print(chart_name)
        if os.path.isfile("chart/%s.tsv" % chart_name):
            print("already exists. skipping")
            continue
        container = soup.find(container_type[chart], attrs={"class": "list"})

        if chart == "track":
            songs = container.findAll('tr', attrs={"rowtype": "track"})
            songs = list(filter(lambda tr: tr.has_attr("trackid"),
                                songs))
            with open("chart/%s.tsv" % chart_name, "w") as f:
                writing_file = True
                f.write("rank\tsong_id\tsong_name\talbum_id\tartist_id\tartist_name\n")
                for s in songs:
                    rank = int(s.find("strong").text)

                    track_id = s["trackid"]
                    album_id = s["albumid"]
                    artist_id = s["artistid"]

                    title = s.find("p", "title")
                    if title.find("a"):
                        title = title.find("a")["title"]
                    elif title.find("span"):
                        title = title.find("span").text
                    else:
                        title = ""
                    artist_name = s.find("p", "artist").find("a")["title"]
                    line = "%s\t%s\t%s\t%s\t%s\t%s\n" % (rank, track_id, title,
                                                       album_id, artist_id,
                                                       artist_name)
                    f.write(line.encode("utf8"))
            print("%s songs written in file chart/%s.tsv" % (len(songs), chart_name))
        elif chart == "album":
            albums = container.findAll("figure", attrs={"class":"albumInfo"})
            albums = list(filter(lambda f: f.has_attr("albumid"),
                                albums))
            with open("chart/%s.tsv" % chart_name, "w") as f:
                writing_file = True
                f.write("rank\talbum_id\talbum_name\talbum_date\tartist_id\tartist_name\n")
                for a in albums:
                    album_id = a["albumid"]
                    artist_id = a["artistid"]
                    rank = int(a.find("strong").text)
                    obj = a.find("a", attrs={"class": "btnActions"})
                    artist_name = obj["artist_name"]
                    album_name = obj["album_title"]
                    subinfo = a.find("div", attrs={"class": "subInfo"})
                    if subinfo and subinfo.find("time"):
                        album_date = subinfo.find("time").text
                    line = "%s\t%s\t%s\t%s\t%s\t%s\n" % (rank, album_id, album_name,
                                                       album_date, artist_id,
                                                       artist_name)
                    f.write(line.encode("utf8"))
            print("%s albums written in file chart/%s.tsv" % (len(albums),
                                                             chart_name))
        elif chart == "mv":
            mvs = container.findAll("figure", attrs={"class":"mvInfo"})
            mvs = list(filter(lambda f: f.has_attr("trackid"),
                                mvs))
            with open("chart/%s.tsv" % chart_name, "w") as f:
                writing_file = True
                f.write("song_id\tsong_name\tmv_date\talbum_id\tartist_name\n")
                not_processed = 0
                for i, mv in enumerate(mvs):
                    album_id = mv["albumid"]
                    track_id = mv["trackid"]
                    obj = mv.find("p", attrs={"class": "artist"})
                    if obj.find("a"):
                        artist_name = obj.find("a").text
                    elif obj.find("span"):
                        artist_name = obj.find("span").text
                    else:
                        write_log(log, "cannot find artist name. %s" % str(obj))
                        not_processed +=1
                        continue
                    obj =  mv.find("p", attrs={"class": "trackTitle"})
                    if obj.find("a"):
                        song_name = obj.find("a").text
                    else:
                        write_log(log, "cannot find song name. %s" % str(obj))
                        not_processed +=1
                        continue

                    subinfo = mv.find("div", attrs={"class": "subInfo"})
                    if subinfo and subinfo.find("time"):
                        mv_date = subinfo.find("time").text
                    line = "%s\t%s\t%s\t%s\t%s\n" % (track_id,
                                                     song_name,
                                                     mv_date,
                                                     album_id,
                                                     artist_name)
                    f.write(line.encode("utf8"))
            print("%s songs written in file chart/%s.tsv" % (len(mvs) - not_processed,
                                                             chart_name))


    except KeyboardInterrupt:
        print "Interrupt!"
        if writing_file and os.path.isfile("chart/%s.tsv" % chart_name):
            os.unlink("chart/%s.tsv" % chart_name)
            print("remove file due to error")
        break
    except urllib2.URLError:
        print "Network has some problem. Sleeping 2 mins and then resume"
        write_log(log, traceback.format_exc())
        time.sleep(60*2)
        continue
    except:
        write_log(log, traceback.format_exc())
        if writing_file and os.path.isfile("chart/%s.tsv" % chart_name):
            os.unlink("chart/%s.tsv" % chart_name)
            print("remove file due to error")
        continue
