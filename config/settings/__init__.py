import os

DEV_MODE = 'development'
PROD_MODE = 'production'
mode = os.environ.get('DJANGO_ENVIRONMENT_MODE', DEV_MODE)

if mode == PROD_MODE:
    from .production import *
else:
    from .development import *
