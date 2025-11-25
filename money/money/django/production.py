"""
Config for production environment.
"""

from money.env import env

from .base import *

ALLOWED_HOSTS = ["money.vps.dmytrienko.com"]
CSRF_TRUSTED_ORIGINS = ["https://money.vps.dmytrienko.com"]
