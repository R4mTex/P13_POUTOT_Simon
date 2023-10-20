from . import *
import psycopg2

# SECURITY WARNING: keep the secret key used in Toolion secret!
SECRET_KEY="django-insecure-lpxfa$ctf^n0+w7qlbo536ojr7ab!x@k_d#wc80vays9$5^jix"

# SECURITY WARNING: don't run with debug turned on in Toolion!
DEBUG=True

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