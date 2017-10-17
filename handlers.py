from coroweb import get,post,auth
from models import User,Blog,Comment
import json
import logging; logging.basicConfig(level=logging.INFO)
import hashlib
from aiohttp import web
import time
import asyncio


COOKIE_NAME='cureduck'
_COOKIE_KEY='private'



@get('/login')
@auth('None')
async def lonin():
    dic={
        '__template__':'login.html'
    }
    return dic


@get('/register')
@auth('None')
async def register():
    dic={
        '__template__':'register.html'
    }
    return dic


@get('/')
@auth('None')
async def index():
    return b'hello'

@get('/portfolio')
@auth('None')
async def portfolio():
    dic={
        '__template__':'portfolio.html'
    }
    return dic


@get('/code')
@auth('None')
async def code():
    dic={
        '__template__':'code.html'
    }
    return dic


@get('/cloud/{id}')
@auth('Owner')
async def cloud(id):
    dic={
        '__template__':'111.html'
    }
    return dic