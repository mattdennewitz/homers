from __future__ import unicode_literals
import os


DEBUG = True
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgres://localhost/homers')
DATA_DIR = os.path.realpath(
    os.path.join(os.path.dirname(__file__),
                 os.pardir,
                 'game-data'))

# app settings
PER_PAGE = 20
DAYS_PER_PAGE = 7


# allow for config overrides
try:
    from local_config import *
except ImportError:
    pass
