from coroweb import get,post,auth
from models import *
import json,logging
import asyncio
from aiohttp import web
from cookie import user2cookie

from config import COOKIE_NAME
import os

@get('/api/users')
@auth('Admin')
async def get_users():
    users=await User.findAll()
    return users

@get('/api/blogs')
@auth('None')
async def get_blogs():
    blogs=await Blog.findAll()
    return blogs


@get('/api/blog/id={id}')
@auth('None')
async def get_blog_by_id(id):
    blog=await Blog.find(id)
    return blog

@get('/api/blog/id={id}/comments')
@auth('None')
async def get_blog_comments(id):
    comments=await Comment.findAll(where='blog_id=?',args=(id,))
    return comments

@get('/api/user/id={id}/blogs')
@auth('None')
async def get_user_blogs(id):
    blogs=await Blog.findAll(where='user_id=?',args=('id',))
    return blogs



#anything handle requires 'Owner' auth will be passed a object
@get('/api/blog/id={id}/delete')
@auth('Owner')
async def blog_delete(blog):
    blog.remove()


@post('/api/register')
@auth('None')
async def register(name,passwd,email=None,image=None):
    users=await User.findAll('name=?',name)
    if len(users)>0 :
        return b'name already registered'
    else:
        u=User(name=name,passwd=passwd,email=email,image=image)
        await u.save()
        return b'register successfully'
    await u.save()


@get('/api/logout')
@auth('None')
async def logout():
    resp=web.Response()
    resp.set_cookie(COOKIE_NAME,value='--deleted---')
    return resp


@post('/api/authenticate')
@auth('None')
async def authenticate(name,passwd):
    user=await User.findAll(' name=?',name)
    user=user[0]
    if passwd==user.passwd:
        resp=web.json_response(data=user)
        resp.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
        return resp
    else:
        return b'fuck off'




@get('/api/img/{date}')
@auth('None')
async def get_url_for_img(date):
    path='static/data/img/'+ date

    urls=os.listdir(path)
    urls=['/'+path+'/'+x for x in urls if x.endswith('.jpg') ]
    return urls


@get('/api/cloud/{id}')
@auth('Owner')
async def get_personal_cloud(id):
    path='cloud/'+str(id)
    if not os.path.exists(path):
        os.makedirs(path)

    dirs=os.listdir(path)
    return dirs


@post('/api/cloud/{id}')
@auth('Owner')
async def upload_file(id):
    path='cloud/'+str(id)
    if not os.path.exists(path):
        os.makedirs(path)

