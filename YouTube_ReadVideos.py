####!/usr/bin/env python3 
#CODE BELOW:
#GETS VIDEOS LIST FROM A SPECIFIC YOUTUBE CHANNEL USING apiclient.discovery AND GOOGLE YOUTUBE API KEY
#GETS TRANSCRIPTS OF THE VIDEOS USING YouTubeTranscriptApi, AVAILABLE IN PIP
#GETS RID OF NON-SPEECH SOUNDS AND TIMESTAMPS THAT ARE SPIT OUT FROM YouTubeTranscriptApi
#CREATES A LIST AND PICKLES IT OUT



from youtube_transcript_api import YouTubeTranscriptApi
import re
import csv
import pickle
import pandas as pd

#KEY ACCESS SECTIONS:
from apiclient.discovery import build
API_Key="YOUR_KEY"
youtube= build('youtube', 'v3', developerKey= API_Key)
type(youtube)

#GETS CHANNEL'S ID FROM CHANNEL'S NAME
def get_channel(channel_name):
    return youtube.search().list(q=channel_name, type='channel', part='id,snippet').execute()['items'][0]

#GETS VIDEOS LIST IN A CHANNEL 
def get_videos(channel_id, part='id,snippet', limit=10):
    res = youtube.channels().list(id=channel_id, 
                                  part='contentDetails').execute()
    playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']    
    videos = []
    next_page_token = None   
    while 1:
        res = youtube.playlistItems().list(playlistId=playlist_id, 
                                           part=part, 
                                           maxResults=min(limit, 50),
                                           pageToken=next_page_token).execute()
        videos += res['items']
        next_page_token = res.get('nextPageToken')      
        if next_page_token is None or len(videos) >= limit:
            break
    return videos




channel_name='astrophysics for kids'
channel_id = get_channel(channel_name)['id']['channelId']

videos = get_videos(channel_id, limit=500) #VIDEOS FROM NEWEST TO OLDEST!!!

#This lists the videos IDs
video_ids= list(map(lambda x:x['snippet']['resourceId']['videoId'], videos))

words=[]
transcriptsmultiple={}
for video_idx in video_ids:
    transcript= YouTubeTranscriptApi.get_transcript(video_idx)
    list1 = [t['text'] for t in transcript]
    my_list=[]
    for item in list1:  
        if item.find('[')==-1:
            my_list.append(item) 
            longlist=' '.join(map(str, my_list))
    transcriptsmultiple[video_idx]=longlist
    pickle.dump(transcriptsmultiple, open(channel_name+"_released.pickle", "wb"))
  
