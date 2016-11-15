from django_jinja import library

from ..utils import get_setting as get_setting_util


@library.global_function
def setting(key):
    obj = get_setting_util(key=key, default=None)
    if not obj:
        return key
    return obj.value()


@library.global_function
def get_setting(key):
    return get_setting_util(key=key)
