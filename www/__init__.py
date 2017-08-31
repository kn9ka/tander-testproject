#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import sqlite3
import re
import json
import os
import urllib.parse
from string import Template

from cgi import escape
from . import template

def render(filename):
    result = None
    name = os.path.dirname(os.path.abspath(__file__))  + filename
    with open(name, 'r') as f:
        result = f.read()
    return [result.encode('utf-8')]

def index (environ, start_response):
    # "/" mount
    start_response('200 OK', [('Content-Type', 'text/html')])
    result = render('/templates/index.html')
    return result

def css(environ, start_response):
     start_response('200 OK', [('Content-Type', 'text/css')])
     result = render('/static/main.css')
     return result
     
def js(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    result = render('/static/script.js')
    return result
    
def submit(environ, start_response):
    start_response('200 OK', [('Content-Type', 'application/json')])
    if environ['REQUEST_METHOD'] == 'POST':
        try:
            request_body_size = int(environ['CONTENT_LENGTH'])
            request_body = environ['wsgi.input'].read(request_body_size)
            decoded = urllib.parse.parse_qs(request_body.decode('utf-8'))
            print(decoded)
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
        except:
            print ('nope')

    #print(environ)
    return [b'Success']

def city(environ, start_response):
    
    start_response('200 OK', [('Content-Type', 'application/json')])
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    result = cursor.execute('''SELECT city.name, region.name FROM city LEFT JOIN region ON city.id_region=region.id;''')
    rows = result.fetchall()
    r = json.dumps(rows)
    return [bytes(r, 'utf-8')]

def getAllRows(environ, start_response):
    start_response('200 OK', [('Content-Type', 'application/json')])
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    result = cursor.execute("SELECT * FROM maindata;")
    rows = result.fetchall()
    r = json.dumps(rows)
    return [bytes(r, 'utf-8')]
    
def getAboveFive(environ, start_response):
    start_response('200 OK', [('Content-Type', 'application/json')])
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    
    result = cursor.execute("SELECT region, city, COUNT(region), COUNT(city) FROM maindata GROUP BY region, city HAVING COUNT(region) >= 5;")
    rows = result.fetchall()
    r = json.dumps(rows)
    
    return [bytes(r, 'utf-8')] 

def commentForm(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    result = render('/templates/entry.html')
    
    return result

def viewForm(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    result = render('/templates/list.html')

    return result

def statForm (environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    result = render('/templates/stat.html')

    return result
    
def hello(environ, start_response):
    #Example route
    
    # get the name from the url if it was specified there.
    args = environ['myapp.url_args']
    if args:
        subject = escape(args[0])
    else:
        subject = 'World'
    start_response('200 OK', [('Content-Type', 'text/html')])
    
    return [bytes('''Hello %(subject)s Hello %(subject)s! ''' % {'subject': subject}, 'utf-8')]

def not_found(environ, start_response):
    """Called if no URL matches."""
    start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
    
    return [b'Not Found']

# map urls to functions
urls = [
    (r'^$', index),
    (r'comment/?$', commentForm),
    (r'view/?$',viewForm),
    (r'stat/?$', statForm),
    (r'getAboveFive/?$', getAboveFive),
    (r'hello/?$', hello),
    (r'hello/(.+)$', hello),
    (r'city/?$', city),
    (r'getAllRows/?$', getAllRows),
    (r'submit/?$', submit),
    (r'/main.css', css),
    (r'/script.js', js)
]

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

def run(host, port):
    # Python's bundled WSGI server
    try:
        from wsgiref.simple_server import make_server
        
        # Instantiate the server
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