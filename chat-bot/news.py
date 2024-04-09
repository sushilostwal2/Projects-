


from newsapi import NewsApiClient
import requests
import pandas as pd



key  = "3d578b98072847c9879463e2fe0de3c4"
url="https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey=3d578b98072847c9879463e2fe0de3c4"


def news():
    title=[]
    urla=[]
    url="https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey=3d578b98072847c9879463e2fe0de3c4"
    news=requests.get(url).json()
    article=news["articles"]
    print(news)
    # for i in article:
        # print(i["title"])
        # title.append(i["title"])
        # urla.append(i["url"])


    return pd.DataFrame(title,columns=["Title"])

news()
    
