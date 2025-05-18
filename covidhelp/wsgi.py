import os
import sys
import logging

# Configure logging first
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
)
logger = logging.getLogger(__name__)

# Add the project root directory to Python path
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, current_dir)

logger.debug(f"Python path: {sys.path}")
logger.debug(f"Current directory: {current_dir}")

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'covidhelp.settings')

try:
    from django.core.wsgi import get_wsgi_application
    logger.info("Importing get_wsgi_application succeeded")
    _application = get_wsgi_application()
    logger.info("Django application loaded successfully")
except Exception as e:
    logger.error(f"Failed to load Django application: {str(e)}")
    logger.error(f"Current sys.path: {sys.path}")
    raise

def application(environ, start_response):
    logger.debug(f"Received request for: {environ.get('PATH_INFO')}")
    
    if environ['PATH_INFO'] == '/health/':
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [b'OK']
    
    return _application(environ, start_response) 