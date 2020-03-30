#api.wsgi
import sys
sys.path.append('/home/ubuntu/covid/env/lib/python3.6/site-packages')
sys.path.insert(0, '/var/www/html/covid')

from api import app as application
