import os

from django.core.wsgi import get_wsgi_application

from money.env import BASE_DIR, env

env.read_env(os.path.join(BASE_DIR, ".env"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", env.str("DJANGO_SETTINGS_MODULE"))

application = get_wsgi_application()
