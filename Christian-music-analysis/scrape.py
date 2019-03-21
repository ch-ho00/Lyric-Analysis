import requests
from bs4 import BeautifulSoup
import codecs
from tqdm import tqdm


def artist_list(save_dir):
    # get list of artist and their id
    page = requests.get("https://www.jesusfreakhideout.com/lyrics/new/default.asp")
    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.find('table', id='resultsList')
    table = str(table)
    artist_list ={}
    start = 0
    while(start != -1):
        try:
            start = table.find("artist_id=",start + 1)
            artist_id = int(table[start + len("artist_id="): table.find("\"",start)])
            artist_list[artist_id] = table[start+len("artist_id=")+len(str(artist_id))+2:table.find("</a>", start)]
        except:
            print("Scanned of list of Artist")
    filename = "artistID.txt"
    with codecs.open(str(save_dir) + "/"+ filename, 'w', encoding='utf8') as f:
        for i in artist_list:
            f.write(str(i) +" : " + str(artist_list[i]))
            f.write('\n')
    print("Saved list of artist")
    return artist_list

def artist_track(artist_list,save_dir):
    # get list of artist corresponding track titles and id
    artist_track= {}
    tmp = 0
    for art_id in tqdm(artist_list):
        tracks_url = "https://www.jesusfreakhideout.com/lyrics/new/artist_list.asp?artist_id=" + str(art_id)
        page = requests.get(tracks_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find('table')
        table = str(table)
#        print(table)
        trackid_title = {}
        start = 0
        while start != -1:
            try:
                start = table.find("track_id=",start + 1)
                track_id = str(table[start + len("track_id="): table.find("\"",start)]).split()
                if len(str(track_id)) < 10:
                    tmp +=1
                    tmptitle = table[start+len("track_id=")+len(str(track_id))+ 2:table.find("</a>", start)]
                    trackid_title[int(track_id[0])] = tmptitle
            except:
                continue
        artist_track[art_id] = trackid_title   
    print("Number of Artist = " + str(len(artist_track)))
    #save result
    num = 0
    for i in artist_track:
        num = num + len(artist_track[i])
    print("Number of tracks = " + str(num))
    filename = "artist_track.txt"
    copy = artist_track
    with codecs.open(str(save_dir) + "/"+ filename, 'w', encoding='utf8') as f:
        for i in artist_track:
            f.write(str(i) +" : " + str(artist_track[i]))
            f.write('\n')
            f.write('\n')
    print("Saved artists' tracklist")
    return copy

def lyric_list(artist_track, save_dir):
    # get list of lyrics indexed by their corresponding track id
    lyric_list = {}
    for artist in tqdm(artist_track):
        for trackid in artist_track[artist]:
            song_url = "https://www.jesusfreakhideout.com/lyrics/new/track.asp?track_id=" + str(trackid)
            page = requests.get(song_url)
            soup = BeautifulSoup(page.content, 'html.parser')
            [x.extract() for x in soup.findAll("i")]
            for br in soup.find_all("br"):
                br.replace_with(" ")
                lyric = [tag.get_text() for tag in soup.select(".w3-left")]
                lyric = lyric[0]
                lyric = lyric.replace("\n", "")
                lyric = lyric.replace("\t", "")
                lyric = lyric.replace("\r", "")
                lyric_list[trackid] = lyric
    #save result
    filename = "lyric.txt"
    copy = lyric_list
    with codecs.open(str(save_dir) + "/"+ filename, 'w', encoding='utf8') as f:
        for i in lyric_list:
            f.write(str(i) +" : " + str(lyric_list[i]))
            f.write('\n')
            f.write('\n')
    print("Saved lyric list")
    return copy

