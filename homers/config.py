from __future__ import unicode_literals
import os


DEBUG = True

SQLALCHEMY_DATABASE_URI = os.environ.get(
    'HOMERS_DATABASE_URI', 'postgres://localhost/homers')

DATA_DIR = os.path.realpath(
    os.path.join(os.path.dirname(__file__),
                 os.pardir,
                 'game-data'))

PER_PAGE = 25

# allow for config overrides
try:
    from local_config import *
except ImportError:
    pass
