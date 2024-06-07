import numpy as np
import pandas as pd
import random


#Titles is a dictionary going from a tuple of (title, artist) to a list of [the track number id, the number of playlists that song appears in]
titles = {}

#Count increases by 1 for every new song that appears
count = 0

#Songs is just a list of every song title
songs = []

#list of every playlist
playlists = []

#2000 RnB
mainplaylist = [5, 6, 29, 28, 33]

#Smino/vince/isiah
mainplaylist = [6838, 9520, 17877,  19868, 31676, 86455]

#RE
mainplaylist = [86927, 16385, 35783, 60233, 11476, 72626]
import json

#The million playlists is plit into 1000 files of 1000 playlists
for i in range(1000):
    #Just to keep track of how long it is taking
    if i % 25 == 0:
        print(i)
        
    #opening a file with 1000 playlists
    with open(f"spotify_million_playlist_dataset/data/mpd.slice.{1000*i}-{1000*i + 999}.json") as json_file:
        data = json.load(json_file)
    
    #Goes through each playlist
    for playlist in data["playlists"]:
        current = []
        #This for loop just goes through each track in the playlist and adds the track to titles dictionary and songs list if it is the first time this song appeared. If this is the second time the song appeared it just edits the frequency of the song in the titles dictionary.
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
        #Only adds playlsit to playlists list if at least one song from the main playlsit is on the playlist   
        for song in mainplaylist:
            if song < count:
                if songs[song] in current:
                    playlists.append(current)
                    break
        


#Keeping track of progress
print("Data Loaded")


#Builds a pivot table matrix
sims = np.zeros((len(songs), len(playlists)))
for i in range(len(playlists)):
    for song in playlists[i]:
        sims[titles[song][0], i] = 1

#Turns matrix into panda
df = pd.DataFrame(sims)

#Keeping track of progress
print(df.shape)


#This function takes in an item to compare, the dataframe, and the number of reccomendations you want to return and returns the most similar songs
def get_item_recommendations(compare_item, df, num_recom):
    recs = []
    #Keeping track of progress
    print(df.T.shape[0])
    #going through every song
    for item in range(df.T.shape[0]):
        #keeping track of progress
        if item % 100 == 0:
            print(item)
        if item != compare_item:
            #for every song that is not the test song adds its dot product to the recs list
            recs.append((np.dot(df.T[compare_item],df.T[item]), item))
    #sorts the reccomendation from highest score to lowest score
    recs.sort(reverse = True)
    #finds and returns the num_recom best songs
    final_rec = [recs[i][1] for i in range(num_recom)]
    return final_rec


playlist = mainplaylist
song = playlist[0]


#Gets the 100 most similar tracks to the first track and only considers those tracks in the future in order to minimize runtime
consider = get_item_recommendations(song,df, 1000)

#keeping track of progress
print("First Reccomendations Gotten")

#Creates a dictionary with each song still considering equal to 0
recs = {}
for song in consider:
    recs[song] = 0

#looks at every song in the main playlist and gets its dot product with every song in the 
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
