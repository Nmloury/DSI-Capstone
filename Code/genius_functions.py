import requests
import pandas as pd


def get_artist_id(name):
    # Get Artist ID from Genius API given an artist name
    page = 1
    url = "http://api.genius.com/search"
    headers = {
         'Authorization': 'Bearer TDQl6lpMfeBg9qMVTx2K4Ni-plHe8-6z5nhRpNk9ApQi2L_qXSoRdYHzD5OhUyvP'}
    while True:
        data = {'q': name,
                'per_page': 20,
                'page': page
                }
        response = requests.get(url, data=data, headers=headers)
        r = response.json()
        hits = r['response']['hits']
        if not hits:
            print 'Artist not Found'
            return None
        for hit in hits:
            artist = hit['result']['primary_artist']['name'].lower()
            artist_id = hit['result']['primary_artist']['id']
            if name.lower() == artist:
                return artist_id
        page += 1


def get_song_info(artist_id):
    # Get song information for a given Artist using their ID
    url = "http://api.genius.com/artists/%s/songs" % str(artist_id)
    headers = {
         'Authorization': 'Bearer 75419_qfE0NU8AnbxK4FHxmf9jbPyiPovUdKrhADkt0YqcEB5yFUeImkVYcSqYQ5'}
    page = 1
    song_info = []
    while True:
        print "Page: ", page
        data = {
            'per_page': 50,
            'page': page
        }
        response = requests.get(url, params=data, headers=headers)
        r = response.json()
        songs = r['response']['songs']
        if not songs:
            print "Finished getting songs for %s" % artist_id
            break
        for song in songs:
            song_dict = {}
            song_dict['id'] = song['id']
            song_dict['hot'] = song['stats']['hot']
            song_dict['unreviewed_annotations'] = song['stats']['unreviewed_annotations']
            song_dict['title'] = song['title']
            song_dict['full_title'] = song['full_title']
            song_dict['artist'] = song['primary_artist']['name']
            song_dict['artist_id'] = song['primary_artist']['id']
            song_dict['annotation_count'] = song['annotation_count']
            song_info.append(song_dict)
        page += 1
    return song_info


def get_ref_ann_info(song_id):
    '''Get referent and annotation information for a given song using its ID'''
    url = "http://api.genius.com/referents"
    headers = {
         'Authorization': 'Bearer TDQl6lpMfeBg9qMVTx2K4Ni-plHe8-6z5nhRpNk9ApQi2L_qXSoRdYHzD5OhUyvP'
         }
    page = 1
    ref_info = []
    ann_info = []
    while True:
        params = {
            'song_id': song_id,
            'per_page': 50,
            'page': page,
            'text_format': 'plain'
        }
        response = requests.get(url, params=params, headers=headers)
        r = response.json()
        refs = r['response']['referents']
        if not refs:
            print "Finished gettting refs and anns for song id: %s" % song_id
            break
        for ref in refs:
            ref_dict = {}
            ref_dict['id'] = ref['id']
            ref_dict['song_id'] = ref['song_id']
            ref_dict['classification'] = ref['classification']
            ref_dict['fragment'] = ref['fragment']
            ref_dict['is_description'] = ref['is_description']
            ref_dict['annotator_id'] = ref['annotator_id']
            ref_info.append(ref_dict)
            for ann in ref['annotations']:
                ann_dict = {}
                ann_dict['id'] = ann['id']
                ann_dict['song_id'] = ref['song_id']
                ann_dict['ref_id'] = ref['id']
                ann_dict['text'] = ann['body']['plain']
                ann_dict['verified'] = ann['verified']
                ann_dict['cosigned_by'] = ann['cosigned_by']
                ann_dict['has_voters'] = ann['has_voters']
                ann_dict['state'] = ann['state']
                ann_dict['community'] = ann['community']
                ann_dict['pinned'] = ann['pinned']
                ann_dict['comment_count'] = ann['comment_count']
                ann_dict['votes_total'] = ann['votes_total']
                ann_info.append(ann_dict)
        page += 1
    return ref_info, ann_info


def get_annotation_info(annotation_id):
    pass
