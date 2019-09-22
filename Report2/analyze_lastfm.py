import pylast
import sys
import time
import json
import pandas as pd

def lastfm_connect() :
    with open("secrets.json",'r') as f:
        s = json.load(f)
    network = pylast.LastFMNetwork(api_key=s["Last.FM key"], api_secret=s["Last.FM secret"])
    return network

def get_genres(data) :
    conn = lastfm_connect()
    tag1 = []
    tag2 = []
    tag3 = []
    tag4 = []
    tag5 = []
    l = [tag1,tag2,tag3,tag4,tag5]

    for i in range(0,len(data)) :
        try:
            song = data.loc[i,"Song"]
            artist = data.loc[i,"Artist"]
            q = song + " " + artist

            print("searching for " + q)
            ret = get_tags(artist,song,conn)
            for i in range(0,4) :
                l[i].append(ret[i])
        except Exception as e:
            print(e)
            for i in range(0,4) :
                l[i].append(9999)
    return tag1,tag2,tag3,tag4,tag5

def get_tags(artist,song,conn) :
    search = conn.get_track(artist=artist,title=song)

    tags = search.get_top_tags()
    l = [9999,9999,9999,9999,9999]

    if len(tags) >= 5 :
        r = 5
    else :
        r = len(tags)

    for j in range(0,r) :
        l[j] = tags[j].item.name
        
    return l

data = pd.read_csv("../Report1/data_clean.csv")

tag1,tag2,tag3,tag4,tag5 = get_genres(data)
# print(tag1)

columns = pd.DataFrame({
                'Tag1' : tag1,
                'Tag2' : tag2,
                'Tag3' : tag3,
                'Tag4' : tag4,
                'Tag5' : tag5
                # 'ids' : ids,
                # 'Genre' : g
})
songs = data["Song"]
data_genres = pd.concat([songs,columns],axis=1,ignore_index=False)

data_genres.to_csv("genres.csv")

check = pd.read_csv("genres.csv")
for col in data.columns :
    print(col)
