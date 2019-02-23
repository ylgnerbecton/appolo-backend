from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'desafio',
#         'USER': 'ylgnerbecton',
#         'PASSWORD': 'abc102030#',
#         'HOST': 'db',
#         'PORT': 5432,
#     }
# }

# INSTALLED_APPS += ('debug_toolbar',)

# INTERNAL_IPS = ('127.0.0.1')
# MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

# DEBUG_TOOLBAR_CONFIG = {
#     'DISABLE_PANELS': [
#         'debug_toolbar.panels.redirects.RedirectsPanel',
#     ],
#     'SHOW_TEMPLATE_CONTEXT': True,
# }

# if DEBUG:
#     MIDDLEWARE += ('django_stackoverflow_trace.DjangoStackoverTraceMiddleware', )
#     DJANGO_STACKOVERFLOW_TRACE_SEARCH_SITE = "googlesearch"


# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += ['django_extensions', ]