import os
import DB

DB.renew_artist_table()
DB.renew_album_table()
DB.renew_song_table()
DB.renew_album_artist_table()
DB.renew_song_artist_table()

print("changed the DB schema")
print("now checking which songs are downloaded already")

downloaded_count = 0
not_count = 0
for song_id in list(DB.yield_all_songs()):
    music_file_name = "./song_file/%s.flv" % song_id
    if os.path.isfile(music_file_name):
        DB.mark_song_downloaded(song_id, value=1)
        downloaded_count += 1
    else:
        DB.mark_song_downloaded(song_id, value=0)
        not_count += 1
print("already downloaded songs %s, not downloaded %s" % (downloaded_count,
                                                          not_count))
