import requests
import pandas as pd

# Your API key obtained from Google Cloud Console
API_KEY = 'AIzaSyB6yRwnIhjwFkdz_hxchZHCdqYaZWBhVos'

# URL endpoint for the YouTube Data API
API_ENDPOINT = 'https://www.googleapis.com/youtube/v3/'

def search_videos(query, max_results=10):
    """
    Function to search for videos on YouTube based on a query string.
    Returns a list of video items.
    """
    params = {
        'key': API_KEY,
        'q': query,
        'part': 'snippet',
        'type': 'video',
        'maxResults': max_results
    }

    response = requests.get(API_ENDPOINT + 'search', params=params)

    if response.status_code == 200:
        data = response.json()
        videos = data.get('items', [])
        return videos
    else:
        print("Error occurred: ", response.text)
        return None

def main(hobby):
    query = hobby
    max_results =5

    videos = search_videos(query, max_results)
    index=[]
    video_title=[]
    video_url=[]
    

    if videos:
        print("Search Results:")
        
        for idx, video in enumerate(videos, 1):
            title = video['snippet']['title']
            video_id = video['id']['videoId']
#             print(f"{idx}. {title} - https://www.youtube.com/watch?v={video_id}")
            
            index.append(idx)
            video_title.append(title)
            video_url.append(f"https://www.youtube.com/watch?v={video_id}")
            
        df = pd.DataFrame({
            'Index': index,
            'Video Title': video_title,
            'Video URL': video_url})
            
        return df
    else:
        return "No data Found"