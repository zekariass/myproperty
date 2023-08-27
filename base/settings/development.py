from .base import *
from os import getenv

DEBUG = True
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


DATABASES = {
    # "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "grinmove",
        "PASSWORD": "Grinmove23",
        "HOST": "grinmove-test-db.cgtjrid2hzqu.eu-west-2.rds.amazonaws.com",
        "PORT": "5432",
    }
    # "default": {
    #     "ENGINE": "django.db.backends.postgresql",
    #     "NAME": getenv("DB_NAME"),
    #     "USER": getenv("DB_USER"),
    #     "PASSWORD": getenv("DB_PASSWORD"),
    #     "HOST": getenv("DB_HOST"),
    #     "PORT": getenv("DB_PORT"),
    # }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
ALLOWED_HOSTS = ["*"]
