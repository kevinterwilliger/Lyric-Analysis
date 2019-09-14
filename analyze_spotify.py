import spotipy
import spotipy.util as util
import json
import pandas as pd
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

'''
This retrieves the audio analysis from the spotify search and
returns the loudness, tempo, key, mode, and time signature.
Fills values where there is a problem with 9999
'''
def get_search(search,artist,sp) :
    if len(search['tracks']['items']) is not 0 :
        for item in search["tracks"]["items"] :
            if similar(item['artists'][0]["name"].lower(),artist) > .75 :
                try :
                    audio = sp.audio_analysis(item["id"])
                except :
                    l = 9999
                    t = 9999
                    k = 9999
                    m = 9999
                    time = 9999
                    break
                sections = audio["sections"][0]
                l = sections["loudness"]
                t = sections["tempo"]
                k = sections["key"]
                m = sections["mode"]
                time = sections["time_signature"]
                # print(artist + " Spotify:  " + item["artists"][0]['name'].lower())
            else :
                l = 9999
                t = 9999
                k = 9999
                m = 9999
                time = 9999
            break
    else :
        l = 9999
        t = 9999
        k = 9999
        m = 9999
        time = 9999
    return l,t,k,m,time

'''
This gets the wanted columns by calling get_search.
Loops through songs in dataframe and
'''
def get_analysis(data) :
    loudness = []
    tempo = []
    key = []
    mode = []

    with open("secrets.json",'r') as f:
        s = json.load(f)

    token = util.oauth2.SpotifyClientCredentials(client_id=s["Spotify ID"], client_secret=s["Spotify Secret"])

    cache_token = token.get_access_token()
    sp = spotipy.Spotify(cache_token)

    time_signature = []
    for i in range(0,len(data)) :
        song = data.loc[i,"Song"]
        artist = data.loc[i,"Artist"]
        q = song + " " + artist
        print("Searching for " + q)
        try :
            search = sp.search(q,limit=10, offset=0, type='track', market=None)
            l,t,k,m,time = get_search(search,artist,sp)
        except :
            l = 9999
            t = 9999
            k = 9999
            m = 9999
            time = 9999
        loudness.append(l)
        tempo.append(t)
        key.append(k)
        mode.append(m)
        time_signature.append(time)

        # if i > 1 : return loudness,tempo,key,mode,time_signature
    return loudness,tempo,key,mode,time_signature
#
# data = pd.read_csv("Report1/data_clean.csv")
# l,t,k,m,time = get_analysis(data)
# columns = pd.DataFrame({
#                 'Loudness' : l,
#                 'Tempo' : t,
#                 'Key' : k,
#                 'Mode' : m,
#                 'time_signature' : time
# })
# data_new = pd.concat([data,columns],axis=1,ignore_index=True)
# data_new.to_csv("Data_new_new.csv")
print(similar("sam same and the profets","sam same & the profets"))
