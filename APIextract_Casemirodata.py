from googleapiclient.discovery import build
from datetime import datetime
import pandas as pd


key = '<key>'
playlistId = 'PLenV7kDuAhQk5esWz_WqierzPqZMbySCQ'
maxvideos = 41
nextPage_token= None


youtube= build('youtube','v3', developerKey=key)

playlistvideos = []

while True:
  res = youtube.playlistItems().list(part='snippet', playlistId = playlistId, maxResults = maxvideos).execute()
  playlistvideos += res['items']

  nextPage_token = res.get('nestPageToken')

  if nextPage_token is None:
    break


videos_ids = list(map(lambda x: x['snippet']['resourceId']['videoId'],playlistvideos))

stats = []
for video in videos_ids:
  res = youtube.videos().list(part='statistics',id= video).execute()
  stats += res['items']


stats_ViewCount = list(map(lambda x: x['statistics']['viewCount'],stats))
stats_likeCount = list(map(lambda x: x['statistics']['likeCount'],stats))
stats_favoriteCount = list(map(lambda x: x['statistics']['favoriteCount'],stats))
stats_commentCount = list(map(lambda x: x['statistics']['commentCount'],stats))

videos_date = list(map(lambda x: x['snippet']['publishedAt'],playlistvideos))
videos_title = list(map(lambda x: x['snippet']['title'],playlistvideos))
videos_description = list(map(lambda x: x['snippet']['description'],playlistvideos))
videos_thumbnails = list(map(lambda x: x['snippet']['thumbnails'],playlistvideos))

extraction_date = [str(datetime.now())]*len(videos_ids)


playlist_df = pd.DataFrame({
    'title':videos_title,
    'videos_id':videos_ids,
    'video_description': videos_description,
    'videos_thumbnails': videos_thumbnails,
    'stats_ViewCount' : stats_ViewCount,
    'stats_likeCount': stats_likeCount,
    'stats_favoriteCount': stats_favoriteCount,
    'stats_commentCount': stats_commentCount
})

print(playlist_df)

playlist_df.to_csv("C:\\Users\\User\\Python_projects\\youtube_pipeline\\casemiro_playlistPegadinhas.csv")


