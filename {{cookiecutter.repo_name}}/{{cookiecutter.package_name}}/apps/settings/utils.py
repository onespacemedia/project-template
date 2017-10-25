from .models import Setting


def get_setting(key, default=None):
    try:
        return Setting.objects.get(key=key)
    except Setting.DoesNotExist:
        return default


def get_setting_value(key, default=None):
    setting_obj = get_setting(key)
    if setting_obj is not None:
        return setting_obj.value
    return default
