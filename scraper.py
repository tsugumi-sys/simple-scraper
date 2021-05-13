import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import numpy as np
import time

def find_ameblo_post_url(item: str):
    result = re.findall('^https://ameblo.jp/.+/entry-.+\.html$', item)
    if result:
        return result[0]
    else:
        return None
    
# Parameter
# ==================
# search_query: list
def scrape_ameba_blog(search_query=None):
    if search_query:
        kwds = search_query
    else:
        kwds = ["行政書士", "民事信託", "相続"]
    
    base_urls = []
    for kwd in kwds:
        for i in range(1, 3):
            for j in range(1, 3):
                base_urls.append(f'https://search.ameba.jp/search/entry/{kwd}.html?p={i}&sortField={j}')
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    urls = []
    
    # Get News URL
    for base_url in base_urls:
        res = requests.get(base_url, headers)
        if res.status_code == 200:
            soup = bs(res.content, 'html.parser')
            for item in soup.find_all('a'):
                news_url = find_ameblo_post_url(str(item.get('href')))
                if news_url:
                    urls.append(news_url)
    
    # Drop Duplicates
    unique_urls = []
    for url in urls:
        if not url in unique_urls:
            unique_urls.append(url)
    
    # Get Contents
    print(f'Ameblo: Find {len(urls)} urls')
    news_urls = []
    contents = []
    for url in unique_urls:
        res = requests.get(url, headers)
        if res.status_code == 200:
            soup = bs(res.content, 'html.parser')
            content = ''
            for item in soup.find_all('p'):
                sentence =  item.get_text()
                sentence = sentence.replace('\n', '').replace('\u3000', '').replace(' ', '').replace('  ', '')
                content += sentence
            if len(content) > 100:
                news_urls.append(url)
                contents.append(content)
            else:
                continue
        time.sleep(1)
            
    df = pd.DataFrame({'URL': news_urls, 'CONTENT': contents})
    return df

# Parameter
# ==================
# search_query: list
def find_note_post_url(item: str):
    result = re.findall('^/.+/n/[0-9a-z]+', item)
    if result:
        return result[0]
    else:
        return None
    
def scrape_note(kwds_param=None):
    if kwds_param:
        kwds = kwds_param
    else:
        kwds = ["行政書士", "民事信託", "相続"]
        
    base_urls = [f'https://note.com/search?q={kwd}&context=note&mode=search' for kwd in kwds]
    for kwd in kwds:
        base_urls.append(f'https://note.com/hashtag/{kwd}?f=popular')
        base_urls.append(f'https://note.com/hashtag/{kwd}?f=new')
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    urls = []
    
    # Get News URL
    for base_url in base_urls:
        res = requests.get(base_url, headers)
        if res.status_code == 200:
            soup = bs(res.content, 'html.parser')
            for item in soup.find_all('a'):
                news_url = find_note_post_url(str(item.get('href')))
                if news_url:
                    urls.append(news_url)
    # Drop Duplicates
    unique_urls = []
    for url in urls:
        if not url in unique_urls:
            unique_urls.append(url)
                    
    print(f'Note: Find {len(unique_urls)} urls')
    news_urls = []
    contents = []
    for url in unique_urls:
        res = requests.get('https://note.com' + url, headers)
        if res.status_code == 200:
            soup = bs(res.content, 'html.parser')
            content = ''
            for item in soup.find_all('p'):
                sentence =  item.get_text()
                sentence = sentence.replace('\n', '').replace('\u3000', '').replace(' ', '').replace('  ', '')
                content += sentence
            if len(content) > 100:
                news_urls.append('https://note.com' + url)
                contents.append(content)
            else:
                continue
        time.sleep(1)
    df = pd.DataFrame({'URL': news_urls, 'CONTENT': contents})
    return df

if __name__ == '__main__':
    scrape_ameba_blog()
    scrape_note()