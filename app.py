import streamlit as st
import numpy as np

import scrapetube
from py_youtube import Data
import pandas as pd
import re


def videoList(type, id, limit=20):
    if type=='playlist':
        videos = [video['videoId'] for video in scrapetube.get_playlist(id)]
    elif type=='channel':
        videos = [video['videoId'] for video in scrapetube.get_channel(id)]
    else:
        videos = [video['videoId'] for video in scrapetube.get_search(id, limit, 1, 'relevance', 'video')]
    
    print(len(videos))
    return videos


def getDataset(query, videos, language='English'):
    video_info = []
    for video in videos:
        link = f'https://youtu.be/{video}'
        data = Data(link).data()

        if language=="English":
            srt = f'yttool --language en --subtitles {video}' #English playlist
        else:
            srt = f'yttool --language asr --subtitles {video}' # for CampusX
        # srt = f'yttool --subtitles {video}' #https://github.com/nlitsme/youtube_tool/


        sbttl = {srt}
        subtitle = " ".join(sbttl)
        word_count = len(subtitle.split())

        video_info.append({
            'id': data['id'],
            'title': data['title'],
            'views': data['views'],
            'likes': data['likes'],
            'thumbnails': data['thumbnails'],
            'publishdate': data['publishdate'],
            'channel_name': data['channel_name'],
            'subscriber': data['subscriber'],
            'category': data['category'],
            'subtitle': subtitle,
            'WordCount': word_count
        })

    finalDF = pd.DataFrame(video_info, columns=['id', 'title', 'views', 'likes', 'thumbnails', 'publishdate', 'channel_name', 'subscriber', 'category', 'subtitle', 'WordCount'])
    finalDF['views'] = finalDF['views'].astype(float)
    finalDF.to_csv(f'{query}.csv', index=False)
    return finalDF

videos = videoList('channel','UCnXs-Nq1dzMZQOKUHKW3rdw') # type = playlist/channel/search # id=id/query
dataset = getDataset('Bioinformagician', videos, language='English')
dataset

title = st.text_input('Title',"Default Text")
st.write('The current movie title is', title)
title
print(title)