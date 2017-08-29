#! /usr/bin/env python

import cgi

# Comments form
form = open('views/index.html', 'r').read().encode('utf-8')

def application(environ, start_response):
    html = form

    # if environ['REQUEST_METHOD'] == 'POST':
    #     post_env = environ.copy()
    #     post_env['QUERY_STRING'] = ''
    #     post = cgi.FieldStorage(
    #         fp=environ['wsgi.input'],
    #         environ=post_env,
    #         keep_blank_values=True
    #     )
        
    #     html = bytes(('Hello, ' + '!'), 'utf-8')
        
    start_response('200 OK', [('Content-Type', 'text/html')])
    
    return [html]

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