#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import sqlite3
import re
import json
import os
import urllib.parse
import traceback

from string import Template
from . import template
from cgi import escape


#рендер шаблона
def render(filename, **kwargs):
    result = None
    fullname = os.path.dirname(os.path.abspath(__file__))  + filename
    with open(fullname, 'r') as f:
        data = f.read()
        tpl = template.Template()
        data = tpl.render(data)
        r = Template(data)
        result = r.substitute(kwargs['pagedata'])
    return [bytes(result, 'utf-8')]

# mount на "/"
def index (environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    result = render('/templates/index.html', pagedata={'title': 'start page'})
    return result

#mount на все подключения (script.js, main.css)
def static(environ, start_response):
    path = environ['PATH_INFO']
    filetype = path.split('.')[1]
    if filetype == 'js':
        start_response('200 OK', [('Content-Type', 'text/javascript')])
        fullname = os.path.dirname(os.path.abspath(__file__)) + '/' + path
        
        with open(fullname, 'r') as f:
            result = [bytes(f.read(), 'utf-8')]
            
    else:
        start_response('200 OK', [('Content-Type', 'text/css')])
        fullname = os.path.dirname(os.path.abspath(__file__)) + '/' + path
        
        result = render(path, pagedata={})

    return result

# mount на нажатие кнопки "submit", route = /comment/
def submit(environ, start_response):
    start_response('200 OK', [('Content-Type', 'application/json')])
    if environ['REQUEST_METHOD'] == 'POST':
        try:
            request_body_size = int(environ['CONTENT_LENGTH'])
            request_body = environ['wsgi.input'].read(request_body_size)
            decoded = urllib.parse.parse_qs(request_body.decode('utf-8'))

            if decoded.get('patronymic') is None:
                decoded['patronymic'] = ['']
            
            conn = sqlite3.connect('main.db')
            cursor = conn.cursor()
            
            cursor.execute("INSERT INTO maindata (second_name ,first_name, patronymic, region, city, mobile, email, comment) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", (
                decoded['first_name'] + 
                decoded['second_name'] +
                decoded['patronymic'] +
                decoded['region'] +
                decoded['city'] +
                decoded['mobile'] +
                decoded['email'] +
                decoded['comment']
            ))
            
            conn.commit()
            conn.close()
            
            return [b'1']
            
        except:
            print('Error in submit')
            return [b'0']

#mount на кнопку "delete row", route = /view/
def deleteRow(environ, start_response):
    start_response('200 OK', [('Content-Type', 'application/json')])
    if environ['REQUEST_METHOD'] == 'POST':
        request_body_size = int(environ['CONTENT_LENGTH'])
        request_body = environ['wsgi.input'].read(request_body_size)
        
        decoded = urllib.parse.parse_qs(request_body.decode('utf-8'))
        
        conn = sqlite3.connect('main.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM maindata where id = ?;", (decoded['rowId']))
            
            conn.commit()
            conn.close()
        except:
            print('Error in delete')
            return [b'0']
        
    return [b'1']

#загрузка локаций для index.html
def getLocations(environ, start_response):
    start_response('200 OK', [('Content-Type', 'application/json')])
    
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    result = cursor.execute('''SELECT city.name, region.name FROM city LEFT JOIN region ON city.id_region=region.id;''')
    rows = result.fetchall()
    r = json.dumps(rows)
    
    conn.commit()
    conn.close()
    
    return [bytes(r, 'utf-8')]
    
#загрузка данных для list.html, route = '/view/'
def getAllRows(environ, start_response):
    start_response('200 OK', [('Content-Type', 'application/json')])
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    result = cursor.execute("SELECT * cFROM maindata;")
    rows = result.fetchall()
    r = json.dumps(rows)
    
    conn.commit()
    conn.close()
    
    return [bytes(r, 'utf-8')]
    
#mount на "/comment/"
def commentForm(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    result = render('/templates/entry.html', pagedata={'title': 'Comment Entry'})
    
    return result
    
#mount на "/view/"
def viewForm(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    result = render('/templates/list.html', pagedata={'title': 'View page'})

    return result

#mount на "/stat/"
def statForm (environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    result = render('/templates/stat.html', pagedata={'title': 'Region stat page'})

    return result

#загрузка коментов по регионам
def getCommentsByRegion(environ, start_response):
    start_response('200 OK', [('Content-Type', 'application/json')])
    if environ['REQUEST_METHOD'] == 'POST':
        
        conn = sqlite3.connect('main.db')
        cursor = conn.cursor()
        result = cursor.execute("select maindata.region, count(*), region.id from maindata left join region on region.name = maindata.region group by region order by region;")

        rows = result.fetchall()
        r = [bytes(json.dumps(rows), 'utf-8')]
        
        conn.commit()
        conn.close()
        
    return r

#загрузка коментов по городам
def getCommentsByCity(environ, start_response):
    start_response('200 OK', [('Content-Type', 'application/json')])

    if environ['REQUEST_METHOD'] == 'POST':
        request_body_size = int(environ['CONTENT_LENGTH'])
        request_body = environ['wsgi.input'].read(request_body_size)
        decoded = urllib.parse.parse_qs(request_body.decode('utf-8'))
    
    id = decoded['regionId']
    
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    result = cursor.execute("select city, count(*) from maindata left join region on maindata.region = region.name group by city having region.id = ? order by city;  ", (id))
    rows = result.fetchall()
    r = [bytes(json.dumps(rows), 'utf-8')]
    
    conn.commit()
    conn.close()
    
    return r

#mount на "/stat/{region id}"
def statCityForm (environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    result = render('/templates/cityStat.html', pagedata={'title': 'City stat page'})
    
    return result

# 404
def not_found(environ, start_response):
    """Called if no URL matches."""
    start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
    
    return [b'Not Found']

# карта маршрутов
urls = [
    (r'^$', index),
    (r'comment/?$', commentForm),
    (r'view/?$',viewForm),
    (r'stat/$', statForm),
    (r'getCommentsByCity/$', getCommentsByCity),
    (r'stat/(.+)/$', statCityForm),
    (r'getCommentsByRegion/?$', getCommentsByRegion),
    (r'getLocations/?$', getLocations),
    (r'getAllRows/?$', getAllRows),
    (r'submit/?$', submit),
    (r'delete/?$', deleteRow),
    (r'static/(?P<filename>.*)$', static)
]

#базовый запуск WSGI приложения
def application(environ, start_response):
    """
    The main WSGI application. Dispatch the current request to
    the functions from above and store the regular expression
    captures in the WSGI environment as  `myapp.url_args` so that
    the functions from above can access the url placeholders.

    If nothing matches call the `not_found` function.
    """
    
    path = environ.get('PATH_INFO', '').lstrip('/')
    for regex, callback in urls:
        match = re.search(regex, path)
        if match is not None:
            environ['myapp.url_args'] = match.groups()
            return callback(environ, start_response)
            
    return not_found(environ, start_response)

# базовый запуск WSGI сервера
def run(host, port):
    try:
        from wsgiref.simple_server import make_server
        
        httpd = make_server (
            host, # The host name
            port, # A port number where to wait for the request
            application # The application object name
        )
        print('Starting server on port: %s' % port)
        httpd.serve_forever()
        
    except KeyboardInterrupt:
        print('Server stopped by keyinterupt')
        
    except BaseException as e:
        print('Error during work: %s' % e)