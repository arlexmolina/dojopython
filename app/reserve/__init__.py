from flask import Blueprint
from flask import g

reserve = Blueprint('reserve', __name__, url_prefix='/')


@reserve.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('environment', g.environment)


@reserve.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.environment = ''
    g.check_request = True

from . import views
