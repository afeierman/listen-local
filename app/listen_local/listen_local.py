import requests
import pandas as pd
import spotipy

class SpotifyPlaylistMaker:
    def __init__(self, songkick_api_key, start_date="2017-01-01", end_date="2017-12-31",
                 tracks_to_retrieve=5):
        self.start_date = start_date
        self.end_date = end_date
        self.tracks_to_retrieve = tracks_to_retrieve
        self.songkick_api_key = songkick_api_key


    def get_songkick_url(self, endpoint):
        """Points the request to the Songkick API."""
        return requests.get('http://api.songkick.com/api/3.0/{}&apikey={}'
                            .format(endpoint, self.songkick_api_key))

    def get_songkick_venue_id(self, venue_query):
        """Gets a venue_id based on a text query using the Songkick API."""
        return self.get_songkick_url("search/venues.json?query={}".format(venue_query))

    def get_venue_artists(self, venue):
        concert_dates = pd.date_range(start=self.start_date, end=self.end_date,
                                      freq='D')

    def __init__(self, start_date = "2017-01-01", end_date = "2017-12-31",
                 tracks_to_retrieve = 5):
        self.start_date = start_date
        self.end_date = end_date
        self.tracks_to_retrieve = tracks_to_retrieve

    def get_venue_artists(self, venue):
        concert_dates = pd.date_range(start = self.start_date, end = self.end_date, freq = 'D')
        artists = []
        for show in concerts.loc[concerts['venue'] == venue, ['date', 'artist']].itertuples():
            if show[1] in concert_dates:
                artists.append(show)
        return set(artists)

    def get_artist_ids(self, artists):
        sp = spotipy.Spotify()
        artist_plus_ids = []
        for artist in artists:
            search = sp.search(q=artist, type = 'artist', limit = 1)
            try:
                artist_plus_ids.append((search['artists']['items'][0]['name'],  search['artists']['items'][0]['id']))
            except IndexError:
                pass
        return set(artist_plus_ids)

    def get_venue_artist_ids(self, venue):
        sp = spotipy.Spotify()
        artists = get_venue_artists(venue, self.start_date, self.end_date)
        artist_plus_ids = []
        for artist in artists:
            search = sp.search(q=artist[2], type = 'artist', limit = 1)
            try:
                artist_plus_ids.append((search['artists']['items'][0]['name'] ,  search['artists']['items'][0]['id']))
            except IndexError:
                pass
        return set(artist_plus_ids)

    def create_venue_songlist(self, venue):
        sp = spotipy.Spotify()
        songlist = []
        if (self.start_date == "2017-01-01") and (self.end_date == "2017-12-31"):
            self.tracks_to_retrieve = 3
        for artist in get_venue_artist_ids(venue):
            artist_tracks = sp.artist_top_tracks(artist[1])['tracks']
            if len(artist_tracks) >= self.tracks_to_retrieve:
                for track in range(0, self.tracks_to_retrieve):
                    songlist.append((artist_tracks[track]['name'],
                                     artist_tracks[track]['id']))
                    songlist.append((artist_tracks[track]['name'], artist_tracks[track]['id']))
        return songlist

    def prepare_song_id_list(self, songlist):
        song_ids = []
        for song in songlist:
            song_ids.append(str(song[1]))
        return song_ids

    def create_venue_songlist_ids(self, venue):
        songlist = create_venue_songlist(venue, self.start_date, self.end_date)
        #the max length for playlists created via the spotify API is 100 songs, so truncate the song list if it's too long
        if len(songlist) >= 100:
            songlist = songlist[0:99]
        ptitle = ("%s from %s to %s") % (venue, self.start_date, self.end_date)
        return (ptitle, prepare_song_id_list(songlist))