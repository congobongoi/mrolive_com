activate_this = 'C:/Users/Adam/Envs/mrolive_portal/Scripts/activate_this.py'
# execfile(activate_this, dict(__file__=activate_this))
exec(open(activate_this).read(),dict(__file__=activate_this))
import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('c:/users/adam/envs/mrolive_portal/lib/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('C:/Users/Adam/Envs/mro_portal/mo_template/mo_template/')
sys.path.append('C:/Users/Adam/Envs/mro_portal/mo_template/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'mo_template.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mo_template.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
