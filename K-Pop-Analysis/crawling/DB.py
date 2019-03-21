import re
import pymssql
import traceback

def create_connection():
#    return pymssql.connect(server='localhost', port=1433,
#                           user='kpop', password='Bugs_sql1234', database='KPOP')
    return pymssql.connect(server='localhost',
                            user='sa', password='Bugs_sql2028', database='KPOP')

conn = create_connection()
cursor = conn.cursor()

def check_song_table():
    cursor.execute("""IF object_id(\'song\', \'U\') is null
                        CREATE TABLE song (id varchar(64)
                                                NOT NULL PRIMARY KEY
                                                WITH (IGNORE_DUP_KEY = ON),
                                            album_id varchar(64),
                                            name varchar(MAX),
                                            lyrics varchar(MAX),
                                            lyrics_provider varchar(64),
                                            producers varchar(MAX),
                                            downloaded BIT)
                   """)
    conn.commit()

def check_song_artist_table():
    cursor.execute("""IF object_id(\'song_artist\', \'U\') is null
                        CREATE TABLE song_artist (song_id varchar(64) NOT NULL,
                                                   artist_id varchar(64) NOT NULL)
                   """)
    cursor.execute("""
                   IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS WHERE CONSTRAINT_NAME = 'PK_song_artist')
                   BEGIN
                    ALTER TABLE dbo.song_artist ADD CONSTRAINT PK_song_artist
                        PRIMARY KEY (song_id, artist_id) WITH (IGNORE_DUP_KEY = ON)
                   END
                   """)
    conn.commit()

def check_album_table():
    cursor.execute("""IF object_id(\'album\', \'U\') is null
                        CREATE TABLE album (id varchar(64)
                                                NOT NULL PRIMARY KEY
                                                WITH (IGNORE_DUP_KEY = ON),
                                            name varchar(MAX),
                                            type varchar(MAX),
                                            genre varchar(MAX),
                                            style varchar(MAX),
                                            date varchar(64),
                                            distributor varchar(MAX),
                                            company varchar(MAX),
                                            review varchar(MAX))
                   """)
    conn.commit()

def check_artist_table():
    cursor.execute("""IF object_id(\'artist\', \'U\') is null
                        CREATE TABLE artist (id varchar(64)
                                                NOT NULL PRIMARY KEY
                                                WITH (IGNORE_DUP_KEY = ON),
                                             name varchar(MAX))
                   """)
    conn.commit()

def check_album_artist_table():
    cursor.execute("""IF object_id(\'album_artist\', \'U\') is null
                        CREATE TABLE album_artist (album_id varchar(64) NOT NULL,
                                                   artist_id varchar(64) NOT NULL)
                   """)
    cursor.execute("""
                   IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS WHERE CONSTRAINT_NAME = 'PK_album_artist')
                   BEGIN
                    ALTER TABLE dbo.album_artist ADD CONSTRAINT PK_album_artist
                        PRIMARY KEY (album_id, artist_id) WITH (IGNORE_DUP_KEY = ON)
                   END
                   """)
    conn.commit()



def insert_album_basics(ids, names, genres, dates):
    cursor.executemany("""INSERT INTO album (id, name, genre, date)
                                            VALUES (%d, %s, %s, %s)""",
                        zip(ids, names, genres, dates))
    conn.commit()

def insert_artists(ids, names):
    cursor.executemany("""INSERT INTO artist VALUES (%d, %d)""",
                        zip(ids, names))
    conn.commit()

def insert_album_artist(album_artist_pairs):
    cursor.executemany("""INSERT INTO album_artist VALUES (%d, %d)""",
                        album_artist_pairs)
    conn.commit()

def insert_songs(ids, titles, album_ids, lyrics,
                 lyric_providers, producers, downloaded):
    cursor.executemany("""INSERT INTO song (id, album_id, name, lyrics, lyrics_provider, producers, downloaded)
                            VALUES (%d, %s, %d, %s, %s, %s, %s)""",
                        zip(ids, album_ids, titles,
                            lyrics, lyric_providers, producers, downloaded))
    conn.commit()

def insert_song_artist(song_artist_pairs):
    cursor.executemany("""INSERT INTO song_artist VALUES (%d, %d)""",
                        song_artist_pairs)
    conn.commit()


def yield_all_album_not_crawled():
    # second connection for multiple concurrent queries
    with create_connection() as conn2:
        with conn.cursor(as_dict=True) as cursor2:
            cursor2.execute("SELECT id, date FROM album WHERE type is NULL")
            for row in cursor2:
                yield row['id'], row['date']

def yield_all_songs_not_downloaded(range_start, range_end):
    # second connection for multiple concurrent queries
    with create_connection() as conn2:
        with conn.cursor(as_dict=True) as cursor2:
            if range_start is None or range_end is None:
                cursor2.execute("SELECT id FROM song WHERE downloaded = 0")
            else:
                cursor2.execute("SELECT id FROM song WHERE downloaded = 0 and id > %s and id < %s", (range_start, range_end))
            for row in cursor2:
                yield row['id']

def yield_all_songs():
    # second connection for multiple concurrent queries
    with create_connection() as conn2:
        with conn.cursor(as_dict=True) as cursor2:
            cursor2.execute("SELECT id FROM song")
            for row in cursor2:
                yield row['id']

