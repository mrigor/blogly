import os
import subprocess
import sys
import uuid

FILENAME = os.path.abspath(__file__)
DIRNAME = os.path.dirname(FILENAME)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASE_ENGINE = 'postgresql_psycopg2'
DATABASE_USER = '' #local_settings
DATABASE_PASSWORD = '' #local_settings
DATABASE_HOST = 'localhost'
DATABASE_PORT = '5432'

DATABASE_DEFAULT = 'blogly'
DATABASE_EVENTS = 'event_log'
DATABASE_NAME = DATABASE_DEFAULT

DATABASE_CONFIG = {
    '_default': {
        'user': 'DATABASE_USER',
        'pass': 'DATABASE_PASSWORD',
        'host': 'DATABASE_HOST',
        'port': 'DATABASE_PORT',
    },
    # override as necessary...
    DATABASE_DEFAULT: {},
    DATABASE_EVENTS: {},
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# TODO option to "remember me on this computer"
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

import socket
SERVERNAME = socket.gethostname()

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

# adds the user and path to the template context
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

# Set ROOT_URLCONF to 'urls.api' in local_settings on api server
ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(DIRNAME, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.humanize',
    'django.contrib.markup',
    'blog',
    'accounts',
    'api',
    'comments',
    'profiles',
)

MEDIA_ROOT = os.path.join(DIRNAME, 'static')

BYTECODE_CACHE_DIR = DIRNAME + '/static/bytecode/'

# grab the current code revision for use in the code
CODE_REVISION = None
#try:
#    p = subprocess.Popen(
#        ['git', 'rev-parse', '--short', 'HEAD'],
#        cwd=DIRNAME,
#        stdout=subprocess.PIPE,
#        stderr=subprocess.PIPE,
#    )
#    if p.wait() == 0:
#        CODE_REVISION = p.communicate()[0].strip()
#    else:
#        # fall back to using a uuid
#        error = p.communicate()[1].strip()
#        print >> sys.stderr, 'Failed to grab code revision from git: %s' % error
#except OSError as e:
#    print >> sys.stderr, 'Failed to create git process: %s' % e
if not CODE_REVISION:
    CODE_REVISION = uuid.uuid4().get_hex()

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
AUTH_PROFILE_MODULE = 'profiles.UserProfile'
