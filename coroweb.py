import functools,asyncio,inspect
from aiohttp import web
import os,logging,json
from config import COOKIE_NAME
from cookie import cookie2user
from models import User,Blog,Comment

def get(path):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args,**kw):
            return func(*args,**kw)
        wrapper.__method__='GET'
        wrapper.__route__=path
        return wrapper
    return decorator

def post(path):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args,**kw):
            return func(*args,**kw)
        wrapper.__method__='POST'
        wrapper.__route__=path
        return wrapper
    return decorator

def auth(auth):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args,**kw):
            return func(*args,**kw)
        wrapper.auth=auth
        return wrapper
    return decorator

class RequestHandler(object):

    def __init__(self,app,fn):
        self._app=app
        self._func=fn

    async def __call__(self, request):

        if self._func.auth=='None':
            pass

        elif self._func.auth=='Owner':
            user = await cookie2user(request.cookies.get(COOKIE_NAME))
            request.__user__=user
            if user is None:return web.HTTPUnauthorized()
            path,id=request.path,request.match_info['id']
            if path.startswith('/blog')or path.startswith('/api/blog'):
                item=await Blog.find(id)
                if user.id != item.user_id and user.admin is  False: return web.HTTPUnauthorized()
            elif path.startswith('/comment')or path.startswith('/api/comment'):
                item=await Comment.find(id)
                if user.id != item.user_id and user.admin is False: return web.HTTPUnauthorized()
            elif path.startswith('/cloud')or path.startswith('/api/cloud'):
                if id!=user.id: return web.HTTPUnauthorized()




        elif self._func.auth=='Admin':
            user = await cookie2user(request.cookies.get(COOKIE_NAME))
            request.__user__=user
            if user is None:
                return web.HTTPUnauthorized()
            elif user.admin is False:
                return web.HTTPUnauthorized()
            else:
                pass


        if request.method=='POST':
            if request.content_type=='application/json':
                data=await request.json()
                res= await self._func(**data)
                return res
            else:
                #to be resolved
                pass


        if request.method=='GET':
            kw=request.match_info
            res=await self._func(**kw)

            return res




def add_route(app,fn):
    method=getattr(fn,'__method__',None)
    path=getattr(fn,'__route__',None)
    if path is None or method is None:
        raise ValueError()
    if not asyncio.iscoroutine(fn) and not inspect.isgeneratorfunction(fn):
        fn=asyncio.coroutine(fn)
    logging.info('add route %s %s => %s(%s)' % (method, path, fn.__name__, ', '.join(inspect.signature(fn).parameters.keys())))

    app.router.add_route(method,path,RequestHandler(app,fn))

def add_routes(app,module_name):
    n=module_name.rfind('.')
    if n == (-1):
        mod = __import__(module_name, globals(), locals())
    else:
        name = module_name[n+1:]
        mod = getattr(__import__(module_name[:n], globals(), locals(), [name]), name)
    for attr in dir(mod):
        if attr.startswith('_'):
            continue
        fn = getattr(mod, attr)
        if callable(fn):
            method = getattr(fn, '__method__', None)
            path = getattr(fn, '__route__', None)
            if method and path:
                add_route(app, fn)

def add_static(app):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    app.router.add_static('/static/', path)
    logging.info('add static %s => %s' % ('/static/', path))

