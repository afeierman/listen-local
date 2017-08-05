import json
import requests
<<<<<<< HEAD
import re
=======
>>>>>>> 6c6309ddf008f7838b4bf5810d8b944c494152d3
import base64
import urllib

import pandas as pd
from flask import Flask, request, redirect, render_template, jsonify
<<<<<<< HEAD

=======
>>>>>>> 6c6309ddf008f7838b4bf5810d8b944c494152d3
import spotipy

from listen_local import *

# Authentication Steps, parameters, and responses are defined at:
<<<<<<< HEAD
#    https://developer.spotify.com/web-api/authorization-guide/
=======
# https://developer.spotify.com/web-api/authorization-guide/
>>>>>>> 6c6309ddf008f7838b4bf5810d8b944c494152d3
# Visit this url to see all the steps, parameters, and expected response.

app = Flask(__name__)

# use a secret key to set our session...?
app.secret_key = 'longsecretkey'

# Concert data, scraped from songkick.com
concerts = pd.read_csv("~/listen-local/app/concerts_clean.csv", index_col=0,
                       encoding='utf-8')
<<<<<<< HEAD
concerts['date'] = pd.to_datetime(concerts['date'], format="%Y/%m/%d")
venues = list(set(concerts['venue']))


=======
concerts['date'] = pd.to_datetime(concerts['date'], format = "%Y/%m/%d")
venues = list(set(concerts['venue']))

>>>>>>> 6c6309ddf008f7838b4bf5810d8b944c494152d3
#  Client Keys

def __get_attribute(prop, project):
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop),
<<<<<<< HEAD
                       open('config.py').read())
    return result.group(1)


CLIENT_ID = __get_attribute('__id__', 'listen-local')
CLIENT_SECRET = __get_attribute('__secret__', 'listen-local')
SONGKICK_API_KEY = __get_attribute('__songkick_key__', 'listen-local')
=======
                       open(project + '/config.py').read())
    return result.group(1)

CLIENT_ID = __get_attribute('__id__', 'listen-local')
CLIENT_SECRET = __get_attribute('__secret_', 'listen-local')
>>>>>>> 6c6309ddf008f7838b4bf5810d8b944c494152d3

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

<<<<<<< HEAD
# Server-side Parameters
# CLIENT_SIDE_URL = "https://afeierman.pythonanywhere.com"
CLIENT_SIDE_URL = "http://127.0.0.1"
# add these lines if you want to run locally
PORT = 8080
REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
# REDIRECT_URI = "{}/callback/q".format(CLIENT_SIDE_URL)
=======

# Server-side Parameters
CLIENT_SIDE_URL = "https://afeierman.pythonanywhere.com"
# add these lines if you want to run locally
# PORT = 8080
# REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
REDIRECT_URI = "{}/callback/q".format(CLIENT_SIDE_URL)
>>>>>>> 6c6309ddf008f7838b4bf5810d8b944c494152d3
SCOPE = "playlist-modify-public playlist-modify-private"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

# Give IDs to Spotipy
SPOTIPY_CLIENT_ID = CLIENT_ID
SPOTIPY_CLIENT_SECRET = CLIENT_SECRET
SPOTIPY_REDIRECT_URI = REDIRECT_URI

<<<<<<< HEAD
=======

>>>>>>> 6c6309ddf008f7838b4bf5810d8b944c494152d3
auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
<<<<<<< HEAD
    "state": STATE,
    "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}


=======
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}

>>>>>>> 6c6309ddf008f7838b4bf5810d8b944c494152d3
@app.route("/")
def index():
    # Auth Step 1: Authorization
    url_args = "&".join(["{}={}".format(
<<<<<<< HEAD
        key, urllib.quote(val)) for key, val in
        auth_query_parameters.iteritems()])
=======
        key,urllib.quote(val)) for key,val in auth_query_parameters.iteritems()])
>>>>>>> 6c6309ddf008f7838b4bf5810d8b944c494152d3
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)


@app.route("/callback/q")
def callback():
    global spotipy_token
    global spotipy_username
    # Auth Step 4: Requests refresh and access tokens
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI
    }
    base64encoded = base64.b64encode("{}:{}".format(CLIENT_ID, CLIENT_SECRET))
    headers = {"Authorization": "Basic {}".format(base64encoded)}
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload,
                                 headers=headers)

    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

