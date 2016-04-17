"""
Django settings for djangoProject project on Heroku. Fore more info, see:
https://github.com/heroku/heroku-django-template

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "^ab3n9-*_87@zr=yu2uo!h6+bp(=x#q&h6r0og5@f(_20uov=c"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django_extensions',

	'oauth2_provider',
	'rest_framework',
	'rest_framework.authtoken',
	'rest_framework_social_oauth2',
	'social.apps.django_app.default',
	'rest_social_auth',
	'gunicorn',
	'corsheaders',
	'lessons',
)

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'django.middleware.security.SecurityMiddleware',
	'corsheaders.middleware.CorsMiddleware',
)

ROOT_URLCONF = 'djangoProject.urls'

TEMPLATES = (
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
				'social.apps.django_app.context_processors.backends',
				'social.apps.django_app.context_processors.login_redirect',
			],
			'debug': DEBUG,
		},
	},
)

WSGI_APPLICATION = 'djangoProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

# Update database configuration with $DATABASE_URL.
#if not 'DATABASE_URL' in os.environ:
#    os.environ['DATABASE_URL'] = 'postgres://qdvhboeogqfxst:aX1EdOLLTEn81yj7492fK2_aQ_@ec2-107-21-101-67.compute-1.amazonaws.com:5432/dbuh639t95mo72'
if not DEBUG:
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql_psycopg2',
			'NAME': 'dbuh639t95mo72',
			'USER': 'qdvhboeogqfxst',
			'PASSWORD': 'aX1EdOLLTEn81yj7492fK2_aQ_',
			'HOST': 'ec2-107-21-101-67.compute-1.amazonaws.com',  
			'PORT': '5432',
		}
	}
else:
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql_psycopg2',
			'NAME': 'chime',
			'USER': '',
			'PASSWORD': '',
			'HOST': 'localhost',  
			'PORT': '',
		}
	}

AUTH_PASSWORD_VALIDATORS = (
	{
		'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	},
)

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'
#TIME_ZONE = 'UTC'
#LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_L10N = True
USE_TZ = True
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
	os.path.join(PROJECT_ROOT, 'static'),
]

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

REST_FRAMEWORK = {
	# Use Django's standard `django.contrib.auth` permissions,
	# or allow read-only access for unauthenticated users.
	'DEFAULT_PERMISSION_CLASSES': [
		'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
	#    'rest_framework.permissions.IsAdminUser',
	],
	'PAGE_SIZE': 10,
	'DEFAULT_AUTHENTICATION_CLASSES': (
		'oauth2_provider.ext.rest_framework.OAuth2Authentication',
		'rest_framework_social_oauth2.authentication.SocialAuthentication',
		),
}

SOCIAL_AUTH_PIPELINE = (
	'social_auth.backends.pipeline.social.social_auth_user',
	'social_auth.backends.pipeline.social.associate_user',
	'social_auth.backends.pipeline.social.load_extra_data',
	'social_auth.backends.pipeline.user.update_user_details'
)

AUTH_USER_MODEL = 'lessons.User'

AUTHENTICATION_BACKENDS = (
		# Facebook OAuth2
	'social.backends.facebook.FacebookOAuth2',
	'social.backends.google.GoogleOAuth2',
	'social.backends.twitter.TwitterOAuth',
	'rest_framework_social_oauth2.backends.DjangoOAuth2',
	'django.contrib.auth.backends.ModelBackend',
)
CORS_ORIGIN_ALLOW_ALL = True
SOCIAL_AUTH_URL_NAMESPACE = 'social'
"""
TEMPLATE_CONTEXT_PROCESSORS = (
	'social.apps.django_app.context_processors.backends',
	'social.apps.django_app.context_processors.login_redirect',
)
"""
# Facebook configuration
SOCIAL_AUTH_FACEBOOK_KEY = '640270719458713'
SOCIAL_AUTH_FACEBOOK_SECRET = 'ce8ba5f8607988faace4591f87cdba49'

# Define SOCIAL_AUTH_FACEBOOK_SCOPE to get extra permissions from facebook. Email is not sent by default, to get it, you must request the email permission:
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
"""
SOCIAL_AUTH_TWITTER_KEY = 'Your Twitter Key'
SOCIAL_AUTH_TWITTER_SECRET = 'Your Twitter Secret'
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'your secret id'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'your secret key'
SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_EMAILS = ['email address']
"""
# https://github.com/st4lk/django-rest-social-auth
# https://github.com/PhilipGarnero/django-rest-framework-social-oauth2
# https://pypi.python.org/pypi/django-socialprofile/0.2.2#facebook
#url = "https://graph.facebook.com/v2.6/me?fields=id%2Cname%2Clocation%2Cbirthday&access_token=EAAJGUqTLHZAkBAHUZBugSoLHNzIO4n72aO4KKr8mQpQInJZCaZCcLnZCIRgPgzKGdxlns9wTsn68ucrpwp9ZAivwB33xZB8Eo2e3mb4ABe8g7DIrkp2liB9VzAVCrShyLt6TNL6iN0K6TXOUsMyr1ebvZBOkIZAczvi6iVL90QOfdFgZDZD"
#curl -X GET "https://graph.facebook.com/v2.6/me?fields=id%2Cname%2Clocation%2Cbirthday&access_token=CAAJGUqTLHZAkBAL7c8an0bOqnoGOlnAQDUVZB4GvZBTTE0rR9kNL7CVZAOhWxPuXZA2JmVKP7btrJ3PZBnZAC1geCmEY6s4gH0pYfn1w94roAZCYazsxYC2QRFV61iFiXwUeDhZCDIVEbl1WD5w4QcLZAPYuIgDFZAtqqqauKRlLU3GNIO8wx9QvylZB7OH37vdwpzncle9ZBLGjnhwZDZD"


