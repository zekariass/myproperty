# from re import DEBUG
# from .base import *
from os import getenv


DEBUG = False

# Take environment variables from .env file
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # },
    # "default": {
    #     "ENGINE": "django.db.backends.postgresql",
    #     "NAME": "postgres",
    #     "USER": "grinmove",
    #     "PASSWORD": "Grinmove23",
    #     "HOST": "myproperty.cgtjrid2hzqu.eu-west-2.rds.amazonaws.com",
    #     "PORT": "5432",
    # },
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "grinmove$myproperty2",
        "USER": "grinmove",
        "PASSWORD": "Myproperty@23",
        "HOST": "grinmove.mysql.pythonanywhere-services.com"
        # "PORT": "5432",
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
ALLOWED_HOSTS = ["*"]
