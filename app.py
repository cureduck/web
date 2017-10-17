import logging; logging.basicConfig(level=logging.INFO)

import asyncio,os,json,time
from datetime import datetime

from aiohttp import web
from jinja2 import Environment,FileSystemLoader
import orm
from response_factory import response_factory


from coroweb import add_routes,add_static

def init_jinja2(app,**kw):
    logging.info('init jinja2...')
    options=dict(
        autoescape=kw.get('autoescape',True),
        block_start_string=kw.get('block_start_string','{%'),
        block_end_string=kw.get('block_end_string','%}'),
        variable_start_string=kw.get('variable_start_string','{{{'),
        variable_end_string=kw.get('variable_end_string','}}}'),
        auto_reload=kw.get('auto_reload',True)
    )
    path=kw.get('path',None)
    if path is None:
        path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates')
    env=Environment(loader=FileSystemLoader(path),**options)
    filters=kw.get('filters',None)
    if filters is not None:
        for name,f in filters.items():
            env.filters[name]=f
    app['__templating__']=env


def index(request):
    return web.Response(body=b'hello')


async def init(loop):
    _pool=await orm.create_pool(loop)
    app=web.Application(loop=loop,middlewares=[response_factory])
    init_jinja2(app)
    add_static(app)
    add_routes(app,'handlers')
    add_routes(app,'apis')

    srv=await loop.create_server(app.make_handler(),'192.168.31.13',9000)
    logging.info('server started...')
    return srv

loop=asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()