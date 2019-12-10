import pylast
import sys
import time
import json
import pandas as pd

def lastfm_connect() :
    with open("secrets.json",'r') as f:
        s = json.load(f)
    network = pylast.LastFMNetwork(api_key=s["Last.FM key"],
                                   api_secret=s["Last.FM secret"])
    return network


'''
Returns list of 5 top user tags from Last_FM API for each song in dataset
'''
def get_genres(data) :
    conn = lastfm_connect()
    l = [[],[],[],[],[],[]]

    for i in range(0,len(data)) :
        try:
            song = data.loc[i,"Song"]
            artist = data.loc[i,"Artist"]
            q = song + " " + artist

            print("searching for " + q)
            tags = get_tags(artist,song,conn)
            for i in range(0,len(l)) :
                try:
                    l[i].append(tags[i])
                except:
                    l[i].append(9999)
        except pylast.WSError as e:
            print("line 33")
            for i in range(0,len(l)) :
                l[i].append(9999)
            continue
    return l

def get_tags(artist,song,conn) :
    l = [9999,9999,9999,9999,9999]
    try:
        search = conn.get_track(artist=artist,title=song)
    except pylast.WSError as e:
        print("line 46")
        return l
    except Exception as e:
        print("line 49")
        return l
    tags = search.get_top_tags()

    if len(tags) >= 5 :
        r = 5
    else :
        r = len(tags)

    for j in range(0,r) :
        l[j] = tags[j].item.name

    return l

# data = pd.read_csv("../Report1/data_clean.csv")
#
# l = get_genres(data)
# # print(tag1)
# print(
# str(len(l[0])) +
# " || " +
# str(len(l[1])) +
# " || " +
# str(len(l[2])) +
# " || " +
# str(len(l[3]))
# )
#
#
#
# columns = pd.DataFrame({
#                 'Tag1' : l[0],
#                 'Tag2' : l[1],
#                 'Tag3' : l[2],
#                 'Tag4' : l[3],
#                 'Tag5' : l[4]
#                 # 'ids' : ids,
#                 # 'Genre' : g
# })
# songs = data["Song"]
# data_genres = pd.concat([songs,columns],axis=1,ignore_index=False)
#
# data_genres.to_csv("genres.csv")

check = pd.read_csv("genres.csv")
for col in check.columns :
    print(col)
