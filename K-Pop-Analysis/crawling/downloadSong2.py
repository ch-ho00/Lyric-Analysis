
import re
import time
import mechanize
import sys
import pymssql
import json
import DB
import os.path
import traceback
from utils import write_log
import os
import urllib2
import logging
import shlex
from easyprocess import EasyProcess

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

log = "ErrorDownloadSong.out"
br = mechanize.Browser()
br.set_handle_robots(False)


sleep_time = 0.5
iFile = "albums"
baseURL = "http://music.bugs.co.kr/album/"
baseURL_track = "http://music.bugs.co.kr/track/"
idx = 0
startSong = ""
maxTRY = 20
range_start = None
range_end = None
error = False
time_out_duration = 60*7 # 7mins
for i in sys.argv:
    if "-sleep" in i:
        sleep_time = float(sys.argv[idx+1])

    if "-h" in i:
        print " -sleep: Sleep time between songs (unit:sec, default: 0.5 sec) \n\n -h: help \n"
        print "[Example] -sleep 0.5 -i input \n"
        sys.exit(0)

    if "-log" in i:
        log = sys.argv[idx+1]

    if "-t" in i:
        maxTRY = int(sys.argv[idx+1])

    if "-range-start" in i:
        range_start = int(sys.argv[idx+1])

    if "-range-end" in i:
        range_end = int(sys.argv[idx+1])

    if "-skip-downloaded" in i:
        skip_downloaded = True
    else:
        skip_downloaded = False
    idx += 1

songs = list(DB.yield_all_songs_not_downloaded(range_start, range_end))
logging.info("%s songs on queue" % len(songs))
for track_id in songs:
    logging.info("### downloading song_id: %s" % track_id)
    music_file_name = "./song_file/%s.flv"
    output_file = music_file_name % track_id

    time.sleep(sleep_time)
    if skip_downloaded and os.path.isfile(music_file_name):
        print("already downloaded. skipping")
        DB.mark_song_downloaded(track_id)
        continue

    try:
        url = "https://music.bugs.co.kr/newPlayer/secureUrl?track_id=%s&format=aac_128"

        response = None
        flag = 0
        for i in range(maxTRY):
            try:
                response = br.open(url % track_id)
                flag = 1
                break

            except:
                time.sleep(sleep_time)
                print "Server is not responding! Retry - "+str(i+1)
                continue

        if flag == 0:
            print "Server is not responding!"

            if error != True:
                f2 = open("dwSong_Log", "a")
                f2.write(track_id + "|msg:Server is not responding! \n")
                f2.close()

            continue

        text = response.read()

        try:
            data = json.loads(text)
        except ValueError:
            logging.info("Track does not have audio")
            DB.mark_song_downloaded(track_id, value=None)
            continue
        logging.info("Downloading:" + track_id)

        # print arg
        ffmpeg_command = "ffmpeg -i \"%s\" -y -f flv %s" % (data["secureUrl"].rstrip(),
                                                            output_file)
        logging.debug(ffmpeg_command)
        isTimeout = EasyProcess(ffmpeg_command).call(timeout=time_out_duration).timeout_happened
        # Test whether a song is completely downloaded
        if isTimeout:
            logging.error("timeout happened!")
            if os.path.isfile(output_file):
                os.unlink(output_file)
                logging.error("Remove "+track_id)
            continue
        else:
            if os.path.isfile(output_file):
                logging.info("sucessfully saved")
                DB.mark_song_downloaded(track_id)
            else:
                logging.error("not saved")

    except KeyboardInterrupt:
        print "KeyboardInterrupt"
        if os.path.isfile(output_file):
            logging.error("Remove "+track_id)
            os.unlink(output_file)
        break
    except urllib2.URLError:
        logging.error("Network has some problem. Sleeping 2 mins and then resume")
        write_log(log, traceback.format_exc())
        time.sleep(60*2)
        continue
    except:
        if os.path.isfile(output_file):
            logging.error("Remove "+track_id)
            os.unlink(output_file)
        write_log(log, traceback.format_exc())
        continue
