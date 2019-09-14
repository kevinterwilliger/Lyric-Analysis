import spotipy
import spotipy.util as util
import json
import pandas as pd
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
    

def get_analysis(search) :
    for item in search["tracks"]["items"] :
        if closeEnough(item['artists'][0]["name"].lower(),artist) :
            audio = sp.audio_analysis(item["id"])
            track = audio['track']
            loudness =

            # for key in audio.keys() :
            #     if type(audio[key]) is type(dict()) :
            #         print(audio[key].keys())
            #     else:
            #         print(audio[key][0])
        else:
            print(item['artists'][0]['name'])
        break
    return l,t,k,m,time

with open("secrets.json",'r') as f:
    s = json.load(f)

token = util.oauth2.SpotifyClientCredentials(client_id=s["Spotify ID"], client_secret=s["Spotify Secret"])

cache_token = token.get_access_token()
sp = spotipy.Spotify(cache_token)

data = pd.read_csv("Report1/data_clean.csv")

for i in range(0,len(data)) :
    song = data.loc[i,"Song"]
    artist = data.loc[i,"Artist"]
    q = song + " " + artist
    print("Searching for " + q)
    search = sp.search(q,limit=10, offset=0, type='track', market=None)

    break
