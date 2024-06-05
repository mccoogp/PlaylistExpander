import numpy as np
import pandas as pd
import random


#Spotify challenge
titles = {}
count = 0
songs = []

playlists = []

#2000 RnB
mainplaylist = [5, 6, 29, 28, 33]

#Smino/vince/isiah
mainplaylist = [6838, 9520, 17877,  19868, 31676, 86455]

#RE
mainplaylist = [86927, 16385, 35783, 60233, 11476, 72626]
import json
for i in range(1000):
    if i % 25 == 0:
        print(i)
    with open(f"spotify_million_playlist_dataset/data/mpd.slice.{1000*i}-{1000*i + 999}.json") as json_file:
        data = json.load(json_file)
    
    for playlist in data["playlists"]:
        current = []
        for track in playlist["tracks"]:
            title = (track["track_name"], track["artist_name"])
            if title not in titles:
                #if  track["artist_name"] == "Billy Joel"  or track["artist_name"] == "Neil Young" :
                    #print(title, count)
                titles[title] = [count, 1]
                count += 1
                songs.append(title)
                current.append(title)
            else:
                titles[title][1] += 1
                current.append(title)
                
        for song in mainplaylist:
            if song < count:
                if songs[song] in current:
                    playlists.append(current)
                    break
        



print("Data Loaded")

sims = np.zeros((len(songs), len(playlists)))

for i in range(len(playlists)):
    for song in playlists[i]:
        sims[titles[song][0], i] = 1


df = pd.DataFrame(sims)

print(df.shape)



def get_item_recommendations(compare_item, df, num_recom):
    recs = []
    print(df.T.shape[0])
    for item in range(df.T.shape[0]):
        if item % 100 == 0:
            print(item)
        if item != compare_item:
            recs.append((np.dot(df.T[compare_item],df.T[item]), item))
    recs.sort(reverse = True)
    final_rec = [recs[i][1] for i in range(num_recom)]
    return final_rec


playlist = mainplaylist
song = playlist[0]



consider = get_item_recommendations(song,df, 1000)


print("First Reccomendations Gotten")


recs = {}
for song in consider:
    recs[song] = 0


for compare_item in playlist:
    for item in consider:
        if item not in playlist:
            adding = np.dot(df.T[compare_item], df.T[item])
            recs[item] += adding
listy = []
for song in recs:
    listy.append((recs[song]/titles[songs[song]][1], song))
listy.sort(reverse = True)
final_rec = [(songs[listy[i][1]], listy[i][0]) for i in range(30)]
for rec in final_rec:
    print(rec)