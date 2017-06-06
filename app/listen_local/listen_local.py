import pandas as pd
import spotipy

def get_venue_artists(venue, start_date = "2017-01-01", end_date = "2017-12-31"):
    concert_dates = pd.date_range(start = start_date, end = end_date, freq = 'D')
    artists = []
    for show in concerts.loc[concerts['venue'] == venue, ['date', 'artist']].itertuples():
        if show[1] in concert_dates:
            artists.append(show)
    return set(artists)

def get_artist_ids(artists):
    sp = spotipy.Spotify()
    artist_plus_ids = []
    for artist in artists:
        search = sp.search(q=artist, type = 'artist', limit = 1)
        try:
            artist_plus_ids.append((search['artists']['items'][0]['name'],  search['artists']['items'][0]['id']))
        except IndexError:
            pass
    return set(artist_plus_ids)

def get_venue_artist_ids(venue, start_date = "2017-01-01", end_date = "2017-12-31"):
    sp = spotipy.Spotify()
    artists = get_venue_artists(venue, start_date, end_date)
    artist_plus_ids = []
    for artist in artists:
        search = sp.search(q=artist[2], type = 'artist', limit = 1)
        try:
            artist_plus_ids.append((search['artists']['items'][0]['name'] ,  search['artists']['items'][0]['id']))
        except IndexError:
            pass
    return set(artist_plus_ids)

def create_venue_songlist(venue, start_date = "2017-01-01", end_date = "2017-12-31"):
    sp = spotipy.Spotify()
    songlist = []
    num_tracks = 5
    if (start_date == "2017-01-01") and (end_date == "2017-12-31"):
        num_tracks = 3
    for artist in get_venue_artist_ids(venue, start_date, end_date):
        artist_tracks = sp.artist_top_tracks(artist[1])['tracks']
        if len(artist_tracks) >= num_tracks:
            for track in range(0, num_tracks):
                songlist.append((artist_tracks[track]['name'], artist_tracks[track]['id']))
    return songlist

def prepare_song_id_list(songlist):
    song_ids = []
    for song in songlist:
        song_ids.append(str(song[1]))
    return song_ids

def create_venue_songlist_ids(venue, start_date = "2017-01-01", end_date = "2017-12-31"):
    songlist = create_venue_songlist(venue, start_date, end_date)
    #the max length for playlists created via the spotify API is 100 songs, so truncate the song list if it's too long
    if len(songlist) >= 100:
        songlist = songlist[0:99]
    ptitle = ("%s from %s to %s") % (venue, start_date, end_date)
    return (ptitle, prepare_song_id_list(songlist))