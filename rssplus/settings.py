"""
Django settings for rssplus project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'davidhweinstein@gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get('GMAIL_PASSWORD')



STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secrte key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
if DEBUG:
    BASE_URL = "test1.com"
else:
    BASE_URL = "https://infocatch.herokuapp.com/"

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [".herokuapp.com","test1.com"]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'subscribe',
    'userSettings',
    'social.apps.django_app.default',
#    'django_extensions',
#    'werkzeug',
)

# Added for social login
SOCIAL_AUTH_FACEBOOK_KEY =os.environ.get('SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET =os.environ.get('SOCIAL_AUTH_FACEBOOK_SECRET')
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY =os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET =os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
SOCIAL_AUTH_TWITTER_KEY =os.environ.get('SOCIAL_AUTH_TWITTER_KEY')
SOCIAL_AUTH_TWITTER_SECRET =os.environ.get('SOCIAL_AUTH_TWITTER_SECRET')
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
SOCIAL_AUTH_LOGIN_ERROR_URL = '/'
TEMPLATE_CONTEXT_PROCESSORS = (
   'django.contrib.auth.context_processors.auth',
   'django.core.context_processors.debug',
   'django.core.context_processors.i18n',
   'django.core.context_processors.media',
   'django.core.context_processors.static',
   'django.core.context_processors.tz',
   'django.contrib.messages.context_processors.messages',
   'social.apps.django_app.context_processors.backends',
   'social.apps.django_app.context_processors.login_redirect',
)
AUTHENTICATION_BACKENDS = (
   'social.backends.facebook.FacebookOAuth2',
   'social.backends.google.GoogleOAuth2',
   'social.backends.twitter.TwitterOAuth',
   'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
#    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware', 
)

ROOT_URLCONF = 'rssplus.urls'

WSGI_APPLICATION = 'rssplus.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
# https://devcenter.heroku.com/articles/django-assets
STATICFILES_DIRS = (
  os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = 'staticfiles'
#STATIC_URL = 'static/'
STATIC_URL = '/static/'

'''
if not os.environ.get("HOME") == "/home":
    # Parse database configuration from $DATABASE_URL
    import dj_database_url
    DATABASES['default'] = dj_database_url.config()
'''

#https://www.youtube.com/watch?v=qLRxkStiaUg&list=PLxxA5z-8B2xk4szCgFmgonNcCboyNneMD&index=22
AUTH_PROFILE_MODULE = 'userSettings.UserSettings'
