from django_jinja import library

from ..utils import get_setting as get_setting_util
from ..utils import get_setting_value


@library.global_function
def setting(key, default=None):
    return get_setting_value(key=key, default=default)


@library.global_function
def get_setting(key):
    return get_setting_util(key=key)
