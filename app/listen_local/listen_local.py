import requests
import pandas as pd
import spotipy

class SongkickClient:
    def __init__(self, songkick_api_key, venue_query):
        self.api_key = songkick_api_key
        self.venue_query = venue_query

    def _handle_songkick_response(self, endpoint):
        response = requests.get(self._get_songkick_url(endpoint))
        if response.raise_for_status():
            return response.raise_for_status()
        else:
            return response.json()

    def _get_songkick_url(self, endpoint):
        """Points the request to the Songkick API."""
        return 'http://api.songkick.com/api/3.0/{}&apikey={}'\
            .format(endpoint, self.api_key)

    def get_venue_query(self):
        """Gets a venue_id based on a text query using the Songkick API."""
        response = self._handle_songkick_response("search/venues.json?query={}"
                                                  .format(self.venue_query))
        if not response['resultsPage']['results']:
            raise ValueError('No venue found with those search terms.')
        return response

    def get_venue_ids(self, venues_to_return=1):
        venue_ids = []
        venue_query_response = self._handle_songkick_response(
            "search/venues.json?query={}".format(self.venue_query))
        for venue_index in range(venues_to_return):
            venue_ids.append(venue_query_response['resultsPage']['results']['venue'][venue_index]['id'])
        return venue_ids

    def get_venue_concerts(self, venue_id):
        venue_concerts = []
        page = 1
        get_more_concerts = True
        while get_more_concerts:
            venue_concerts_response = self._handle_songkick_response(
            'venues/{}/calendar.json?page={}'.format(venue_id, page))
            if not venue_concerts_response['resultsPage']['results']:
                get_more_concerts = False
            else:
                venue_concerts.append(venue_concerts_response['resultsPage']['results']['event'])
                page += 1
        # Fancy list comp returns a list of concerts from the paginated JSON
        return [concerts for concerts_list in venue_concerts for concerts in concerts_list]

    def get_venue_concerts_from_query(self):
        """Provide a search query for a venue and get a list of concerts
        at the first result of the search query."""
        return self.get_venue_concerts(self.get_venue_ids()[0])


class SpotifyPlaylistMaker:
    def __init__(self, concert_json, venue,
                 token,
                 start_date="2017-01-01", end_date="2017-12-31",
                 tracks_to_retrieve=5):
        self.start_date = start_date
        self.end_date = end_date
        self.tracks_to_retrieve = tracks_to_retrieve
        self.venue = venue
        self.concerts = concert_json
        self.artists = self.get_venue_artists()
        self.token = token

    def get_venue_artists(self):
        concert_dates = pd.date_range(start=self.start_date,
                                      end=self.end_date, freq='D')
        artists = []
        for show in self.concerts:
            if show['start']['date'] in concert_dates:
                for unique_artist in show['performance']:
                    artists.append(unique_artist['artist']['displayName'])
        return set(artists)

    def get_artist_ids(self):
        sp = spotipy.Spotify(auth=self.token)
        artist_plus_ids = []
        for artist in self.artists:
            search = sp.search(q=artist, type='artist', limit=1)
            try:
                artist_plus_ids.append((search['artists']['items'][0]['name'],
                                        search['artists']['items'][0]['id']))
            except IndexError:
                pass
        return set(artist_plus_ids)

    def get_venue_artist_ids(self):
        sp = spotipy.Spotify(auth=self.token)
        artist_plus_ids = []
        for artist in self.artists:
            search = sp.search(q=artist[2], type='artist', limit=1)
            try:
                artist_plus_ids.append((search['artists']['items'][0]['name'],
                                        search['artists']['items'][0]['id']))
            except IndexError:
                pass
        return set(artist_plus_ids)

    def create_venue_songlist(self):
        sp = spotipy.Spotify(auth=self.token)
        songlist = []
        for artist in self.get_venue_artist_ids():
            artist_tracks = sp.artist_top_tracks(artist[1])['tracks']
            if len(artist_tracks) >= self.tracks_to_retrieve:
                for track in range(0, self.tracks_to_retrieve):
                    songlist.append((artist_tracks[track]['name'],
                                     artist_tracks[track]['id']))
                    songlist.append((artist_tracks[track]['name'],
                                     artist_tracks[track]['id']))
        return songlist

    def create_venue_songlist_ids(self):
        songlist = self.create_venue_songlist()
        # the max length for playlists created via the Spotify API
        # is 100 songs; truncate the song list if it's too long
        songlist = songlist[0:99]
        ptitle = ("%s from %s to %s") % (self.venue, self.start_date, self.end_date)
        return (ptitle, [str(song[1]) for song in songlist])