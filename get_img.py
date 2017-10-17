from urllib import request
import json
import time,os
from bs4 import BeautifulSoup as bs

def get_by_id(id):
    resp=request.urlopen('https://api.imjad.cn/pixiv/v1/?type=illust&id='+str(id))
    json_content=json.loads(resp.read().decode('utf-8'),encoding='utf-8')
    large_img_url=json_content['response'][0]['image_urls']['large']

    req=request.Request(large_img_url)
    req.add_header('referer','https://www.pixiv.net/member_illust.php?mode=medium&illust_id='+str(id))
    req.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')
    req.add_header('Accept-Encoding', 'gzip, deflate, sdch')
    req.add_header('Language','zh-CN,zh;q=0.8')

    resp=request.urlopen(req)

    return resp

def save(resp,name):
    path='static/data/img/'+str(time.strftime('%Y-%m-%d', time.localtime()))
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path+'/'+str(name)+'.jpg','wb') as f:
        f.write(resp.read())


def pixiv_download():
    ranking_html=request.urlopen('https://www.pixiv.net/ranking.php?mode=daily&content=illust').read()
    bs_ranking=bs(ranking_html,'html.parser')
    ranking_items=bs_ranking.find_all(attrs='ranking-item')

    ids,i=[],0
    for item in ranking_items:
        save(get_by_id(item['data-id']),i)
        i+=1


