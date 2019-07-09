from .base import *

DEBUG = False

# TODO: Update with production host
# ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

# TODO: Point to the production server
DATABASES = {"default": env.db("DATABASE_URL")}