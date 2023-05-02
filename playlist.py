import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import seaborn as sns
import requests
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail
import base64
import matplotlib.pyplot as plt

load_dotenv()

CLIENT_ID = os.getenv('3ac1b199205442c58e6f3ec71c505aba')
CLIENT_SECRET = os.getenv('8c619b45f9a34623911712f15a1acb52')
SENDGRID_API_KEY = os.getenv("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")
SENDER_EMAIL_ADDRESS = os.getenv("clarekorbs@gmail.com")
BASE_URL = 'https://github.com/ckorbs/cis1051spotify.git'
AUTH_URL = 'http://localhost/'


class SpotifyService():
    def __init__(self):

        self.spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
        auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
            })

        auth_response_data = auth_response.json()

        access_token = auth_response_data['access_token']
        self.headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}


    def get_artist(self, artist):

        result = self.spotify.search(artist)
        artist_uri = result['tracks']['items'][0]['artists'][0]['uri']
        return artist_uri

    def artist_song_recommendations(self, artist_uri): 

        songrecs = []
        recs = self.spotify.recommendations(seed_artists=[artist_uri],limit = 5)
        for track in recs['tracks']:
            songrecs.append((track['name'],"by",track['artists'][0]['name']))
        return songrecs
    

def main():
    service = SpotifyService()
    artist = input("Please enter the name of an artist that you want recomendations: ")
    try:
        artist_uri = service.get_artist(artist)
    except:
        print("Not an artist, try again.")
        sys.exit()
    else:
        select_artist = service.verify_artist(artist_uri)
        correct_artist = input("Is "+select_artist+" the artist you chose? Enter 1 for yes, 0 for no. ")
        if correct_artist == "1":
            service.email_report(artist_uri)
        else:
            print("Please check for typos.")
            sys.exit()

if __name__ == '__main__':
    main()