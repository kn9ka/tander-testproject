#! /usr/bin/env python
#https://stackoverflow.com/questions/12365970/wsgi-jquery-example

# Comments form
form = open('views/index.html', 'r').read().encode('utf-8')

import sqlite3
import re
import json
from cgi import escape
import urllib.parse

def css(environ, start_response):
     start_response('200 OK', [('Content-Type', 'text/css')])
     css = open('views/css/main.css','r').read().encode('utf-8')
     
     return [css]
     
def js(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    js = open('views/js/script.js', 'r').read().encode('utf-8')
    
    return [js]
    
def submit(environ, start_response):
    start_response('200 OK', [('Content-Type', 'application/json')])
    if environ['REQUEST_METHOD'] == 'POST':
        print (environ['QUERY_STRING'])
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
    
def index(environ, start_response):
    #This function will be mounted on "/"
    
    html = form
    start_response('200 OK', [('Content-Type', 'text/html')])
    
    return [html]

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
    (r'hello/?$', hello),
    (r'hello/(.+)$', hello),
    (r'city/?$', city),
    (r'submit/?$', submit),
    (r'css/main.css', css),
    (r'js/script.js', js)
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

if __name__ == '__main__':
    
    try:
        # Python's bundled WSGI server
        from wsgiref.simple_server import make_server
        
        # Instantiate the server
        httpd = make_server (
            '', # The host name
            8080, # A port number where to wait for the request
            application # The application object name, in this case a function
        )
        
        httpd.serve_forever()
        
    except KeyboardInterrupt:
        print('Goodbye.')