#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime

def get_multi_artist(s):
    s = s.split("openMultiArtistSearchResultPopLayer(this, \'")[1]
    s = s.split("\',")[0]

    artist_names = []
    artist_ids = []
    for segment in s.split("\\\\n"):
        artist_name = segment.split("||")[0]
        artist_id = segment.split("||")[-1]
        assert artist_id.isdigit(), "Artist ID is not digit. Error"

        artist_ids.append(artist_id)
        artist_names.append(artist_name)

    return artist_names, artist_ids

def write_log(filename, s):
    with open(filename, "a") as f:
        print(s)
        f.write("%s: %s\n" % (str(datetime.datetime.now()), s))

