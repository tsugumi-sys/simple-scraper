from typing import List, Optional
from fastapi import FastAPI, Query, Path, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import os

from nlp_process import nlp_process
from send_chat import send_chatwork

app = FastAPI()

templates = Jinja2Templates(directory="templates")
@app.get('/')
async def index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/v1')
async def scrape_nlp(
    search_kwd: Optional[List[str]] = Query(
        None,
        title='スクレイピングで記事検索を行うときの検索キーワード。',
        description='与えられたキーワードでameba blog, noteの記事検索を行います。3つのキーワード指定で記事が200前後集まります。'
    ),
    relate_kwd: Optional[List[str]] = Query(
        None,
        title='スクレイピングで取得した記事との関連性を見つけたいキーワード。',
        description='取得した記事の中から、関連性を見つけたいキーワードをもとに記事の絞り込みを行います。'
    )
):
    result = nlp_process(search_query=search_kwd, kwds_query=relate_kwd)
    kwds = ', '.join(result['keyword'])
    urls = result['url']
    contents = result['content']
    
    send_chatwork(f'[info][title]キーワードからブログ記事を抽出[/title][info][title]キーワード[/title]{kwds}[/info][/info]')
    for i in range(len(urls)):
        send_chatwork(f'[info][title]記事{i + 1}[/title]{urls[i]} \n\n{contents[i]}[/info]')
        
    return result

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))