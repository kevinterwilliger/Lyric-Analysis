import spotipy
import spotipy.util as util
import json
import pandas as pd
from difflib import SequenceMatcher
from time import sleep

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def spotify_connect() :
    with open("secrets.json",'r') as f:
        s = json.load(f)
    token = util.oauth2.SpotifyClientCredentials(client_id=s["Spotify ID"], client_secret=s["Spotify Secret"])
    cache_token = token.get_access_token()
    return spotipy.Spotify(cache_token)


'''
This retrieves the audio analysis from the spotify search and
returns the loudness, tempo, key, mode, and time signature.
Fills values where there is a problem with 9999
'''
def get_search(search,artist,sp) :
    if len(search['tracks']['items']) is not 0 :
        for item in search["tracks"]["items"] :
            if similar(item['artists'][0]["name"].lower(),artist) > .75 :
                # id = search["tracks"]["items"][0]["artists"]#["id"]
                # print(id)
                # try :
                #     id = search["tracks"]["items"][0]["artists"][0]["id"]
                #     # print(id)
                #     artist = sp.artist(artist_id=id)
                #     # with open("temp.txt",'w') as f:
                #     #     json.dump(artist,f)
                #
                #     if len(artist["genres"]) is 0:
                #         g = 9999
                #     else:
                #         g = artist['genres'][0]
                # except Exception as e:
                #     print("error in genre")
                #     check(e)
                #     l = 9999
                #     t = 9999
                #     k = 9999
                #     m = 9999
                #     time = 9999
                #     # g = 9999
                #     # id = 9999
                #     break
                try :
                    audio = sp.audio_analysis(item["id"])
                except Exception as e:
                    print("error in audio analysis")
                    check(e)
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
                return l,t,k,m,time
    else :
        print("Return is length 0, appending junk values")
        l = 9999
        t = 9999
        k = 9999
        m = 9999
        time = 9999
        # id = 9999
        # g = 9999
        return l,t,k,m,time

'''
This gets the wanted columns by calling get_search.
Loops through songs in dataframe and returns columns
'''
def get_analysis(data) :
    sp = spotify_connect()

    loudness = []
    tempo = []
    key = []
    mode = []
    time_signature = []
    # genre = []
    # ids = []

    for i in range(0,len(data)) :
        if i % 500 == 0 and i is not 0 :
            print("Sleeping")
            sleep(300)
        l = 9999
        t = 9999
        k = 9999
        m = 9999
        time = 9999
        flag = True

        song = data.loc[i,"Song"]
        artist = data.loc[i,"Artist"]
        q = song + " " + artist
        print("Searching for " + q)
        try :
            search = sp.search(q,limit=3, offset=0, type='track', market="US")
        except Exception as e:
            print("error in sp.search")
            check(e)
            l = 9999
            t = 9999
            k = 9999
            m = 9999
            time = 9999
            # g = 9999
            # id = 9999
            flag = False
        if flag:
            try :
                l,t,k,m,time = get_search(search,artist,sp)
            except Exception as e:
                print("error in get_search")
                check(e)
                l = 9999
                t = 9999
                k = 9999
                m = 9999
                time = 9999
                # g = 9999
                # id = 9999
        loudness.append(l)
        tempo.append(t)
        key.append(k)
        mode.append(m)
        time_signature.append(time)
        # genre.append(g)
        # ids.append(id)

    return loudness,tempo,key,mode,time_signature

def check(exception) :
    try:
        print(e)
        print(type(e))
    except:
        print("did not work")
    try:
        print(e.keys())
    except:
        print("oof")

data = pd.read_csv("../Report1/data_clean.csv")
# thefacththatihavetodothis(data)

l,t,k,m,time = get_analysis(data)
# print(g)
columns = pd.DataFrame({
                'Loudness' : l,
                'Tempo' : t,
                'Key' : k,
                'Mode' : m,
                'time_signature' : time
                # 'ids' : ids,
                # 'Genre' : g
})

data_new = pd.concat([data,columns],axis=1,ignore_index=False)
data_new.to_csv("Data_new_new.csv")

data = pd.read_csv("Data_new_new.csv")
for col in data.columns :
    print(col)
