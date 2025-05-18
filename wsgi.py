def application(environ, start_response):
    if environ['PATH_INFO'] == '/health/':
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [b'OK']
    
    # Import Django WSGI application only for non-health check requests
    from covidhelp.wsgi import application as django_application
    return django_application(environ, start_response) 