<<<<<<< HEAD
    # Auth Step 6: Use the access token to access Spotify API
    authorization_header = {"Authorization": "Bearer {}".format(access_token)}
=======

    # Auth Step 6: Use the access token to access Spotify API
    authorization_header = {"Authorization":"Bearer {}".format(access_token)}
>>>>>>> 6c6309ddf008f7838b4bf5810d8b944c494152d3

    # Get profile data
    user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
    profile_response = requests.get(user_profile_api_endpoint,
                                    headers=authorization_header)
    profile_data = json.loads(profile_response.text)

    # Get user playlist data (currently unused)
    playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
    playlists_response = requests.get(playlist_api_endpoint,
                                      headers=authorization_header)
    playlist_data = json.loads(playlists_response.text)

    # Combine profile and playlist data to display
    display_arr = "You are logged into Spotify as: " + profile_data['id']

    # reluctantly setting global variables for spotipy
    spotipy_token = access_token
    spotipy_username = profile_data['id']

    # return data for the display
    return render_template("index.html", logged_in=display_arr,
<<<<<<< HEAD
                           concerts=concerts, venues=venues)

=======
                           concerts = concerts, venues = venues)
>>>>>>> 6c6309ddf008f7838b4bf5810d8b944c494152d3

@app.route('/create_playlist')
def create_playlist():
    try:
        datefrom = request.args.get('from', 0, type=str)
        datefrom = datefrom.replace("/", "-")
        dateto = request.args.get('to', 0, type=str)
        dateto = dateto.replace("/", "-")
        venue = request.args.get('venue', 0, type=str)
        success_message = "Success! Playlist created. Check Spotify for a " \
<<<<<<< HEAD
                          "playlist called: {} to {} at {}".format(
            datefrom, dateto, venue)
        run_listen_local(venue, start_date=datefrom, end_date=dateto)
=======
                          "playlist called: " + datefrom + " to " + dateto + \
                          " at " + venue
        run_listen_local(venue, start_date = datefrom, end_date = dateto)
>>>>>>> 6c6309ddf008f7838b4bf5810d8b944c494152d3
        return jsonify(result=success_message)
    except Exception as e:
        return jsonify(result="Uh oh, something went wrong. Did you fill in "
                              "the date range and select a venue?" +
                              "\n Error: " + str(e))


# create_venue_songlist_ids returns a tuple with the playlist title,
# and a list of Spotify song IDs
# main function below (this is what the webapp calls)

<<<<<<< HEAD
def run_listen_local(venue, start_date="2017-08-01",
                     end_date="2017-12-31", tracks=5):
    global spotipy_token
    global spotipy_username

    playlist_prep = SpotifyPlaylistMaker(songkick_api_key,
                                         start_date=start_date,
                                         end_date=end_date,
                                         tracks_to_retrieve=tracks)
=======
def run_listen_local(venue, start_date = "2017-06-15",
                     end_date = "2017-12-31", tracks = 5):
    global spotipy_token
    global spotipy_username

    playlist_prep = SpotifyPlaylistMaker(start_date = start_date,
                                            end_date = end_date,
                                         tracks_to_retrieve = tracks)
>>>>>>> 6c6309ddf008f7838b4bf5810d8b944c494152d3

    playlist_prepped = playlist_prep.create_venue_songlist_ids(venue)
    playlist_title = playlist_prepped[0]
    track_ids = playlist_prepped[1]

    if SPOTIPY_CLIENT_ID:
        sp = spotipy.Spotify(auth=SPOTIPY_CLIENT_SECRET)
<<<<<<< HEAD
        sp.trace = False  # This can be set to True to help with debugging
=======
        sp.trace = False #This can be set to True to help with debugging
>>>>>>> 6c6309ddf008f7838b4bf5810d8b944c494152d3
        sp.user_playlist_create(spotipy_username, playlist_title)
        playlists = sp.user_playlists(spotipy_username)
        for playlist in playlists['items']:
            if playlist['name'] == playlist_title:
                playlist_id = playlist['id']
                break
        results = sp.user_playlist_add_tracks(spotipy_username,
                                              playlist_id, track_ids)
        print("Playlist created! %s") % (results)
    else:
        print("Authentication failed. Can't get token.")

<<<<<<< HEAD

if __name__ == "__main__":
    app.run(debug=True, port=PORT)
=======
if __name__ == "__main__":
    app.run(debug=False,port=PORT)
>>>>>>> 6c6309ddf008f7838b4bf5810d8b944c494152d3
