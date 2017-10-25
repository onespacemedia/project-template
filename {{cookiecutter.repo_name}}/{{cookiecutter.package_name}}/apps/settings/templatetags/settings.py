from django_jinja import library

from ..utils import get_setting as get_setting_util
from ..utils import get_setting_value


@library.global_function
def setting(key, default=None):
    value = get_setting_value(key=key, default=None)
    if value is None:
        # rather than 'return default or key' - means coverage isn't fooled?
        if default is not None:
            return default
        return key
    return value


@library.global_function
def get_setting(key):
    return get_setting_util(key=key)
