"""
Copyright (C) 2020 Patrick Maloney

"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def search_youtube(search_term):
    # format search term into youtube search url
    formatted_search_term = ''
    search_url = 'https://www.youtube.com/results?search_query='

    for char in search_term:
        if char.isspace():
            formatted_search_term += ('+')
        else:
            formatted_search_term += (char)

    search_url += formatted_search_term

    # retrive video thumbnail, url, and title
    text = requests.get(search_url).text
    soup = BeautifulSoup(text,features="lxml")
    divs = [div for div in soup.find_all('div') if div.has_attr('class') and 'yt-lockup-dismissable' in div['class']]
    try:
        thumbnail_src = divs[0].find_all('img')[0]['src']
    except IndexError:
        thumbnail_src = None
    link_lst = [x for x in divs[0].find_all('a') if x.has_attr('title')]
    video_url = 'https://youtu.be/' + link_lst[0]['href'][9::]
    video_title = link_lst[0]['title']
    return(thumbnail_src,video_url,video_title)
