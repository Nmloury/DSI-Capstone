#!/usr/bin/env python

import genius_functions as gf
import pandas as pd
import psycopg2 as psy

# Get Song IDs for Popular Artists
artists = ['kanye west', 'ludacris', 'lil wayne', 'wu-tang clan', 'future']
artist_ids = []
for artist in artists:
    artist_ids.append(gf.get_artist_id(artist))
print zip(artists, artist_ids)

# Get Artist Song Info
song_info = []
for aid in artist_ids:
    song_info += gf.get_song_info(aid)

# Create Song Info DataFrame
song_info_df = pd.DataFrame(song_info)

# Get Referents/annotations for Drake Songs
ref_info = []
ann_info = []
for id in song_info_df['id']:
    ref, ann = gf.get_ref_ann_info(id)
    ref_info += ref
    ann_info += ann


# Insert songs into Database
def insert_songs(songs, database):
    '''Insert Genius Songs into a database'''
    for i, song in enumerate(songs):
        conn = psy.connect("dbname=%s" % database)
        cursor = conn.cursor()
        try:
            cursor.execute(
                """INSERT INTO songs (song_id, hot, unreviewed_annotations,
                    title, full_title, artist, artist_id, annotation_count)
                    VALUES (%(id)s, %(hot)s, %(unreviewed_annotations)s,
                    %(title)s, %(full_title)s, %(artist)s, %(artist_id)s,
                    %(annotation_count)s);""", song
            )
            conn.commit()
            print "Song %s added!" % song['title']
        except Exception, e:
            print e.pgerror


# Insert referents into Database
def insert_refs(refs, database):
    '''Insert Genius referents into a database'''
    for ref in refs:
        conn = psy.connect("dbname=%s" % database)
        cursor = conn.cursor()
        try:
            cursor.execute(
                """INSERT INTO referents (id, song_id, classification,
                fragment, is_description, annotator_id) VALUES (%(id)s,
                %(song_id)s, %(classification)s,%(fragment)s,
                %(is_description)s, %(annotator_id)s);""", ref
            )
            conn.commit()
            print "Referent %s added!" % ref['id']
        except Exception, e:
            print e.pgerror


# Insert annotations into Database
def insert_annotations(anns, database):
    '''Insert Genius annotations into a database'''
    for ann in anns:
        conn = psy.connect("dbname=%s" % database)
        cursor = conn.cursor()
        try:
            cursor.execute(
                """INSERT INTO annotations (id, song_id, ref_id, ann_text,
                verified,cosigned_by, has_voters, state, community, pinned,
                comment_count, votes_total) VALUES (%(id)s, %(song_id)s,
                %(ref_id)s, %(text)s, %(verified)s, %(cosigned_by)s,
                %(has_voters)s, %(state)s, %(community)s, %(pinned)s,
                %(comment_count)s, %(votes_total)s);""", ann
            )
            conn.commit()
            print "Annotation %s added!" % ann['id']
        except Exception, e:
            print e.pgerror


# Add songs to song table
insert_songs(song_info, "test")

# Add new referents to referents table
insert_refs(ref_info, "test")

# Add new annotations to annotations table
insert_annotations(ann_info, "test")
