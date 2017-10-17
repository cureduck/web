from urllib import request
import json
import time,os

resp=request.urlopen('https://api.imjad.cn/pixiv/v1/?type=ranking&mode=daily&content=illust&per_page=50&mode=daily')
ranking=json.loads(resp.read().decode('utf-8'),encoding='utf-8')


works=ranking['response']
large_img_urls=[work['image_urls']['large'] for work in works]
ids=[work['id'] for work in works ]

for i in range(len(ids)):
    req=request.Request(large_img_urls[i])


    req.add_header('referer','https://www.pixiv.net/member_illust.php?mode=medium&illust_id='+str(ids[i]))
    req.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')
    req.add_header('Accept-Encoding', 'gzip, deflate, sdch')
    req.add_header('Language','zh-CN,zh;q=0.8')

    resp=request.urlopen(req)

    path='static/data/img/'+str(time.strftime('%Y-%m-%d', time.localtime()))
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path+'/'+str(i)+'.jpg','wb') as f:
        f.write(resp.read())