def mark_song_downloaded(_id, value=1):
    cursor.execute("UPDATE song SET downloaded = %s WHERE id = %s", (value, _id))
    conn.commit()

def update_album_info(_id, info):
    query = "UPDATE album SET %s WHERE id = %s"
    s = ""
    values = []
    for i, key in enumerate(info.keys()):
        if i > 0:
            s += ", "
        s += (key + " = %s")
        values.append(info[key])
    cursor.execute(query % (s, _id), tuple(values))
    conn.commit()

########################## migration from old DB

def renew_song_table():
    cursor.execute("""ALTER TABLE song
                        ALTER COLUMN id VARCHAR(64) NOT NULL""")
    try:
        cursor.execute("""ALTER TABLE song
                            ADD CONSTRAINT song_pk_id PRIMARY KEY (id)""")
    except pymssql.OperationalError as e:
        if "already has a primary key" in str(e):
            print("skip defining primary key")
        else:
            trackback.print_exec()
            exit()

    cursor.execute("""ALTER TABLE song
                        ALTER COLUMN name varchar(MAX);""")
    cursor.execute("""ALTER TABLE song
                        ALTER COLUMN lyrics varchar(MAX);""")
    cursor.execute("""ALTER TABLE song
                        ALTER COLUMN lyrics_provider varchar(64);""")
    cursor.execute("""ALTER TABLE song
                        ADD
                            producers varchar(MAX),
                            downloaded BIT""")
    cursor.execute("""ALTER TABLE song REBUILD WITH (IGNORE_DUP_KEY = ON)""")
    conn.commit()

def renew_song_artist_table():
    cursor.execute("""ALTER TABLE song_artist
                        ALTER COLUMN song_id VARCHAR(64) NOT NULL""")
    cursor.execute("""ALTER TABLE song_artist
                        ALTER COLUMN artist_id VARCHAR(64) NOT NULL""")
    try:
        cursor.execute("""ALTER TABLE song_artist ADD CONSTRAINT PK_song_artist
                            PRIMARY KEY (song_id, artist_id) WITH (IGNORE_DUP_KEY = ON)""")
    except pymssql.OperationalError as e:
        if "already has a primary key" in str(e):
            print("skip defining primary key")
        else:
            trackback.print_exec()
            exit()

    cursor.execute("""ALTER TABLE song_artist REBUILD WITH (IGNORE_DUP_KEY = ON)""")
    conn.commit()

def renew_album_artist_table():
    cursor.execute("""ALTER TABLE album_artist
                        ALTER COLUMN album_id VARCHAR(64) NOT NULL""")
    cursor.execute("""ALTER TABLE album_artist
                        ALTER COLUMN artist_id VARCHAR(64) NOT NULL""")
    try:
        cursor.execute("""ALTER TABLE album_artist ADD CONSTRAINT PK_album_artist
                            PRIMARY KEY (album_id, artist_id) WITH (IGNORE_DUP_KEY = ON)""")
    except pymssql.OperationalError as e:
        if "already has a primary key" in str(e):
            print("skip defining primary key")
        else:
            trackback.print_exec()
            exit()
    cursor.execute("""ALTER TABLE album_artist REBUILD WITH (IGNORE_DUP_KEY = ON)""")
    conn.commit()


def renew_album_table():
    cursor.execute("""ALTER TABLE album
                        ALTER COLUMN id VARCHAR(64) NOT NULL""")
    try:
        cursor.execute("""ALTER TABLE album
                            ADD CONSTRAINT album_pk_id PRIMARY KEY (id)""")
    except pymssql.OperationalError as e:
        if "already has a primary key" in str(e):
            print("skip defining primary key")
        else:
            trackback.print_exec()
            exit()
    cursor.execute("""ALTER TABLE album
                        ALTER COLUMN name varchar(MAX);""")
    cursor.execute("""ALTER TABLE album
                        ALTER COLUMN type varchar(MAX);""")
    cursor.execute("""ALTER TABLE album
                        ALTER COLUMN genre varchar(MAX);""")
    cursor.execute("""ALTER TABLE album
                        ALTER COLUMN style varchar(MAX);""")
    cursor.execute("""ALTER TABLE album
                        ALTER COLUMN distributor varchar(MAX);""")
    cursor.execute("""ALTER TABLE album
                        ALTER COLUMN review varchar(MAX);""")
    cursor.execute("""ALTER TABLE album
                        ADD
                            company varchar(MAX)""")
    cursor.execute("""ALTER TABLE album REBUILD WITH (IGNORE_DUP_KEY = ON)""")
    conn.commit()

def renew_artist_table():
    cursor.execute("""ALTER TABLE artist
                        ALTER COLUMN id VARCHAR(64) NOT NULL""")
    try:
        cursor.execute("""ALTER TABLE artist ADD CONSTRAINT PK_artist PRIMARY KEY (id)""")
    except pymssql.OperationalError as e:
        if "already has a primary key" in str(e):
            print("skip defining primary key")
        else:
            trackback.print_exec()
            exit()
    cursor.execute("""ALTER TABLE artist
                        ALTER COLUMN name varchar(MAX);""")
    cursor.execute("""ALTER TABLE artist REBUILD WITH (IGNORE_DUP_KEY = ON)""")
    conn.commit()


