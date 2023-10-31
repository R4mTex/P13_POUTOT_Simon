from . import *
import psycopg2

# SECURITY WARNING: keep the secret key used in Toolion secret!
SECRET_KEY="_0jm6arn^)d2b8m=c6cxng$xbs390xicml9n!klh9*p$3s@pey"

# SECURITY WARNING: don't run with debug turned on in Toolion!
DEBUG=True

INSTALLED_APPS = [
    'authentication',
    'blog',
    'widget_tweaks',
    'phonenumber_field',
    'jquery',
    'jsignature',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

DATABASES = {
    'default': {
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
         'NAME': 'toolshare_db',
         'USER': 'simon',
         'PASSWORD': 'Kundera1',
         'HOST': 'localhost',
         'PORT': '5432',
    }
}

# Reset Password Settings
EMAIL_HOST="smtp.gmail.com"
EMAIL_HOST_USER="founder.toolshare@gmail.com"
EMAIL_HOST_PASSWORD="raaanxhaptucttlm"

# Google Maps API Key
GOOGLE_MAPS_API_KEY="AIzaSyD1ckgetM8cnzdgwd1XpEetOhxghe5w82M"